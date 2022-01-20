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
py softwarelist_parser.py
```
Description: \
Télécharge les 27 dernières listes publiées puis met le tout en format csv dans le dossier Liste sous le format _list_log4shell_mm-jj_. \
À chaque fois que l'on utilise la commande, on laisse une trace dans le fichier _liste.txt_.

**softwarelist_compare.py**
```bash
py softwarelist_compare.py #Par default, on va comparer la date de hier et d'aujourd'hui
py softwarelist_compare.py --date_1 1-10 --date_2 1-11 #Si on compare le 10 et le 11 janvier
```
Description: \
Compare la liste du jour et la comparaison de la journée d'avant, puis créer un fichier texte dans le dossier Resultat sous le format _Resultat_mm-jj_ avec la 2e date (mm-jj) utilisé lors de la comparaison.
