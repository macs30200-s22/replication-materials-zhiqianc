from statsmodels.tsa.stattools import kpss
import pandas as pd
import matplotlib as plt



def plot_by_column(file_path):
    df = pd.read_csv(file_path,index_col=0)
    columns = df.columns
    df.index = df.index.astype(str)
    
    for column in columns:
        plt.plot(data[i])
        plt.title(i)
        plt.xlabel('year')
        plt.ylabel(i)
        plt.xticks(rotation= 70)
        plt.savefig('README_files/{}_by_year.png'.format(column))
        plt.show();
    
    
def kpss_test(series, **kw):    
    statistic, p_value, n_lags, critical_values = kpss(series, **kw)
    # Format Output
    print(f'KPSS Statistic: {statistic}')
    print(f'p-value: {p_value}')
    print(f'num lags: {n_lags}')
    print('Critial Values:')
    for key, value in critical_values.items():
        print(f'   {key} : {value}')
    print(f'Result: The series is {"not " if p_value < 0.01 else ""}stationary')

    
def differencing(series,order):
    while order != 0:
        series = series.diff()
        order -= 1
    return series