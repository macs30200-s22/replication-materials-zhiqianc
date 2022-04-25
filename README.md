# Supplemental Code

The code is written in Python.</p>
Introduction of the files:</p>
`Data`: This folder includes all the data downloaded online including top rap songs, suicide rates, GNP per capita and growth, divorce rates and unemployment rates.</p>
`analysis.py`: the module includes several Python functions that can help reproducing the analysis.</p>
`music.py`: the module includes several Python functions that can help processing the lyrical texts.</p>
`LIWC2007_English100131.dic`: the dictionary that assigns English words into different categories. It is used to help counting the percentage of words related to some topics.</p>
`data_crawler.ipynb`: codes that show how I utilize **Genius api** to scrape the lyrics texts, process the texts by using music module, and combine all the time series data into one dataframe.</p>
`ADFtest.ipynb`: codes and results that show how I conduct **ADF test** on lyrics mentions percentage and suicide rates</p>

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

It seems that this two series are non-stationary. Let's use the `adftest` function in the `analysis` module to test. 
```python
data = pd.read_csv('data/data.csv',index_col=0)
analysis.adf_test(data['lyrical mentions percentage'])
analysis.adf_test(data['Suicide rate'])
```
The outputs are:
```
Lyrical mentions series:
ADF Statistic: -0.4159667435653719
p-value: 0.907398576229738
Critial Values:
   1%, -3.7529275211638033
Critial Values:
   5%, -2.998499866852963
Critial Values:
   10%, -2.6389669754253307
Test conclusion:
the test rejects the null hypothesis. The series is non-stationary.
```
```
Suicide rates series
ADF Statistic: -0.0136069442726193
p-value: 0.9573922308417956
Critial Values:
   1%, -4.137829282407408
Critial Values:
   5%, -3.1549724074074077
Critial Values:
   10%, -2.7144769444444443
Test conclusion:
the test rejects the null hypothesis. The series is non-stationary.
```

The ADF test shows these two series are not stationary. To solve it, `differencing` function in `analysis` module can make the series stationary. Then use `adf_test` again.

```python
analysis.adf_test(analysis.differencing(data['lyrical mentions percentage'],1))
analysis.adf_test(analysis.differencing(data['Suicide rate'],1))
```
The outputs are:
```
Lyrical mentions series (After first order difference):
ADF Statistic: -5.420586730191859
p-value: 3.0657883922907044e-06
Critial Values:
   1%, -3.769732625845229
Critial Values:
   5%, -3.005425537190083
Critial Values:
   10%, -2.6425009917355373
Test conclusion:
At the significance level of 1%, the test fails to reject the null hypothesis that there is no unit root. The series is stationary.
```

```
Suicide rates (after first order difference)
ADF Statistic: -2.8574421801122227
p-value: 0.050525437139072774
Critial Values:
   1%, -4.137829282407408
Critial Values:
   5%, -3.1549724074074077
Critial Values:
   10%, -2.7144769444444443
Test conclusion:
At the significance level of 10%, the test fails to reject the null hypothesis that there is no unit root. The series is stationary.
```

The results show after first order differencing, these two time series are stationary. Thus we will use the first order difference of these two series as the two variables of the regression model.</p>

These initial findings are important. When building models on time series data, we need to make sure these time series are stationary (no unit root exists). If the unit root exists, the relationship between the independent and dependent variables is deceptive because any error in the residual sequence does not decay as the sample size (the number of periods) increases, meaning that the effect of the residual in the model is permanent. This regression is also called pseudo-regression. If the unit root exists, the process is a random walk.</p>

To use this repository for a scientific publication, you can cite the Zenodo DOI.
