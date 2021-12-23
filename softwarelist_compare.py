import pandas as pd
import datacompy

from datetime import date

from pandas.core.reshape.merge import merge

current_day = date.today()
mois = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

#---------To-DO --------
#  changer l'adresse pour l'emplacement des fichiers
if(current_day.day == 1):
    listeHier = '.\Liste\list_log4shell_'+str(current_day.month-1)+'-'+str(mois[current_day.month-1])+'.csv'
else:
    listeHier = '.\Liste\list_log4shell_'+str(current_day.month)+'-'+str((current_day.day-1))+'.csv'

listeAjd = '.\Liste\list_log4shell_'+str(current_day.month)+'-'+str((current_day.day))+'.csv'

dfHier = pd.read_csv(listeHier, sep=';',header=0)
dfAjd = pd.read_csv(listeAjd, sep=';', header=0 )

compare = datacompy.Compare(dfHier, dfAjd, join_columns=['Supplier','Product'])

with open('.\Resultat\Resultat_Comparaison_'+str(current_day.month)+'-'+str((current_day.day))+'.txt','w+', encoding='UTF-8') as txtresultat:
    txtresultat.write(compare.report(sample_count=100, column_count=100))

'''
#for ligne in dfAjd:
comp = dfHier.isin(dfAjd)
print (comp)

dfMerge = pd.merge(dfHier, dfAjd, how='inner', left_index=True, right_index=True)


print(dfHier)
print('------------------------------------------------')
print(dfAjd)

with open('.\merge.csv', 'w+', encoding='UTF-8', newline='') as csvfile:
    dfMerge.to_csv(csvfile, sep=';',header=True)
'''    