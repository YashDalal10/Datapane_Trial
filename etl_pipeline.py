# packages
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date, timedelta


# file reading
yearly_data = pd.read_csv('data/yearly_stock_data.csv')
my_portfolio = pd.read_excel('data/YD_shares.xlsx', sheet_name = 'Sheet1')
company_names = pd.read_csv('data/company_name.csv')
latest_data = pd.read_csv('data/latest_value.csv')


# rounding off numbers
col_list = ['Open','High','Low','Close']
for i in range(len(col_list)):
    yearly_data[col_list[i]] = np.round(yearly_data[col_list[i]],2)
    latest_data[col_list[i]] = np.round(latest_data[col_list[i]],2)


# preprocessing yearly data
# yearly_data['Date'] = pd.to_datetime(yearly_data['Date'])
# yearly_data['Date'] = yearly_data['Date'].dt.date
# print(yearly_data.sample(10))
yearly_data = yearly_data.merge(company_names, how = 'inner', on = 'ticker')
yearly_data.drop(['ticker'], axis = 1, inplace = True)
yearly_data['Returns'] = np.round(yearly_data.groupby('name')['Close'].diff(),2)
yearly_data['Returns'] = yearly_data['Returns'].fillna(0)
print("Yearly Data Preprocessing complete")
# print(yearly_data.sample(10))


# # latest data
# # latest_date = date.today() - timedelta(1)
# # latest_date = pd.Timestamp(latest_date)
# # latest_df1 = yearly_data[yearly_data['Date']==latest_date]
latest_data = latest_data.merge(company_names, how = 'inner', on = 'ticker')
latest_data.drop(['ticker'], axis = 1, inplace = True)
print("Latest Data Preprocessing complete")
# print(latest_data.columns)
# print(latest_data.head(10))


# preprocessing portfolio info
# print("My Portfolio")
# print(my_portfolio.head(10))
my_portfolio['Weighted_Price'] = np.round(my_portfolio['Buy Price'] * my_portfolio['Quantity'],2)
weighted_mean = np.round(my_portfolio.groupby('name')['Weighted_Price'].sum() / my_portfolio.groupby('name')['Quantity'].sum(),2)
shares_quantity = my_portfolio.groupby(['name'])['Quantity'].sum()
buy_price = {'name':weighted_mean.index, 'avg_buy_price':weighted_mean.values, 'quantity': shares_quantity.values}
buy_price = pd.DataFrame(buy_price)
print("Buy Price preprocessing complete")
# print(buy_price.sample(10))


# merging the latest data with portfolio
my_portfolio_latest = my_portfolio.merge(latest_data, how = 'inner', on = 'name')
print("Portfolio Latest completed")
# print(my_portfolio.head(10))
my_portfolio_latest.to_csv('data/portfolio_latest.csv', index=False)


# grouping names together
latest_price = np.round(my_portfolio_latest.groupby(['name'])['Close'].mean(),2)
# print(latest_price)
latest_price = {'name':latest_price.index, 'latest_price':latest_price.values}
latest_price = pd.DataFrame(latest_price)
print("Latest Price deduced")
# print(latest_price.head(10))


# merging the derived columns of both dfs
latest_price = latest_price.merge(buy_price, how = 'inner', on = 'name')
latest_price['Gain_per_stock'] = latest_price['latest_price'] - latest_price['avg_buy_price']
latest_price['total_earnings'] = latest_price['quantity'] * latest_price['Gain_per_stock']
latest_price['percentage_earnings'] = np.round((latest_price['latest_price'] / latest_price['avg_buy_price']) * 100,2)
profit = []
for i in range(len(latest_price)):
    if latest_price['total_earnings'][i] >= 0:
        profit.append(1)
    else:
        profit.append(0)  
latest_price['Profit_Loss'] = profit
print("Profit Loss found")
# print(latest_price.sample(10))
# print("\n")
latest_price.to_excel('data/profit_loss_statement.xlsx', index = False)
yearly_data.to_csv('data/yearly_data.csv', index=False)
print("SUCCESS!!!")
# print("Successfully executed latest data available.")



