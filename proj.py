import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import os
from os import listdir
from os.path import isfile, join
import re 

def read_data_velo_feu():

    df1=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2014_2016.csv")
    df2=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2017_2019.csv")
    df3=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2020_2022.csv")
    #view different automobiles that were tracked
	#set(df1['Description_Code_Banque'])
    return pd.concat([df1,df2,df3])


velo1=read_data_velo_feu()

def read_data_velo_piste():

	mypath='/home/apkhoury/Documents/projects/DataScience_Project/datasets'
	onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	r = re.compile("comptage[v_].*")
	newlist = list(filter(r.match, onlyfiles))
	dfs=[]
	[dfs.append(pd.read_csv("datasets/"+x))for x in newlist]
    """
	CHANGE DATE FORMAT THROUGH FILES FOR IT TO BE UNIFORM
    """

    #view different automobiles that were tracked
	#set(df1['Description_Code_Banque'])
	return pd.concat(dfs)

velo2=read_data_velo_piste()
