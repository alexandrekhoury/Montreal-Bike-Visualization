import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import os
from os import listdir
from os.path import isfile, join
import re 
import datetime
from mpl_toolkits.basemap import Basemap

def date_time(day,month,year):
    return datetime.datetime(int(year), int(month), int(day), 0, 0).strftime('%Y-%m-%d')    

#number of bikes at intersections
def read_data_velo_feu():
    df1=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2014_2016.csv")
    df2=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2017_2019.csv")
    df3=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2020_2022.csv")
    #view different automobiles that were tracked
    #set(df1['Description_Code_Banque'])
    return pd.concat([df1,df2,df3]).reset_index()

#number of bikes on cycling paths
def read_data_velo_piste():

    mypath=os.getcwd()+"/datasets"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    r = re.compile("comptage[v_].*")
    newlist = list(filter(r.match, onlyfiles))
    dfs=[]
    [dfs.append(pd.read_csv("datasets/"+x))for x in newlist]
    
    #adjusting month that is in french to regular dataset values
    dfs[8]['Date'][17376:20352]=dfs[8]['Date'][17376:20352].str.extract(r'([0-9]+)(\s\w+\.)(\s2021)(.*)')[[0,2,3]].apply(lambda row : date_time(row[0],7,row[2]), axis = 1)+dfs[8]['Date'][17376:20352].str.extract(r'([0-9]+)(\s\w+\.)(\s2021)(.*)')[3]+":00"
           
    # setting date and time in two different columns for datasets that have them in one column only
    for x in [0,4,6,8]:
        dfs[x]['Time'] = pd.to_datetime(dfs[x]['Date']).dt.time
        dfs[x]['Date'] = pd.to_datetime(dfs[x]['Date']).dt.date
    for y in [1,2,3,5,7]:
        dfs[y]['Date'] = pd.to_datetime(dfs[y]['Date']).dt.date

    #view different automobiles that were tracked
    #set(df1['Description_Code_Banque'])
    df=pd.concat(dfs)
    df.sort_values(by='Date',inplace=True)
    df.reset_index(inplace=True)
    return df

#coordinates of velo piste compteurs
def read_localisation_velos():
    df=pd.read_csv("datasets/localisation_des_compteurs_velo.csv")
    return df

#number of vehicules in montreal
def read_number_vehicles():
    df=pd.read_excel('datasets/tableau.xlsx',skiprows=5,skipfooter=17)
    df= df.set_index("Type d'utilisation").T
    return df

def read_air_quality_station():
    #only 2021 and 2022 data
    df=pd.read_csv("datasets/rsqa-indice-qualite-air-station-historique.csv")
    return df

def read_air_quality_montreal():
    df=pd.read_csv('datasets/montreal-air-quality.csv')
    return df

def read_CO2():
    #2014 to 2018 data
    df=pd.read_csv('datasets/ghg-emissions-transport.csv')
    return df

def get_map_velo():
    #reading datasets
    velo2df=read_data_velo_piste()
    locdf=read_localisation_velos()
    
    """
    =========================================
    Converting columns from velo datafile to localisation datafile
    =========================================
    """
    #getting the columns to be consistent with the names 
    velo2df.columns=velo2df.columns.str.replace("_"," ")
    velo2df.columns=velo2df.columns.str.replace("compteur ","")
    locdf['Nom']=locdf['Nom'].str.replace("_"," ")
    locdf['Nom']=locdf['Nom'].str.replace(" \(@.*\)","")
    
    hardcode=['PierDup','Rachel / Hôtel de Ville','Pont Jacques Cartier','Totem Laurier','Christophe-Colomb','Eco-Totem - Métro Laurier']
    tohard=['Pierre-Dupuy','Rachel / HôteldeVille','Pont Jacques-Cartier','Eco-Display - Métro Laurier','Christophe-Colomb/Louvain','Eco-Display - Métro Laurier']
    
    for y in range(0,len(hardcode)):
        velo2df.rename(columns={hardcode[y]:tohard[y]},inplace=True)
    
    column_ind=[]
    ID_found=[]
    for count,x in enumerate(velo2df.columns):
        if np.sum(locdf['Nom']==x)>0:
            column_ind=np.append(column_ind,count)
            ID_found=np.append(ID_found,locdf['ID'][locdf['Nom']==x])
    
    cvals = velo2df.columns.values
    cvals[list(map(int,column_ind))]=list(map(int,ID_found))
    velo2df.columns=cvals
    
    '''
    =========================================
    Creating the map
    =========================================
    '''
    
    

if __name__ == "__main__":

    velo1df=read_data_velo_feu()
    velo2df=read_data_velo_piste()

    vehicle1df=read_number_vehicles()
    airdf=read_air_quality_montreal()
    
    locdf=read_localisation_velos()
    
    
#%% Cell 1
    
#TEST CELL FOR NOW
    
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import os
from os import listdir
from os.path import isfile, join
import re 
import datetime
from mpl_toolkits.basemap import Basemap


velo2df=read_data_velo_piste()
locdf=read_localisation_velos()

"""
=========================================
Converting columns from velo datafile to localisation datafile
=========================================
"""
#getting the columns to be consistent with the names 
velo2df.columns=velo2df.columns.str.replace("_"," ")
velo2df.columns=velo2df.columns.str.replace("compteur ","")
locdf['Nom']=locdf['Nom'].str.replace("_"," ")
locdf['Nom']=locdf['Nom'].str.replace(" \(@.*\)","")

hardcode=['PierDup','Rachel / Hôtel de Ville','Pont Jacques Cartier','Totem Laurier','Christophe-Colomb','Eco-Totem - Métro Laurier']
tohard=['Pierre-Dupuy','Rachel / HôteldeVille','Pont Jacques-Cartier','Eco-Display - Métro Laurier','Christophe-Colomb/Louvain','Eco-Display - Métro Laurier']

for y in range(0,len(hardcode)):
    velo2df.rename(columns={hardcode[y]:tohard[y]},inplace=True)

column_ind=[]
ID_found=[]
for count,x in enumerate(velo2df.columns):
    if np.sum(locdf['Nom']==x)>0:
        column_ind=np.append(column_ind,count)
        ID_found=np.append(ID_found,locdf['ID'][locdf['Nom']==x])

cvals = velo2df.columns.values
cvals[list(map(int,column_ind))]=list(map(int,ID_found))
velo2df.columns=cvals

'''
=========================================
Creating the map
=========================================
'''

import plotly.express as px
import plotly.io as pio
import plotly.offline as pyo
# Set notebook mode to work in offline
pyo.init_notebook_mode()

token= open("/home/apkhoury/Dropbox/python/tokens/.mapbox_token").read()
px.set_mapbox_access_token(token)
#MATHIAS YOU WILL HAVE TO ASK ME FOR ACCESS TOKEN FOR THIS TO WORK


fig = px.scatter_mapbox(locdf, lat="Latitude", lon="Longitude",
                  size_max=15, zoom=10)
fig.write_image('bike_location.png')
fig.show()
# lat=45.5017
# lon=-73.5673


# fig = plt.figure(figsize=(8, 8))
# m = Basemap(projection='lcc', resolution='c',
#             width=1E6, height=1E6, 
#             lat_0=lat, lon_0=lon,lat_1=lat+2,lon_1=lon+2)
# m.etopo(scale=0.5, alpha=0.5)