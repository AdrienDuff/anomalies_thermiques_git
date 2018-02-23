from libtiff import TIFF
import numpy as np

import os
import shutil
import pickle

couleur_positif_save_path = "../../Data/Melange_imagettes_jour/Couleur/Positif/"
couleur_negatif_save_path = "../../Data/Melange_imagettes_jour/Couleur/Negatif/"
greyscale_positif_save_path = "../../Data/Melange_imagettes_jour/Greyscale/Positif/"
greyscale_negatif_save_path = "../../Data/Melange_imagettes_jour/Greyscale/Negatif/"

pickle_save_path = "../../Data/"

def create_dataset_pickle(pickle_name = "default.pickle" ,augmented = False,couleur = False):
  if couleur == True:
    positif_path = couleur_positif_save_path
    negatif_path = couleur_negatif_save_path
  else:
    positif_path = greyscale_positif_save_path
    negatif_path = greyscale_negatif_save_path

  #listes des fichiers
  X = [] # On enregistre dedans nos données
  Y = [] # On enregistre dedans nos labels
  path = positif_path
  for file in os.listdir(path):
    if file.endswith(".tif"): # Ce sont les véritables images
      tif_file = TIFF.open(path + file, mode='r')
      imagette = tif_file.read_image()
      X.append(imagette)
      Y.append(1)
    elif augmented == True:
      for file_in_directory in os.listdir(path + file):
        if file_in_directory.endswith(".tif"): # Ce sont les images générées
          tif_file = TIFF.open(path + file + "/" + file_in_directory, mode='r')
          imagette = tif_file.read_image()
          X.append(imagette)
          Y.append(1)

  path = negatif_path
  for file in os.listdir(path):
    if file.endswith(".tif"): # Ce sont les véritables images
      tif_file = TIFF.open(path + file, mode='r')
      imagette = tif_file.read_image()
      X.append(imagette)
      Y.append(0)
    elif augmented == True:
      for file_in_directory in os.listdir(path + file):
        if file_in_directory.endswith(".tif"): # Ce sont les images générées
          tif_file = TIFF.open(path + file + "/" + file_in_directory, mode='r')
          imagette = tif_file.read_image()
          X.append(imagette)
          Y.append(0)


  X = np.array(X)
  Y = np.array(Y)


  print(X.shape)
  print(Y.shape)

  pickle.dump([X, Y], open( pickle_save_path + pickle_name, 'wb' )) # We store the data




if __name__ == "__main__":
  create_dataset_pickle(pickle_name = "col_augmented.pickle", augmented = True, couleur = True)
  create_dataset_pickle(pickle_name = "col_not_augmented.pickle", augmented = False, couleur = True)
  create_dataset_pickle(pickle_name = "grey_augmented.pickle", augmented = True, couleur = False)
  create_dataset_pickle(pickle_name = "grey_not_augmented.pickle", augmented = False, couleur = False)
