import tifffile as tiff
import numpy as np
import os
import shutil

from PIL import Image
from libtiff import TIFF
from keras.preprocessing.image import ImageDataGenerator,array_to_img

# ------- y
# |
# |
# |
#\ /
# x


couleur_positif_save_path = "../../Data/Melange_imagettes_jour/Couleur/Positif/"
couleur_negatif_save_path = "../../Data/Melange_imagettes_jour/Couleur/Negatif/"
greyscale_positif_save_path = "../../Data/Melange_imagettes_jour/Greyscale/Positif/"
greyscale_negatif_save_path = "../../Data/Melange_imagettes_jour/Greayscale/Negatif/"

def generate_imagettes(imagette_name,directory_path, nb_generate = 30, clear_directory=True):
  tif_file = TIFF.open(directory_path + imagette_name + '.tif', mode='r')
  imagette = tif_file.read_image()

  augmented_imagette_directory_path = directory_path + imagette_name + '/'
  print(augmented_imagette_directory_path)
  if os.path.isdir(augmented_imagette_directory_path):
    if clear_directory:
      #On vide le dossier
      shutil.rmtree(augmented_imagette_directory_path)
      os.mkdir(augmented_imagette_directory_path)
      print('\n----- Ecrasement + Création d\'un nouveau dossier -----\n')
  else:
    try:
      os.mkdir(augmented_imagette_directory_path)
      print('\n----- Création d\'un nouveau dossier -----\n')
    except OSError:
      print('\n----- Erreur dans la création du dossier -----\n')

  datagen = ImageDataGenerator(
    rotation_range=50,
    width_shift_range=0.05,
    height_shift_range=0.05,
    horizontal_flip=True,
    vertical_flip=True,
    shear_range = 0.3,
    zoom_range=0.2,
    fill_mode = "wrap",
    data_format = "channels_first"
   )

  if len(imagette.shape) == 2: #Si image greyscale, il faut ajouter une dimenssion channel
    imagette = imagette[np.newaxis,:]

  if imagette.shape[0] == 1:
    rgb = False
  else:
    rgb = True

  for epoch in range(1,nb_generate + 1):
    for new_imagette, _ in datagen.flow(imagette[np.newaxis,:], y= np.ones((1,))):
      new_imagette = np.array(np.int_(new_imagette[0]), copy =True)
      new_imagette = new_imagette.astype(np.uint8)
      tif_file = TIFF.open(augmented_imagette_directory_path + imagette_name + "_new_" + str(epoch) + ".tif", mode='w')
      print(new_imagette.shape)
      tif_file.write_image(new_imagette,write_rgb=rgb)
      break


if __name__ == "__main__":

  # Data augmentation pour les images couleurs
  for imagette_name in os.listdir(couleur_positif_save_path):
    if imagette_name.endswith(".tif"):
      imagette_name = imagette_name[:-4] #Remove .tif
      generate_imagettes(imagette_name,couleur_positif_save_path,nb_generate = 300)

  # Data augmentation pour les images greyscale
  for imagette_name in os.listdir(greyscale_positif_save_path):
    if imagette_name.endswith(".tif"):
      imagette_name = imagette_name[:-4] #Remove .tif
      generate_imagettes(imagette_name,greyscale_positif_save_path,nb_generate = 300)
