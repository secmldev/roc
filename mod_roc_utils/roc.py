import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_roc(data, period):
    """
    Rate of change indicator 
    This method create roc values
    Parameters
    -------------
    Input: 
    - Data frame with price column
    - period
    return: Data frame with price, diff, ROC of n period
    """
    roc_data = pd.DataFrame(index=data.index)
    roc_data['price'] = data['price']
    roc_data['roc' + str(period)] = roc_data['price'].diff(periods=period) / roc_data['price'].shift(periods=period)
    return roc_data


def get_roc_signal(data, period, buy_threshold, sell_threshold):
    """
    Get ROC signals
    Input: data frame with price, ROC values for given period 
    Ouput: price, buy sell signals
    """
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['price']
    signals['buy']= 0.0
    signals['sell']= 0.0
    signals['buy'] = np.where(data['roc' + str(period)] < buy_threshold, -1.0, 0.0)
    signals['sell'] = np.where(data['roc' + str(period)] > sell_threshold, 1.0, 0.0)
    signals['buy'] = signals['buy'].diff()
    signals['sell'] = signals['sell'].diff()
    signals.loc[signals['buy']==-1.0,['buy']] = 0.0 
    signals.loc[signals['sell']== 1.0,['sell']] = 0.0 
    signals['buy_sell'] = signals['buy'] + signals['sell']
    return signals[['price', 'buy_sell']]

def plot_roc_buy_sell(data, signals, period):
    graph = plt.figure(figsize = (15,15))
    sp1 = graph.add_subplot(311)
    sp2 = graph.add_subplot(312)
    sp3 = graph.add_subplot(312)
    data["roc" + str(period)].plot(ax=sp1,title = "ROC Plot",color = "r", linewidth = 0.5)
    sp1.axhline(y= 0.1, color = "b", lw = 7.)
    sp1.axhline(y= -0.1, color = "g", lw = 7.)
    sp1.axhline(y= 0, color = "k", lw = 5.)

    signals["price"].plot(ax = sp3)
    sp3.plot(signals.loc[signals.buy_sell == 1].index, signals.price[signals.buy_sell == 1], "^", markersize = 12, color = "k")
    sp3.plot(signals.loc[signals.buy_sell ==-1].index, signals.price[signals.buy_sell ==-1], "v", markersize = 12, color = "m")
    plt.show() 