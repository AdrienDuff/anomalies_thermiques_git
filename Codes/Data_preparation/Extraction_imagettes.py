
import tifffile as tiff
import numpy as np


# ------- y
# |
# |
# |
#\ /
# x

couleur_positif_save_path = "../../Data/Melange_imagettes_jour/Couleur/Positif/"
couleur_negatif_save_path = "../../Data/Melange_imagettes_jour/Couleur/Negatif/"
greyscale_positif_save_path = "../../Data/Melange_imagettes_jour/Greyscale/Positif/"
greyscale_negatif_save_path = "../../Data/Melange_imagettes_jour/Greyscale/Negatif/"

from_greyscale_positif_save_path = "../../Data/Melange_imagettes_jour/From_Greyscale/Positif/"
from_greyscale_negatif_save_path = "../../Data/Melange_imagettes_jour/From_Greyscale/Negatif/"

SIZE_IMAGETTE = 31
RAYON_IMAGETTE = int(SIZE_IMAGETTE/2)

def weightedAverage(pixel):
    return 0.299*pixel[0] + 0.587*pixel[1] + 0.114*pixel[2]

def RGBToGreyscale(image):
  grey_image = np.zeros((image.shape[1], image.shape[2]), dtype = np.uint8) # init 2D numpy array
  # get row number
  for rownum in range(image.shape[1]):
     for colnum in range(image.shape[2]):
        grey_image[rownum,colnum] = int(weightedAverage(image[:,rownum,colnum]))
  grey_image = grey_image[np.newaxis,:]
  return grey_image

def extract_imagettes(big_image_path,size_imagette,tab_coords,name_images,classe,couleur = True, from_greyscale = False):
  bigImage = tiff.imread(big_image_path) # <class 'numpy.ndarray'>, (channel,x,y)
  if from_greyscale:
    bigImage = bigImage[-16000:,:]
  print(bigImage.shape)
  if classe == "Positif" and couleur == True:
    save_path_begin = couleur_positif_save_path
  if classe == "Negatif" and couleur == True:
    save_path_begin = couleur_negatif_save_path
  if classe == "Positif" and couleur == False:
    save_path_begin = greyscale_positif_save_path
  if classe == "Negatif" and couleur == False:
    save_path_begin = greyscale_negatif_save_path

  if from_greyscale:
    if classe == "Positif":
      save_path_begin = from_greyscale_positif_save_path
    else:
      save_path_begin = from_greyscale_negatif_save_path

  for xCoord,yCoord,id_place in tab_coords:
    if from_greyscale:
      imagette = bigImage[xCoord-RAYON_IMAGETTE : xCoord+RAYON_IMAGETTE+1, yCoord-RAYON_IMAGETTE : yCoord+RAYON_IMAGETTE+1]
    else:
      imagette = bigImage[:, xCoord-RAYON_IMAGETTE : xCoord+RAYON_IMAGETTE+1, yCoord-RAYON_IMAGETTE : yCoord+RAYON_IMAGETTE+1]
    save_path = save_path_begin + str(id_place) + "_" + name_images + "_" + str(xCoord) + "_" + str(yCoord) + ".tif"

    if couleur == False and from_greyscale == False:
      imagette = RGBToGreyscale(imagette)

    print(save_path)
    tiff.imsave(save_path, imagette)

def extract_imagettes_random(big_image_path,size_imagette,name_images, classe, first_id_place, nb_imagettes_per_axe, couleur = "both"):
  bigImage = tiff.imread(big_image_path) # <class 'numpy.ndarray'>, (channel,x,y)

  tab_coords = []
  x_min = size_imagette
  x_max = bigImage.shape[1] - size_imagette
  y_min = size_imagette
  y_max = bigImage.shape[2] - size_imagette
  id_place = first_id_place
  for _ in range(nb_imagettes_per_axe):
    coordX = np.random.randint(low = x_min, high=x_max)
    coordY = np.random.randint(low = y_min, high=y_max)
    tab_coords.append((coordX,coordY,id_place))
    id_place += 1

  for xCoord,yCoord,id_place in tab_coords:
    imagette = bigImage[:, xCoord-RAYON_IMAGETTE : xCoord+RAYON_IMAGETTE+1, yCoord-RAYON_IMAGETTE : yCoord+RAYON_IMAGETTE+1]

    if couleur != "both":
      if classe == "Positif" and couleur == True:
        save_path = couleur_positif_save_path
      if classe == "Negatif" and couleur == True:
        save_path = couleur_negatif_save_path
      if classe == "Positif" and couleur == False:
        save_path = greyscale_positif_save_path
      if classe == "Negatif" and couleur == False:
        save_path = greyscale_negatif_save_path

      save_path = save_path + str(id_place) + "_" + name_images + "_" + str(xCoord) + "_" + str(yCoord) + ".tif"

      if couleur == False :
        imagette = RGBToGreyscale(imagette)

      tiff.imsave(save_path, imagette)
    else:
      if classe == "Positif":
        save_path_grey = greyscale_positif_save_path
        save_path_col = couleur_positif_save_path
      if classe == "Negatif":
        save_path_grey = greyscale_negatif_save_path
        save_path_col = couleur_negatif_save_path

      save_path_grey = save_path_grey + str(id_place) + "_" + name_images + ".tif"
      save_path_col = save_path_col + str(id_place) + "_" + name_images + ".tif"

      imagette_greyscale = RGBToGreyscale(imagette)
      print(imagette_greyscale.shape)
      print(imagette.shape)
      tiff.imsave(save_path_grey, imagette_greyscale)
      tiff.imsave(save_path_col, imagette)


def extract_positif_imagettes():
  #Axe 3 16h54_24 & 11h18_24
  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe3_16h54_24_C.tif"
  name_images = "Axe3_16h54_24_C"
  tab_coords = [(7669,812,1),(7944,1065,2),(14355,529,3)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = True)
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False)

  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_280799/28_07_99/jour/calibre/TIF/Axe3_11h18_24_C.tif"
  name_images = "Axe3_11h18_24_C"
  tab_coords = [(9194,1058,1),(9380,1363,2),(15747,1128,3)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = True)
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False)

  #Axe 1   17h24_37  & 16h40_37
  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe1_17h24_37_C.tif"
  name_images = "Axe1_17h24_37_C"
  tab_coords = [(10966,537,4)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = True)
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False)

  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe1_16h40_24_C.tif"
  name_images = "Axe1_16h40_24_C"
  tab_coords = [(4388,332,4),(13350,1395,5)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = True)
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False)

#We will choose random places for the negatif class. Remove the wrong one.
def extract_negatif_imagettes(nb_imagettes_per_axe = 23):
  axe_paths = ["../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe1_16h40_24_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe1_17h24_37_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe2_16h47_24_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe3_16h54_24_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe3_17h00_24_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe3_17h30_37_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe3_17h40_14_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe4_17h12_24_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF/Axe4_17h46_14_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_280799/28_07_99/jour/calibre/TIF/Axe2_11h10_24_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_280799/28_07_99/jour/calibre/TIF/Axe3_11h18_24_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_280799/28_07_99/jour/calibre/TIF/Axe3_11h26_37_C.tif",
               "../../DATA_MARNIERES/DAT_marnieres_epreville_280799/28_07_99/jour/calibre/TIF/Axe3_11h35_14_C.tif"]
  first_id_place = 1
  for big_image_path in axe_paths:
    print(big_image_path)
    name_images = "neg"
    classe = "Negatif"
    extract_imagettes_random(big_image_path,SIZE_IMAGETTE,name_images, classe, first_id_place, nb_imagettes_per_axe, couleur = "both")
    first_id_place += nb_imagettes_per_axe


def extract_positif_imagettes_from_greyscale():
  #Axe 3 16h54_24 & 11h18_24
  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/Greyscale/Axe3_16h54_24_NC.tif"
  name_images = "Axe3_16h54_24_NC"
  tab_coords = [(7669,812,1),(7944,1065,2),(14355,529,3)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False, from_greyscale = True)

  """
  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_280799/28_07_99/jour/calibre/TIF/Axe3_11h18_24_C.tif"
  name_images = "Axe3_11h18_24_C"
  tab_coords = [(9194,1058,1),(9380,1363,2),(15747,1128,3)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = True)
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False)
  """

  #Axe 1   17h24_37  & 16h40_37
  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/Greyscale/Axe1_17h24_37_NC.tif"
  name_images = "Axe1_17h24_37_NC"
  tab_coords = [(10966,537,4)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False, from_greyscale = True)

  big_image_path = "../../DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/Greyscale/Axe1_16h40_24_NC.tif"
  name_images = "Axe1_16h40_24_NC"
  tab_coords = [(4388,332,4),(13350,1395,5)]
  classe = "Positif"
  extract_imagettes(big_image_path,SIZE_IMAGETTE,tab_coords,name_images,classe,couleur = False, from_greyscale = True)




if __name__ == "__main__":
  extract_positif_imagettes()
  extract_negatif_imagettes(nb_imagettes_per_axe = 210)
  #extract_positif_imagettes_from_greyscale()


