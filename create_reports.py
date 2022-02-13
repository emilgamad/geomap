import plotly
import plotly.express as px
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    #fig = px.bar(dataframe, x=xAxis, y='decPlantParcelArea',  title="Parcel Vs Planted Area")
    #fig.add_trace(x=xAxis,y)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=dataframe[f'{xAxis}'], y=dataframe['decPlantParcelArea'], name="decPlantParcelArea data"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=dataframe[f'{xAxis}'], y=dataframe['decPlantPlantedArea'], name="decPlantPlantedArea data"),
        secondary_y=True,
    )
    fig.update_layout(
        title_text="Parcel Vs Planted Area"
    )
    fig.update_yaxes(title_text="<b>decPlantParcelArea</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>decPlantPlantedArea</b>", secondary_y=True)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    percent_harvested = None
    total_harvested = None
    max_yield = None
    average_yield = None
    min_yield = None
    production = None

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