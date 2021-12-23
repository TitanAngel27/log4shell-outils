# log4shell-outils
## Installation

1. Installer Python3
2. Installer pip
3. Installer les dépendances via pip

```bash
pip install -r requirements.txt
```
## Utilisation
**softwarelist_parser.py**
```bash
py softwarelist_parser.py csv
```
Description: \
Télécharge la dernière liste publiée puis met le tout en format csv dans le dossier Liste sous le format _list_log4shell_mm-jj_.

**softwarelist_compare.py**
```bash
py softwarelist_compare.py
```
Description: \
Compare la liste du jour et la liste de la journée d'avant, puis créer un fichier texte dans le dossier Resultat sous le format _Resultat_mm-jj_. Pour l'instant les fichiers donnent plus d'informations que nécessaire (À changer et/ou automatiser). Les parties importantes sont : \
-Sample Rows with Unequal Values: Les lignes qui sont différentes (avec ce qui a changé) \
-Sample Rows Only in df2: Les lignes qui ont été ajoutées
