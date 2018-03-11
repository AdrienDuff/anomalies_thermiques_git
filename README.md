# anomalies_thermiques_git
Projet de fin d'étude à l'INSA de Rouen : Détection automatique de puits de marnières.
En collaboration avec le CEREMA sous la tutelle de C. le Guyader et Raphaël Antoine.

## Install Depedencies
Le projet est entièrement codé en python 3. Utiliser pip3 de préférence pour installer les dépendances.
Liste des paquets à installer :
- numpy
- tifffile et libtiff
- tensorflow et keras
- pickle
- matplotlib
- sklearn
- skimage
- scipy


## Les données
Le dossier DATA_MARNIERES contient les données brutes.
Le dossier data contient les données travaillées.
Les dossiers suivants doivent être remplis avec les données adéquates (pour plus de détails : contacter dufraux.adrien@gmail.com)
- DATA_MARNIERES/DAT_marnieres_epreville_270799_jour/27_07_99/jour/calibre/TIF
- DATA_MARNIERES/DAT_marnieres_epreville_280799/28_07_99/jour/calibre/TIF


## Les 3 jupyter notebook
- Le notebook "Visualisation" contient le code permettant de générer les visuels avec les algorithmes ACP et T-SNE.
- Le notebook "test_basiques_modeles" contient le code qui teste les méthodes autre que CNN.
- Le notebook "classification_image" contient le code qui permet de tester les 3 méthodes avec les modèles CNN.
