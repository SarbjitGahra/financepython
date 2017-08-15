DEBUG=True
import matplotlib.pyplot as plt
import datetime
from matplotlib.finance import date2num
import numpy
from matplotlib import style
import bs4 as bs
import requests
import pickle
import os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

def sp_500():
    page = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(page.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers= []
    for row in table.findAll('tr')[1:]:
        ticker=row.findAll('td')[0].text
        tickers.append(ticker)

    #print (tickers)
    with open("sp_500.pickle", "wb") as f:
        pickle.dump(tickers,f)
    return tickers

def get_data_from_yahoo(reload_sp_500=False):
    if reload_sp_500:
        tickers = sp_500()
    else:
        with open("sp_500.pickle", "rb")as f:
            tickers = pickle.load(f)

    if not os.path.exists('stocks_csv'):
        os.makedirs('stocks_csv')
    start = dt.datetime(2010,1,1)
    end   = dt.datetime(2017,8,7 )

    for ticker in tickers[490:]:
        print (ticker)
        if not os.path.exists("stocks_csv/{}.csv".format(ticker)):
            df =web.DataReader(ticker.replace('.','-') ,'yahoo' , start , end)
            df.to_csv("stocks_csv/{}.csv".format(ticker))
        else:
            print ("Already have {}".format(ticker) )
# get_data_from_yahoo()

def compile_data():
    #for count, ticker in enumerate(tickers):
    path ="/Users/sarbjitgahra/python_scripts/stocks_csv/"
    main_df =pd.DataFrame()
    for file in os.listdir("/Users/sarbjitgahra/python_scripts/stocks_csv/"):
        #if DEBUG:
            #print (path+"{}".format(file))
        df = pd.read_csv(path+"{}".format(file))
        ticks=file.partition('.')
        df.set_index('Date', inplace=True)
        df.rename(columns={'Adj Close' :ticks[0]}, inplace=True)
        df.drop(['Open', 'High' , 'Low' , 'Close', 'Volume'], 1,inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
    main_df.to_csv("sp_500_joined.csv")
compile_data()
def plot_data():
    df=pd.read_csv("sp_500_joined.csv")
    tickers = df.dtypes.index
    df.fillna(0,inplace=True)
    val=[]
    for i in df['Date'][1800:]:
        val.append(date2num(datetime.datetime.strptime(i, '%Y-%m-%d')))
    y=numpy.array(df[tickers[-1]][1800:])
    x=numpy.array(val)
    plt.plot(x,y)
    plt.show()


plot_data()
