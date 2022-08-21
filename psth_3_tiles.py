#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import sys
from src.DataProvider import DataProvider
from src.DataHelper import DataHelper
from src.PSTH import PSTH
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
helper = DataHelper()


# In[ ]:

if __name__ == "__main__":
    dataPath = sys.argv[1]
    # dataPath="/mnt/d/data/data_2021/combine"
    dataFrame = DataProvider(dataPath, iterNum=2)
    # plot PSTH
    for loops in dataFrame:
        timeWindow = 6*25/60
        df = dataFrame.getChan()
        Name = dataFrame.fileName.replace(".csv","")
        # plot Control PSTH
        so = dataFrame.getTso()
        psth = PSTH(timeWindow, df, so)
        fig = psth.plotAll(title="Control")
        fig.savefig(f"Control_{Name}.png")
        # plot Reward PSTH
        so = dataFrame.getRso()
        psth = PSTH(timeWindow, df, so)
        fig = psth.plotAll(title="Reward")
        fig.savefig(f"Reward_{Name}.png")
        # plot JoyStick PSTH
        so = dataFrame.getJSso()
        psth = PSTH(timeWindow, df, so)
        fig = psth.plotAll(title="JoyStick")
        fig.savefig(f"JoyStick_{Name}.png")
