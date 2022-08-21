import numpy as np
import pandas as pd
import os
from datetime import date, datetime
from src.DataHelper import DataHelper
helper = DataHelper()

class DataProvider(object):
    """find data files in datapath and load data, and have some get function to get useful information"""

    def __init__(self, dataPath="data/Omega", iterNum=-1):
        self.dataPath = dataPath
        self.fileNames = np.array(os.listdir(dataPath))
        self._index = 0
        if iterNum < 0:
            self.iterNum = len(self.fileNames)
        else:
            self.iterNum = iterNum

    def __iter__(self):
        """make object iterable"""
        return self

    def __next__(self):
        return self.next()

    def shuffle(self):
        """Randomly shuffles order of fileNames."""
        rng = np.random.RandomState()
        new_order = rng.permutation(len(self.fileNames))
        self.fileNames = self.fileNames[new_order]
        self.reset()

    def next(self):
        """load csv file from all files in dataPath."""
        if self._index + 1 > self.iterNum:
            self.reset()
            raise StopIteration()
        self.fileName = self.fileNames[self._index]
        df = self._loadCSV(self.fileName)
        self.df = df
        self._index += 1

    def _loadCSV(self, fileName):
        """load csv"""
        print("load "+fileName)
        df = pd.read_csv(f"{self.dataPath}/{fileName}").drop('Unnamed: 0',axis=1)
        if 'Index' not in df.columns:
            df['Index'] = df.index
        return df

    def reset(self):
         """Resets the provider to the initial state to use."""
         self._index = 0

    def subset_by_round(self,round=1):
        """subset one round data"""
        print(f"subset round {round} data")
        df = self.df.loc[self.df.DayTrial.str.startswith(f"{round}-")].reset_index(drop=True)
        df["Index_"] = df.Index
        df["Index"] = df.index
        self.df = df

    def reset_subset(self):
        self.df = self.loadCSV(self.fileName)

    def getChan(self):
        """get spikes for every channel"""
        df = self.df
        chanData = df.iloc[:,np.where(df.columns.str.contains('Ch'))[0]].fillna(0) # all channels firing rate
        return chanData

    def getChanNum(self):
        """get channal numbers"""
        Units = self.getChan().columns.values
        chanNum, counts = np.unique([int(unit.split("_")[0][2:]) for unit in Units], return_counts=True)
        return chanNum
    
    def getChanCount(self):
        """get the number of every channal"""
        Units = self.getChan().columns.values
        chanNum, counts = np.unique([int(unit.split("_")[0][2:]) for unit in Units], return_counts=True)
        return dict(zip(chanNum,counts))

    def getJSso(self):
        """get Joystick StimulusOnset"""
        df = self.df
        dfJS = df.dropna(subset = ['JoyStick']).reset_index(drop=True)
        index = dfJS.Index[np.where((
            dfJS.Step[1:-1].to_numpy()-dfJS.Step[0:-2].to_numpy()) != 1)[0]+1].to_numpy()
        StimulusOnset = pd.DataFrame(index,columns=["so"])['so'] # JoyStick event timestamp
        return StimulusOnset

    def getRso(self):
        """get Reward StimulusOnset"""
        df = self.df
        StimulusOnset = pd.DataFrame(np.where(
            df['waterStatus'] == 1)[0],columns=["so"])['so'] # reward event timestamp
        return StimulusOnset

    def getTso(self):
        """get every tile StimulusOnset"""
        df = self.df
        dfTile = df.iloc[list(range(0,df.shape[0],25)),:].reset_index()
        StimulusOnset = dfTile['index'].rename("so") # tiles
        return StimulusOnset

    def getDate(self):
        """ get '20-Nov-2020' from fileName 'omegaL-20-Nov-2020-pFlip.csv' """
        fileName = self.fileName
        Date = helper.getDate(fileName)
        return Date

    def getDepth(self, Records):
        """get units depth from Records"""
        chanNum_i = self.getChanNum()
        date_i = helper.DStoDD(self.getDate())
        index = (Records.Date == date_i) & [Records.chanNum[i] in chanNum_i for i in Records.index]
        valid_depth = Records.loc[index,:].reset_index(drop=True)
        return valid_depth
