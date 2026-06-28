# Python LSB Steganography CLI

Un outil en ligne de commande (CLI) permettant de dissimuler des messages secrets à l'intérieur d'images numériques sans en altérer l'apparence visuelle, en utilisant la technique du Least Significant Bit (LSB).

## Comment ça marche ? (La technique LSB)
Le script modifie le tout dernier bit binaire (Bit de Poids Faible) du canal rouge des pixels de l'image pour y insérer les bits du message secret. Cette modification mathématique est quasiment imperceptible pour l'œil humain, laissant l'image extrêmement proche visuellement de l'originale.

## Prérequis

Assurez-vous d'avoir Python 3 installé, ainsi que la bibliothèque de traitement d'image Pillow.

```bash
pip install Pillow
```

## Utilisation

L'outil dispose de deux commandes principales : hide (cacher) et extract (lire).

### Cacher un message secret

Utilisez une image au format PNG (le format JPG compresse l'image et détruirait le message secret).

```bash
python stegano.py hide image_originale.png "Votre message ultra secret" image_secrete.png
```
### Extraire un message secret

```bash
python stegano.py extract image_secrete.png
```

## Limitations connues

Fonctionne uniquement avec des formats d'image sans perte (PNG, BMP). Ne pas utiliser de JPEG.
La longueur du message est limitée par le nombre de pixels de l'image (1 pixel = 1 bit de message).