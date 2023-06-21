from turtle import width
import altair as alt
import datapane as dp
import numpy as np
import pandas as pd

profit_loss_df = pd.read_excel('data/profit_loss_statement.xlsx')
buy_price = profit_loss_df['avg_buy_price'] * profit_loss_df['quantity']
gain_sort = profit_loss_df.sort_values(by = ['Gain_per_stock'], ascending = False)
total_sort = profit_loss_df.sort_values(by = ['total_earnings'], ascending = False)
quantity_sort = profit_loss_df.sort_values(by = ['quantity'], ascending = False)
percentage_increase = profit_loss_df.sort_values(by = ['percentage_earnings'], ascending = False)
total_sort = total_sort[['name','total_earnings']]
total_top10 = total_sort[:10].copy()
total_others = total_sort[10:].copy()
others_sum = np.round(total_others['total_earnings'].sum(),2)
others_row = {'name': 'Others', 'total_earnings': others_sum}
others_row = pd.DataFrame(others_row, columns=['name','total_earnings'], index = ['11'])
total_sort_df = pd.concat([total_top10, others_row])
total_sort_df = total_sort_df.reset_index(drop=True)

yearly_data = pd.read_csv('data/yearly_data.csv')

# dropdown1 = alt.binding_select(options = yearly_data.name.unique(), name = 'Stock')
# selection = alt.selection_single(fields = ['name'], bind = dropdown1)
# color = alt.condition(selection, alt.Color('name:N').legend(None), alt.value('lightgray'))

# yearly_plot = alt.Chart(yearly_data).mark_line().encode(x = 'Date', y = 'Close', color = color).add_params(selection)

custom_color_scheme = ['#1F6459', '#978BB0', '#E21F1F', '#E4FA03', '#1FAC38', '#3A3B3B',
                       '#1DEAC1', '#346706', '#ED9D2A', '#2564F6', '#DE4F6E']

fig1 = alt.Chart(gain_sort[:10]).mark_bar(color = "#1FAC38").encode(x='Gain_per_stock',y='name').properties(width=500,height=300)
fig2 = alt.Chart(gain_sort[-5:]).mark_bar(color = "#E21F1F").encode(x='Gain_per_stock',y='name').properties(width=400,height=300)

fig_up = fig1 | fig2 

fig3 = alt.Chart(total_sort[:10]).mark_bar(color = "#1DEAC1").encode(x='total_earnings',y='name').properties(width=450,height=300)
fig4 = alt.Chart(percentage_increase[:10]).mark_bar(color = "#1F6459").encode(x='percentage_earnings',y='name').properties(width=450,height=300)

fig_down = fig3 | fig4

fig5 = alt.Chart(quantity_sort[:10]).mark_bar(color = "#E21F1F").encode(x='quantity',y='name').properties(width=450,height=300)
fig6 = alt.Chart(total_sort_df).mark_arc().encode(theta="total_earnings",color=alt.Color('name:N', scale=alt.Scale(range=custom_color_scheme)))

fig_viz1 = fig5 | fig6

grouping = dp.Group(
    dp.BigNumber(
        heading="PROFIT",
        value="\u20B9 " + str(np.round(np.sum(gain_sort[gain_sort['Profit_Loss']==1]['total_earnings']),2)), #65393.1
        # change="2%",
        # is_upward_change=True,
    ),
    dp.BigNumber(
        heading="Amount of shares bought",
        value="\u20B9 " + str(np.round(np.sum(buy_price),2)),
        # change="2%",
        # is_upward_change=False,
    ),
    dp.BigNumber(
        heading="LOSS",
        value="\u20B9 " + str(np.round(np.sum(gain_sort[gain_sort['Profit_Loss']==0]['total_earnings']),2)), #10613.8
        # change="200",
        # is_upward_change=True,
    ),
    dp.BigNumber(
        heading="Number of profit making stocks",
        value=str(np.sum(profit_loss_df['Profit_Loss']))+" out of "+str(len(profit_loss_df['Profit_Loss'])),
        # change="200",
        # is_upward_change=False,
    ),
    columns=2,
)

view = dp.View(dp.Text("# Yash Portfolio Statement"),
               dp.Group(grouping),
               dp.Text("### Gains and Loss per Stock in \u20B9"),
               dp.Plot(fig_up),
               dp.Text("### Top 10 earners and top 10 movers"),
               dp.Plot(fig_down),
               dp.Text('### Quantity of Stocks and Total Gains by percentage'),
               dp.Plot(fig_viz1))
            #    dp.Plot(yearly_plot))
        # dp.Select(dp.Group(grouping), dp.Plot(fig), dp.DataTable(profit_loss_df)))
# dp.save_report(view, "report/ersten_report.html", open=True)
dp.serve_app(view)
# print("Successfully done bro! Welcome to Datapane!")