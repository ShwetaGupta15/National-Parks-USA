import os
import pathlib
import re
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import cufflinks as cf
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
import ast
from dash_holoniq_wordcloud import DashWordcloud
import plotly.express as px

# Initialize app

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "National Parks"
server = app.server

# Load data

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

mapbox_access_token = "pk.eyJ1Ijoic2h3ZXRhMTUwOSIsImEiOiJjbDdjbjR5NWMwbmNwM3ZxZnY0amg4M2R3In0.AzeVZvgp6bg5Jl25Qu8qzg"
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"

# App layout
parksDict = pd.read_csv("./parksDataNew.csv").to_dict("records")
parksDf = pd.read_csv("./parksData.csv")
activitiesList = [ast.literal_eval(i['Activities']) for i in parksDict]
activityList = [item for sublist in activitiesList for item in sublist]
occurrence = {item: activityList.count(item) for item in activityList}
wordCloudList = list([key,val] for key,val in occurrence.items())
del activitiesList,activityList,occurrence,parksDict

def normalise(lst, vmax=50, vmin=16):
    lmax = max(lst, key=lambda x: x[1])[1]
    lmin = min(lst, key=lambda x: x[1])[1]
    vrange = vmax-vmin
    lrange = lmax-lmin or 1
    for entry in lst:
        entry[1] = int(((entry[1] - lmin) / lrange) * vrange + vmin)
    return lst

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.A(
                    html.Img(id="logoGithub", src=app.get_asset_url("github.png")),
                    href="https://github.com/ShwetaGupta15",target="_blank"
                ),
                html.A(
                    html.Img(id="logoLinkedIn", src=app.get_asset_url("linkedin.png")),
                    href="https://www.linkedin.com/in/shweta-gupta-a97704a5/",target="_blank"
                ),
                html.A(
                    html.Button("Tableau Public Profile", className="link-button"),
                    href="https://public.tableau.com/profile/shweta.gupta7830#!/",target="_blank"
                ),
                html.H4(children="National Parks of United States of America"),
                html.P(
                    id="description",
                    children="This analysis is intended to be a practical introduction to each of the America's 62 national parks.\
                         We highlight the best activities and trails, explain how to get there, show you the wildlife to watch out for. \
                        From Acadia to Zion, this beautiful introduction to all 62 parks is packed with practical information, \
                        inspiring tips on what to do and see in each.",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="map-container",
                            children=[
                                html.P(
                                    "Map of national parks in USA",
                                    id="map-title",
                                ),
                                dcc.Graph(
                                    id="map-graph",
                                    
                                    figure=dict(
                                        data=[
                                            dict(
                                                lat = parksDf['Latitude'],
                                                lon = parksDf['Longitude'],
                                                #text = parksDf.Description.str.wrap(30).apply(lambda x: x.replace('\n','<br>')),
                                                text = parksDf["Park Name"],
                                                type="scattermapbox",
                                                mode='markers+text',
                                                textposition="top center",
                                                textfont_color='orange'
                                                #hoverinfo="text",

                                            )
                                    ],
                                        layout=dict(
                                            mapbox=dict(
                                                layers=[],
                                                accesstoken=mapbox_access_token,
                                                style=mapbox_style,
                                                center=dict(
                                                    lat=38.72490, lon=-95.61446
                                                ),
                                                pitch=0,
                                                zoom=3.5,
                                                
                                            ),
                                            margin=dict(r=0, l=0, t=0, b=0),
                                            autosize=True,
                                        ),
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    DashWordcloud(
                            id="wordcloud-graph",
                            list=normalise(wordCloudList),
                            width=500,height=800,
                            gridSize=16,
                            color='#7fafdf',
                            backgroundColor='#1f2630',
                            shuffle=False,
                            rotateRatio=0.5,
                            shrinkToFit=True,
                            shape='pentagon',
                            hover=True
                        ),
                    
                ),
                html.H4("", id="report"),
            ],
        ),
    ],
)

@app.callback(
    Output(component_id="map-graph",component_property="figure")
    ,[Input(component_id="wordcloud-graph",component_property="click"),Input(component_id="map-graph",component_property="figure")]
    )
def updateMap(item,figure):
    if item is not None:
        app.logger.info(item[0])
    else:
        app.logger.info('Empty selection!')
    return figure

if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0',port='9950')