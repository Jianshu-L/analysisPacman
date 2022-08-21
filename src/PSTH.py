import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from src.DataHelper import DataHelper
helper = DataHelper()

class PSTH(object):

    def __init__(self, timewindow, dataframe, stimulus_onset):
        self.timewindow = timewindow
        self.dataframe = dataframe # neural data
        self.stimulus_onset = stimulus_onset

    # def calFR(self, smooth=15):
    #     """calculate mean firing rate for PSTH in timewindow(second)"""
    #     dataframe = self.dataframe
    #     if smooth == 0:
    #         so = self.stimulus_onset
    #     else:
    #         so = self.stimulus_onset.apply(lambda x: range(x-smooth,x+smooth)).explode().reset_index(drop=True)
    #     tw = self.timewindow
    #     pAll = int(tw*60) # convert sec to Step
    #     # find index within StimulusOnset timeWindow
    #     Edge = np.linspace(-tw/2,tw/2,int(tw*60))
    #     Index = so.apply(lambda x: range(x-int(tw/2*60),x+int(tw/2*60))).explode().reset_index()
    #     Index = Index.drop(Index.index[Index['so']>=dataframe.shape[0]])
    #     Index_ = Index.iloc[range(0,np.int(Index.shape[0]/pAll)*pAll)]
    #     # get data by index
    #     df = dataframe.iloc[Index_['so']].reset_index(drop=True)*60
    #     df['pIndex'] = np.tile(range(0,pAll),np.int(Index_.shape[0]/pAll))
    #     # calculate mean firing rate
    #     dfPSTH = df.pivot_table(
    #         index="pIndex",
    #         aggfunc="mean"
    #     )
    #     Error = df.pivot_table(
    #         index="pIndex",
    #         aggfunc="sem"
    #     )
    #     return dfPSTH, Error, Edge

    def _axBgEdgeColor(self, ax, bg='#FFFFFF', edge='#000000'):
        ax.grid(False)
        ax.set_facecolor(bg)
        for spine in ax.spines.values():
            spine.set_color(edge)
            spine.set_linewidth(1)

    def plot(self, ax, xdata, ydata, yerror, lineWidth=8, title=""):
        ax.fill_between(xdata, ydata - yerror, ydata + yerror,
                     color='gray', alpha=0.5)
        ax.plot(xdata, ydata, linewidth=lineWidth)
        self._axBgEdgeColor(ax, bg='#FFFFFF', edge='#000000') # set color
        ylim = ax.get_ylim()
        ax.set_ylim(ylim)
        ax.set_title(title, fontsize=70)
        ax.tick_params(axis="x", labelsize=50)
        ax.tick_params(axis="y", labelsize=50)

    def plotAll(self, title="PSTH", size_muti=13, col_num=5):
        dataFrame = self.dataframe
        timeWindow = self.timewindow
        stimulus_onset = self.stimulus_onset
        [dfPSTH,Std,Edge] = helper.calFR(dataFrame, stimulus_onset, timeWindow, smooth=15)
        Num = dataFrame.columns.values.shape[0]
        cols = math.ceil(Num/col_num)
        fig,axs = plt.subplots(cols, col_num,
            figsize=(col_num*size_muti,cols*size_muti),constrained_layout=True)
        xValue = Edge
        param_dict = {'xlabel': 'Time (sec)', 'ylabel': '# of spikes'}
        x = 0
        y = 0
        for index,chanName in enumerate(dfPSTH.columns.values):
            ax = axs[x,y]
            if y == 0:
                ax.set_ylabel(param_dict['ylabel'], fontsize=60)
            if x == cols-1:
                ax.set_xlabel(param_dict['xlabel'], fontsize=60)
            y += 1
            if (not bool(y % col_num)) and y != 1:
                x = x + 1
                y = 0
            out = self.plot(ax,
                xValue, dfPSTH.iloc[:,index], Std.iloc[:,index], lineWidth=8,
                title=chanName) # plot error as area
            ax.plot(np.zeros(100),range(0,100),'--', color='black', lw='4')
            # ax.set_title(i+' '+RecordFig.BrainArea[index],fontsize=70)
        fig.suptitle(f"{title} %1.1fTiles" % float(timeWindow*60/25/2),fontsize=120)
        return fig
