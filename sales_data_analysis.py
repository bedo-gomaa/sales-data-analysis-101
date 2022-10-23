from collections import Counter
from itertools import combinations
from itertools import count, groupby
import matplotlib.pyplot as plt
import pandas as pd
import os
df = pd.read_csv("Sales_Data/Sales_April_2019.csv")
df.head
files = [file for file in os.listdir(
    "D:\work and education\programming\python project/Sales_Data")]
all_month_data = pd.DataFrame()
for file in files:
    df = pd.read_csv(
        "D:\work and education\programming\python project/Sales_Data/"+file)
all_month_data = pd.concat([all_month_data, df])
all_month_data.to_csv("all_data.csv", index=False)

all_data = pd.read_csv("all_data.csv")
all_data
all_data = all_data.dropna(how="all")
nan_df = all_data[all_data.isna().any(axis=1)]


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data['month'] = all_data['Order Date'].str[0:2]
all_data['month'] = all_data['month'].astype('int32')
all_data.head()


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])
all_data['sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.tail(100)
# what is the best month for sale and  how much earn that month
result = all_data.groupby('Order ID').sum()
print(result)
# what is the best city in sales
# first creat new column call city from  'Purchase Address' column in data bwlow the code for that


def get_city(address):
    return address.split(',')[1]


def get_state(address):
    return address.split(',')[2].split(' ')[1]


all_data['city'] = all_data['Purchase Address'].apply(
    lambda x: get_city(x) + ' ' + get_state(x))
all_data.head()
# code below to andentify what the best city in sales
result = all_data.groupby('city').sum()
print(result)
# show the result in graph

cities = [city for city, df in all_data.groupby('city')]
plt.bar(cities, result['sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.xlabel('city name')
plt.ylabel('sales in $')
plt.show()

# what is the best time to but advertisments to maximize customers buying products ?
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['minute'] = all_data['Order Date'].dt.minute
all_data.head()


hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.grid()
plt.xlabel("hour")
plt.ylabel('number of orders')
plt.show
# what products are most often soled together ?
# if the product orderd 2 or more times
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['groubed'] = df.groupby('Order ID')[
    'Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'groubed']].drop_duplicates()
df.head()
# now counting the unique pairs of numbers into a python dictionary

count = Counter()
for row in df['groubed']:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list, 2)))
for key, value in count.most_common(10):
    print(key, value)


# what product sold the most and why do you think  sold the most

product_groub = all_data.groupby("Product")
quantity_orderd = product_groub.sum()['Quantity Ordered']

products = [product for product, df in product_groub]

plt.bar(products, quantity_orderd)
plt.ylabel('orderd')
plt.xlabel("product")
plt.xticks(products, rotation='vertical', size=8)

# to answer why do you think it sold the most
# and the answer is that whenever the price is less the product sold the most as shown in figure.

prices = all_data.groupby("Product").mean()['Price Each']


fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_orderd, color='g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('product name ')
ax1.set_ylabel('quantity orderd', color='g')
ax2.set_ylabel('price $', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()
