from datetime import datetime
import numpy as np
import pandas as pd

class DataHelper(object):
    """some helper functions for data"""
    def __init__(self):
        return None

    def loadCSV(self, dataPath, fileName):
        """load csv"""
        print("load "+fileName)
        df = pd.read_csv(f"{dataPath}/{fileName}").drop('Unnamed: 0',axis=1)
        return df

    def TtoS(self, Tile):
        """Tile to Seconds"""
        Seconds = Tile*25/60
        return Seconds

    def StoT(self, Seconds):
        """Seconds to Tile"""
        Tiles = Seconds*25/60
        return Tiles

    def getDate(self, fileName):
        """ get '20-Nov-2020' from fileName 'omegaL-20-Nov-2020-pFlip.csv' """
        Date = "-".join(fileName.split("-")[1:4])
        return Date

    def DDtoDS(self, Date):
        """ 20201120 to '20-Nov-2020' """
        date_time = datetime.strptime(str(Date), '%Y%m%d').strftime('%d-%b-%Y')
        return date_time

    def DStoDD(self, Date):
        """ '20-Nov-2020' to 20201120 """
        date_time = int(datetime.strptime(str(Date), '%d-%b-%Y').strftime('%Y%m%d'))
        return date_time

    def getChanNum(self, units):
        """read channal numbers from units like Ch100_4"""
        chanNum = int(units.split("_")[0][2:])
        return chanNum

    def calFR(self, dataframe, stimulus_onset, time_window, smooth=15):
        """calculate mean firing rate around stimulus_onset"""
        if smooth == 0:
            so = stimulus_onset
        else:
            so = stimulus_onset.apply(lambda x: range(x-smooth,x+smooth)).explode().reset_index(drop=True)
        tw = time_window
        pAll = int(tw*60) # convert sec to Step
        # find index within StimulusOnset timeWindow
        Edge = np.linspace(-tw/2,tw/2,int(tw*60))
        Index = so.apply(lambda x: range(x-int(tw/2*60),x+int(tw/2*60))).explode().reset_index()
        Index = Index.drop(Index.index[Index['so']>=dataframe.shape[0]])
        Index_ = Index.iloc[range(0,np.int(Index.shape[0]/pAll)*pAll)]
        # get data by index
        df = dataframe.iloc[Index_['so']].reset_index(drop=True)*60
        df['pIndex'] = np.tile(range(0,pAll),np.int(Index_.shape[0]/pAll))
        # calculate mean firing rate
        dfPSTH = df.pivot_table(
            index="pIndex",
            aggfunc="mean"
        )
        Error = df.pivot_table(
            index="pIndex",
            aggfunc="sem"
        )
        return dfPSTH, Error, Edge
