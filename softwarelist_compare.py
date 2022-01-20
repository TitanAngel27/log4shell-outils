
import pandas as pd
import datacompy
import argparse

from datetime import date

from pandas.core.reshape.merge import merge

current_day = date.today()
mois = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

HEADERS = [
    'Supplier',
    'Product',
    'Version',
    'Status CVE-2021-4104',
    'Status CVE-2021-44228',
    'Status CVE-2021-45046',
    'Status CVE-2021-45105',
    'Notes',
    'Links',
    'Date MAJ'
]

#HEADER sans la date de maj
HEADERS_SD = [
    'Supplier',
    'Product',
    'Version',
    'Status CVE-2021-4104',
    'Status CVE-2021-44228',
    'Status CVE-2021-45046',
    'Status CVE-2021-45105',
    'Notes',
    'Links',
]

parser = argparse.ArgumentParser(description="Comparer 2 liste et sortir les différences. Par default, la liste de hier et d'aujourd'hui")

# Par default: Date de hier et d'aujourd'hui
parser.add_argument("--date_1", help="Le mois et le jour de la 1re liste à comparer. Ex: 4-21 ", default="0-0")
parser.add_argument("--date_2", help="Le mois et le jour de la 2e liste à comparer. Ex: 12-1 ", default="0-0")
#TO-DO
#  -- Mode pour fichier Changement.csv supplémentaire

args = parser.parse_args()

# Chemin des fichiers utilises 
if(args.date_1 == "0-0"):
    if(current_day.day == 1):#Verifier changement de mois
        listeHier = '.\Resultat\list_log4shell_comparaison_'+str(current_day.month-1)+'-'+str(mois[current_day.month-1])+'.csv'
    else:
        listeHier = '.\Resultat\list_log4shell_comparaison_'+str(current_day.month)+'-'+str((current_day.day-1))+'.csv'
else:
    listeHier = '.\Resultat\list_log4shell_comparaison_'+args.date_1+'.csv'

if(args.date_2 == "0-0"):
    listeAjd = '.\Liste\list_log4shell_'+str(current_day.month)+'-'+str((current_day.day))+'.csv' 
else:
    listeAjd = '.\Liste\list_log4shell_'+args.date_2+'.csv'

#Verifie si les fichiers souhaites existes
try: 
    dfHier = pd.read_csv(listeHier, sep=';',header=0,encoding_errors='ignore')
    del dfHier['Unnamed: 0'] #Supprime l'index pour eviter les doublons
    dfHier_NonDate = dfHier[HEADERS_SD].copy()#Supprime la date sinon toute les lignes sont différentes

except (FileNotFoundError):
    print('Le fichier :'+listeHier+ " n'existe pas")
    quit()

try: 
    dfAjd = pd.read_csv(listeAjd, sep=';', header=0)
    dfAjd_NonDate = dfAjd[HEADERS_SD].copy()#Supprime la date sinon toute les lignes sont différentes
except (FileNotFoundError):
    print('Le fichier :'+listeAjd+ " n'existe pas")
    quit()

#Comparer les 2 fichiers
compare = datacompy.Compare(dfHier_NonDate, dfAjd_NonDate, join_columns=['Supplier','Product'])

df_mismatch = compare.all_mismatch()

# Supprime les colonnes avec les informations pas à jour
del df_mismatch['version_df1']
del df_mismatch['status cve-2021-4104_df1']
del df_mismatch['status cve-2021-44228_df1']
del df_mismatch['status cve-2021-45046_df1']
del df_mismatch['status cve-2021-45105_df1']
del df_mismatch['notes_df1']
del df_mismatch['links_df1']

# Renomme les colonnes pour éviter les erreurs lors de la fusion
df_mismatch.rename(columns={'supplier': HEADERS[0],
                    'product': HEADERS[1],
                    'version_df2': HEADERS[2],
                    'status cve-2021-4104_df2': HEADERS[3],
                    'status cve-2021-44228_df2': HEADERS[4],
                    'status cve-2021-45046_df2': HEADERS[5],
                    'status cve-2021-45105_df2': HEADERS[6],
                    'notes_df2':HEADERS[7],
                    'links_df2':HEADERS[8]},inplace = True)

# Sort la liste lignes qui on ete modifiees
listeMismatch = df_mismatch.index.values.tolist()

# Les lignes qui on ete ajoute
df_rightOnly = compare.df2_unq_rows

# Renomme les colonnes pour éviter les erreurs lors de la fusion
df_rightOnly.rename(columns={'supplier': HEADERS[0],
                    'product': HEADERS[1],
                    'version': HEADERS[2],
                    'status cve-2021-4104': HEADERS[3],
                    'status cve-2021-44228': HEADERS[4],
                    'status cve-2021-45046': HEADERS[5],
                    'status cve-2021-45105': HEADERS[6],
                    'notes':HEADERS[7],
                    'links':HEADERS[8]},inplace = True)

# Fusion des lignes modifies et ajoutes
df_resultAjout = pd.concat([df_mismatch,df_rightOnly])

# Date de modification
if(args.date_2 == "0-0"):
    date2Jour = current_day
else:
    date2Jour = args.date_2

# Ajout de la colonne Date Maj avec la date de modification
listeDate = []
for x in range(len(df_resultAjout.index)):
    listeDate.append(date2Jour)
df_resultAjout['Date MAJ'] = listeDate

# Supprimer les lignes qui ne sont plus a jour
dfHier.drop(listeMismatch,inplace = True)

# Fusion de la liste avec les lignes non modifiees et la liste avec les lignes modifiees/ajoutees
df_Resultat = pd.concat([dfHier, df_resultAjout])

# Nom du fichier de comparaison
if(args.date_2 == "0-0"):
    nomFichierResultat = '.\Resultat\list_log4shell_comparaison_'+str(current_day.month)+'-'+str(current_day.day)+'.csv'
else:
    nomFichierResultat = '.\Resultat\list_log4shell_comparaison_'+args.date_2+'.csv'

# Creation du CSV 
df_Resultat.to_csv(
    nomFichierResultat,
    sep=';',
    index=True,
    encoding='UTF-8',
)

'''
#---------------------Rapport Écrit de base-----------------
with open('.\Resultat\Resultat_Comparaison_'+str(current_day.month)+'-'+str((current_day.day))+'.txt','w+', encoding='UTF-8') as txtresultat:
    txtresultat.write(compare.report(sample_count=100, column_count=100))
'''