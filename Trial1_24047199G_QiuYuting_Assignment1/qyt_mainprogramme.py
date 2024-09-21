import requests
from bs4 import BeautifulSoup
import statistics
import numpy as np
from qyt_tocsv import to_csv
import matplotlib.pyplot as plt

url = "https://www.hko.gov.hk/tide/CCHtextPH2024.htm"

response = requests.get(url)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

data = []
table = soup.find('table')

for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    while "" in cols:
        cols.remove("")
    data.append(cols)
data.remove([])
#From Qyt: Data is the list of all January tide data

data_number = []
for i in data:
    float_list = [float(x) for x in i[2:]]
    data_number.append(float_list)
    mean = round(statistics.mean(float_list), 2)
    variance = round(statistics.variance(float_list), 2)
    i.append(mean)
    i.append(variance)
#From Qyt: Calculate the mean and variance,append to data

columns = ['Month','Day']
for i in range(1,25):
    columns.append('Hour_{}'.format(i))
columns.append('Mean')
columns.append('Variance')
#From Qyt: generate the list beginning

data.insert(0, columns)
to_csv('tide_data_January.csv',data)
#From Qyt: write into a csv document for reading

MEAN_list = []
VAR_list = []
for i in data[1:]:
    MEAN_list.append(i[int(len(i)-2)])
    VAR_list.append(i[int(len(i)-1)])
#From Qyt: Extract the mean and variance data from the table

x_forvar = list(range(1,32))

fig, ax = plt.subplots(1, 2)
plt.subplots_adjust(wspace=0.5)
fig.suptitle('Tide height changes in January')

ax[0].stem(x_forvar, VAR_list)
ax[0].plot(x_forvar, MEAN_list, label='Mean')
ax[0].plot(x_forvar, VAR_list, label='Variance')
ax[0].legend()

ax[0].set_xlabel('Day', loc = 'right')
ax[0].set_ylabel('Height',loc = 'top')
ax[0].set_title('Mean and Variance')
#From Qyt: Draw Chart 1, mainly showing the changes in the average and variance of daily tidal heights in January

plt.style.use('_mpl-gallery-nogrid')
Z_array = np.array(data_number)
ax[1].imshow(Z_array, origin='lower')
ax[1].set_title('EveryDay Height Colormap')
ax[1].set_xlabel('Hour', loc = 'right')
ax[1].set_ylabel('Day',loc = 'top')
#From Qyt: Draw Chart 2, which mainly maps the daily tidal height values in January to the color depth values to form a color map

plt.savefig('QiuYuting_Assignment1_Finalfigure.png')
plt.show()













