from cProfile import label
from turtle import color
import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import dcc, html
import plotly.express as px
# import dash_table
import plotly.graph_objs as go
from statistics import mean
from queries import *
import sqlalchemy

#old version
# from dash_core_components.Interval import Interval
# from dash_html_components.Br import Br
# from dash_html_components.Div import Div
# from dash_html_components.Label import Label
# import dash_core_components as dcc
# import dash_html_components as html


mapbox_access_token = 'pk.eyJ1Ijoic2luYTE5OTMiLCJhIjoiY2twbXI5ZGM0MGk1ZTJvbWVwYmljNTgyMCJ9.I8FOC4V9hgOm2biN3SR9Tg'
engine = sqlalchemy.create_engine(
    "postgresql://elwas:PelwasG21@nig.eolab.de:5432/elwas")

print("connect to DB")
query = "select * from hygrisc.nitrat_long"
df = pd.read_sql(query, engine)


app = dash.Dash(
    __name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width"}],
)

app.title = "Groundwater"
server = app.server




app.layout = html.Div(
    [

        html.Div(
            [

                html.Div(
                    [

                        html.H3(
                            "Groundwater",
                            style={"margin-bottom": "0px",
                                   'font-weight': 'bold'},
                        ),
                    ],
                    className="three column",
                    id="title",
                ),

            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div([

            html.Div([

                dcc.RangeSlider(
                    id='range-slider',  # any name you'd like to give it
                    marks={
                        2000: '2000',     # key=position, value=what you see
                        2005: '2005',
                        2010: '2010',
                        2015: '2015',
                        2020: '2020',


                    },
                    step=1,                # number of steps between values
                    min=2000,
                    max=2020,
                    value=[2000, 2010],     # default value initially chosen
                    dots=True,             # True, False - insert dots, only when step>1
                    allowCross=False,      # True,False - Manage handle crossover
                    disabled=False,        # True,False - disable handle
                    pushable=2,            # any number, or True with multiple handles
                    updatemode='mouseup',  # 'mouseup', 'drag' - update value method
                    included=True,         # True, False - highlight handle
                    vertical=False,        # True, False - vertical, horizontal slider
                    # hight of slider (pixels) when vertical=True
                    verticalHeight=900,
                    className="dcc_control",

                ),
            ], className="pretty_container eight columns"),

            html.Div([
                dcc.Dropdown(
                    id="factor",
                    options=[

                        {"label": "Nitrat", "value": "Nitrat"},
                        {"label": "Sulfat", "value": "Sulfat"},


                    ],
                    multi=False,
                    value='Nitrat',
                    className="dcc_control",
                ),

            ], className="pretty_container two columns"),
            html.Div([

                dcc.RadioItems(
                    id="data_range",
                    options=[
                        {'label': 'Avrage ',
                         'value': 'avrage'},
                        {'label': 'Specefic year',
                         'value': 'specefic_year'},

                    ],
                    value='avrage',


                    labelStyle={"display": "inline-block"},
                    className="dcc_control",
                ),



            ], className="pretty_container two columns")

        ], className="row flex-display"),

        html.Div(
            [html.Div([


                dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                          #   style={'background': '#00FC87', 'padding-bottom': '2px',
                          #          'padding-left': '2px', 'height': '100vh'}
                          )
                # dcc.Interval(
                #     id='interval-component',
                #     interval=60*1000,  # in milliseconds
                #     n_intervals=0
                # )
            ], className="pretty_container twelve columns"),


            ],
            className="row flex-display",
        ),




    ]
)


df1 = get_table_nitrat("hygrisc")

df1[["year", "month", "day"]] = df1["datum_pn"].astype(
    str).str.split("-", expand=True)



@app.callback(Output('graph', 'figure'),
              [Input('factor', 'value'), Input('range-slider', 'value'), Input('data_range', 'value')])
def update_graph_live(x, i, n):

    if ((x == "Nitrat") and (n == "avrage")):
        # df1 = df_lat
        colors_list = ['green', 'blue', 'yellow', 'red', 'brown', 'black']

        df1["year"] = df1["year"].astype(int)
        dff = df1[(df1['year'] >= i[0]) & (df1["year"] <= i[1])]

        dff = dff.sort_values('year')
        grouped = dff.groupby(['messstelle_id'], as_index=False).mean()
        grouped['color'] = pd.cut(grouped['messergebnis_c'], bins=[0, 30, 50, 70, 120, 200, 566.7], include_lowest=True, labels=[
                                  '0-30 mg/L', '30-50 mg/L', '50-70 mg/L', '70-120 mg/L', '120-200 mg/L', '200-566 mg/L'])
        grouped = grouped.sort_values('color')

       
        fig = px.scatter_mapbox(grouped, title="Nitrate Concentration ", lat="lat", lon="long", color="color", color_discrete_sequence=colors_list,  hover_name="messstelle_id", hover_data=["messergebnis_c", "year"], labels={'color': 'Nitrate Concentration', 'year': 'Date',
                                                                                                                                                                                                                                'messergebnis_c': 'Result', 'lat': 'Latitude', 'long': 'Longitude', 'messstelle_id': 'Station id'}, zoom=8, height=800, size_max=10)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    if ((x == "Sulfat") and (n == "avrage")):
        colors_list = ['green', 'blue', 'yellow',
                       'red', 'brown', 'gray', 'black']
        df2 = get_table_sulfat("hygrisc")
        df2[["year", "month", "day"]] = df1["datum_pn"].astype(
            str).str.split("-", expand=True)
        df2["year"] = df2["year"].astype(int)
        df_sulfat = df2[(df2['year'] >= i[0]) & (df2["year"] <= i[1])]
        grouped_sulfat = df_sulfat.groupby(
            ['messstelle_id'], as_index=False).mean()
        grouped_sulfat['color'] = pd.cut(grouped_sulfat['messergebnis_c'], bins=[0, 30, 50, 70, 120, 200, 566.7, 3980], include_lowest=True, labels=[
                                         '0-30 mg/L', '30-50 mg/L', '50-70 mg/L', '70-120 mg/L', '120-200 mg/L', '200-566 mg/L', '566-3980 mg/L'])
        grouped_sulfat = grouped_sulfat.sort_values('color')
        grouped_sulfat.sort_values(by=['year', 'color'], axis=0, ascending=[
                                   True, True], inplace=True)

        fig = px.scatter_mapbox(grouped_sulfat, title="Sulfat Concentration ", lat="lat", lon="long", color="color",
                                color_discrete_sequence=colors_list, hover_name="messstelle_id", hover_data=["messergebnis_c", "year"], labels={'color': 'Sulfat Concentration', 'datum_pn': 'Date',
                                                                                                                                                'messergebnis_c': 'Result', 'lat': 'Latitude', 'long': 'Longitude', 'messstelle_id': 'Station id'}, zoom=8, height=800, size_max=5)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    if ((x == "Nitrat") and (n == "specefic_year")):
        colors_list = ['green', 'blue', 'yellow', 'red', 'brown', 'black']
        df1["year"] = df1["year"].astype(int)
        df_ns = df1[(df1['year'] >= i[0]) & (df1["year"] <= i[1])]
        df_ns['color'] = pd.cut(df_ns['messergebnis_c'], bins=[0, 30, 50, 70, 120, 200, 566.7], include_lowest=True, labels=[
                                '0-30 mg/L', '30-50 mg/L', '50-70 mg/L', '70-120 mg/L', '120-200 mg/L', '200-566 mg/L'])
        df_ns.sort_values(by=['year', 'color'], axis=0,
                          ascending=[True, True], inplace=True)

        fig = px.scatter_mapbox(df_ns, title="Nitrate Concentration ", lat="lat", lon="long", color="color", color_discrete_sequence=colors_list, animation_frame="year",  hover_name="messstelle_id", hover_data=["messergebnis_c", "datum_pn"], labels={'color': 'Nitrate Concentration', 'datum_pn': 'Date',
                                                                                                                                                                                                                                                          'messergebnis_c': 'Result', 'lat': 'Latitude', 'long': 'Longitude', 'messstelle_id': 'Station id'}, zoom=8, height=800, size_max=10)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    if ((x == "Sulfat") and (n == "specefic_year")):
        colors_list = ['green', 'blue', 'yellow',
                       'red', 'brown', 'gray', 'black']
        df2 = get_table_sulfat("hygrisc")
        df2[["year", "month", "day"]] = df2["datum_pn"].astype(
            str).str.split("-", expand=True)
        df2["year"] = df2["year"].astype(int)
        df_ss = df2[(df2['year'] >= i[0]) & (df2["year"] <= i[1])]

        df_ss['color'] = pd.cut(df_ss['messergebnis_c'], bins=[0, 30, 50, 70, 120, 200, 566.7, 3980], include_lowest=True, labels=[
            '0-30 mg/L', '30-50 mg/L', '50-70 mg/L', '70-120 mg/L', '120-200 mg/L', '200-566 mg/L', '566-3980 mg/L'])
        # df_ss = df_ss.sort_values('color')
        # df_ss = df_ss.sort_values('year')
        df_ss.sort_values(by=['year', 'color'], axis=0,
                          ascending=[True, True], inplace=True)

        fig = px.scatter_mapbox(df_ss, title="Sulfat Concentration ", lat="lat", lon="long", color="color", color_discrete_sequence=colors_list, animation_frame="year",  hover_name="messstelle_id", hover_data=["messergebnis_c", "datum_pn"], labels={'color': 'Sulfat Concentration', 'datum_pn': 'Date',
                                                                                                                                                                                                                                                         'messergebnis_c': 'Result', 'lat': 'Latitude', 'long': 'Longitude', 'messstelle_id': 'Station id'}, zoom=8, height=800, size_max=10)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    # fig.show()
    return fig




# Main
if __name__ == "__main__":
    app.run_server(debug=False)



