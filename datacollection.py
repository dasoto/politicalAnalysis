# -*- coding: utf-8 -*-
# all the imports
from __future__ import print_function
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
import sys
import json


def myFunc(x):
    if x=='Yes':
        return 1
    elif x=='No':
        return 0
    else:
        return 0.5

class generateJson:
    def __init__(self, numClusters, chamber):
        self.numClusters = int(numClusters)
        self.chamber = int(chamber)
        #print('Constructing...', file=sys.stderr)
    def gJSON(self):
        #print('Chamber = : {}'.format(self.chamber),file=sys.stderr)
        if self.chamber == 1: #senate
            #print('Loading Files Senate...', file=sys.stderr)
            dfSenate = pd.read_csv('./static/data/dfSenate.csv')
            dfSenateVotes = pd.read_csv('./static/data/dfSenateVotes.csv')
            dfVotes = pd.read_csv('./static/data/dfVotes.csv')
            infoCandidates = pd.read_csv('./static/data/infoCandidatesS.csv')

            #print('Generating JSON',file=sys.stderr)
            ### We create a pivot table to use each vote for each roll as a input feature
            mydata = dfVotes.pivot(index = 'member_id', columns = 'roll_call', values = 'vote_position')
            mydata = mydata.applymap(lambda x: myFunc(x))
            kmeans_model = KMeans(n_clusters=self.numClusters, random_state=1).fit(mydata)
            labels = kmeans_model.labels_
            newDFS = pd.DataFrame({'id':mydata.index.values,'class_k':labels})
            classified5 = pd.merge(dfSenate, newDFS, on='id', how='inner')

            dfSenateFollowers = pd.merge(classified5, infoCandidates, \
                                 left_on='twitter_account', right_on='Candidato', \
                                 how='inner')
            briefSenate = dfSenateFollowers[['first_name','last_name','party',\
                'class_k','followers']]
            briefSenate['full_name'] = briefSenate['first_name'] + \
                ' '+ briefSenate['last_name']
            groupedT = briefSenate[['class_k','full_name','followers','party']]
            groupedT = groupedT.rename(columns={'full_name': 'name', \
                'followers': 'size', 'party':'color'})
            j = (groupedT.groupby(['class_k'], as_index=False)
                .apply(lambda x: x[['name','size','color']].to_dict('r'))
                .reset_index()
                .rename(columns={0:'children','index':'name'})
                .to_json(orient='records'))
            json_new = '{"name":"flare","children":' + j + '}'
            #print(json_new,file=sys.stderr)
            fileToWrite = './static/data/new' + str(self.chamber) +str(self.numClusters)\
                + '.json'
            with open(fileToWrite, 'w') as outfile:
                outfile.write(json_new)
        if self.chamber == 2: #HoR
            #print('Loading Files... HoR', file=sys.stderr)
            dfHouse = pd.read_csv('./static/data/dfHouse.csv')
            dfHoRVotes = pd.read_csv('./static/data/dfHoRVotes.csv')
            dfVotesH = pd.read_csv('./static/data/dfVotesH.csv')
            infoCandidatesH = pd.read_csv('./static/data/infoCandidatesH.csv')
            infoCandidatesH = infoCandidatesH[~infoCandidatesH.Candidato.isnull()]

            #print('Generating JSON',file=sys.stderr)
            ### We create a pivot table to use each vote for each roll as a input feature
            mydata = dfVotesH.pivot(index = 'member_id', columns = 'roll_call', values = 'vote_position')
            mydata = mydata.applymap(lambda x: myFunc(x))
            kmeans_model = KMeans(n_clusters=self.numClusters, random_state=1).fit(mydata)
            labels = kmeans_model.labels_
            newDFS = pd.DataFrame({'id':mydata.index.values,'class_k':labels})
            classifiedH = pd.merge(dfHouse, newDFS, on='id', how='inner')

            dfHouseFollowers = pd.merge(classifiedH, infoCandidatesH, \
                                 left_on='twitter_account', right_on='Candidato', \
                                 how='inner')
            briefHouse = dfHouseFollowers[['first_name','last_name','party',\
                'class_k','followers']]
            briefHouse['full_name'] = briefHouse['first_name'] + \
                ' '+ briefHouse['last_name']
            groupedT = briefHouse[['class_k','full_name','followers','party']]
            groupedT = groupedT.rename(columns={'full_name': 'name', \
                'followers': 'size', 'party':'color'})
            j = (groupedT.groupby(['class_k'], as_index=False)
                .apply(lambda x: x[['name','size','color']].to_dict('r'))
                .reset_index()
                .rename(columns={0:'children','index':'name'})
                .to_json(orient='records'))
            json_new = '{"name":"flare","children":' + j + '}'
            #print(json_new,file=sys.stderr)
            fileToWrite = './static/data/new' + str(self.chamber) +str(self.numClusters)\
                + '.json'
            with open(fileToWrite, 'w') as outfile:
                outfile.write(json_new)
