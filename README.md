# Supplemental Code

[![DOI](https://zenodo.org/badge/483473735.svg)](https://zenodo.org/badge/latestdoi/483473735)

The code is written in Python.</p>
All of its dependencies can be installed by running the following in the terminal (with the `requirement.txt` file included in this repository):
```python
pip install -r requirement.txt
```

Introduction of the files:</p>
`Data`: This folder includes all the data downloaded online including top rap songs, suicide rates, GNP per capita and growth, divorce rates and unemployment rates.</p>
`analysis.py`: the module includes several Python functions that can help reproducing the analysis.</p>
`music.py`: the module includes several Python functions that can help processing the lyrical texts.</p>
`LIWC2007_English100131.dic`: the dictionary that assigns English words into different categories. It is used to help counting the percentage of words related to some topics.</p>
`data_crawler.ipynb`: codes that show how I utilize **Genius api** to scrape the lyrics texts, process the texts by using music module, and combine all the time series data into one dataframe.</p>
`Project code.ipynb`: codes and results that show how I conduct **KPSS test** , **correlation analysis**, **model construction**, and **cross correlation analysis**</p>

To reproduce the code, you should first import the `analysis` module in this repository. </p>
```python
import analysis
```
Then use the `plot_by_column` function to plot every column of the data (each column representing one time series).
```python
analysis.plot_by_column('data/data.csv')
```
Here are the plots of relevant lyrical mentions and suicide rates across the years: </p>
![lyrical mentions related to death, negative emotions](https://github.com/macs30200-s22/replication-materials-zhiqianc/blob/main/README_files/lyrical%20mentions%20percentage_by_year.png)
![suicide rates](https://github.com/macs30200-s22/replication-materials-zhiqianc/blob/main/README_files/Suicide%20rate_by_year.png)

This two series need to stationary before being fed into the models. Let's use the `kpss_test` function in the `analysis` module to test. 
```python
data = pd.read_csv('data/data.csv',index_col=0)
analysis.kpss_test(data['lyrical mentions percentage'])
analysis.kpss_test(data['Suicide rate'])
```
The outputs are:
```
lyrical mentions series
KPSS Statistic: 0.3560785846689506
p-value: 0.09608681695303853
num lags: 9
Critial Values:
   10% : 0.347
   5% : 0.463
   2.5% : 0.574
   1% : 0.739
Result: The series is stationary
```
```
Suicide rates series
KPSS Statistic: 0.3720922077283856
p-value: 0.08918439322052346
num lags: 9
Critial Values:
   10% : 0.347
   5% : 0.463
   2.5% : 0.574
   1% : 0.739
Result: The series is stationary
```

The kpss test shows these two series are  stationary. No further processing is required</p>

These initial findings are important. When building models on time series data, we need to make sure these time series are stationary (no unit root exists). If the unit root exists, the relationship between the independent and dependent variables is deceptive because any error in the residual sequence does not decay as the sample size (the number of periods) increases, meaning that the effect of the residual in the model is permanent. This regression is also called pseudo-regression. If the unit root exists, the process is a random walk.</p>

To use this repository for a scientific publication, you can cite the Zenodo DOI.
