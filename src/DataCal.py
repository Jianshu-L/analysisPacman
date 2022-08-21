import numpy as np
import pandas as pd
from src.DataProvider import DataProvider
from src.DataHelper import DataHelper
helper = DataHelper()

class DataCal(object):
    """find data files in datapath and load data."""

    def __init__(self, dataPath="data/Data", iterNum=-1):
        self.dataframe = DataProvider(dataPath, iterNum)

    def getEventFr(self, stimulus_type, time_window=6*25/60):
        """get the timing of neuron firings in response to a stimulus event."""
        if stimulus_type == 'reward':
            stimulus_onset = self.dataframe.getRso()
        elif stimulus_type == 'joystick':
            stimulus_onset = self.dataframe.getJSso()
        elif stimulus_onset == 'tile':
            stimulus_onset = self.dataframe.getTso()
        dataframe = self.dataframe.getChan()
        results = helper.calFR(dataframe, stimulus_onset, time_window)
        return results

    def rename(self, dataframe):
        """change dataframe columns name from Ch100_4 to Ch100_4_20201130."""
        df_i = dataframe
        for colName in df_i.columns.tolist():
            Date = helper.DStoDD(self.dataframe.getDate())
            df_i.rename(columns={colName: colName + "_" + str(Date)}, inplace=True)
        return df_i
