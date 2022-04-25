from statsmodels.tsa.stattools import adfuller
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
    
    
    
def adf_test(series):
    series.dropna(inplace=True)
    test_res = adfuller(series)
    t_statistic = test_res[0]
    p_value = test_res[1]
    critical_val_dict = test_res[4]
    
    print(f'ADF Statistic: {t_statistic}')
    print(f'p-value: {p_value}')
    for key, value in critical_val_dict.items():
        print('Critial Values:')
        print(f'   {key}, {value}')
        
    print('Test conclusion:')
    if t_statistic < critical_val_dict['1%']:
        print('At the significance level of 1%, the test fails to reject the null hypothesis that there is no unit root. The series is stationary.')
    elif t_statistic < critical_val_dict['5%']:
        print('At the significance level of 5%, the test fails to reject the null hypothesis that there is no unit root. The series is stationary.')
    elif t_statistic < critical_val_dict['10%']:
        print('At the significance level of 10%, the test fails to reject the null hypothesis that there is no unit root. The series is stationary.')
    else:
        print('the test rejects the null hypothesis. The series is non-stationary.')

def differencing(series,order):
    while order != 0:
        series = series.diff()
        order -= 1
    return series