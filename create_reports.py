import plotly
import plotly.express as px
import json
import pandas as pd

def graph(dataframe,region,province,municipality,barangay):

    if region:
        xAxis = 'region'
    if province:
        xAxis = 'province'
    if municipality:
        xAxis = 'municipality'
    if barangay:
        xAxis = 'barangay'
    print(xAxis)
    #fig = px.bar(dataframe, x=xAxis, y=['decPlantParcelArea','decPlantPlantedArea'],  title="Parcel Vs Planted Area")
    fig = px.bar(dataframe, x=xAxis, y='decPlantPlantedArea',  title="Parcel Vs Planted Area")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#     df = pd.DataFrame({
#       'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 
#       'Bananas'],
#       'Amount': [4, 1, 2, 2, 4, 5],
#       'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
#    })
#     fig = px.bar(df, x='Fruit', y='Amount', color='City', 
#         barmode='group')
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #print(graphJSON)
    return graphJSON