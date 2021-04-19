import pandas as pd

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_leaflet as dl

import myfunc as mf
import plot_network as net
import mywordcloud as wc

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


df = pd.read_excel('dashboard_data.xlsx')
df.head()


def radar_graph():
    return html.Div(dcc.Graph(id='radar_graph', figure=mf.sentiment_radar(df, '11 Cadogan Gardens'),
                              style=RADAR_GRAPH_STYLE
                              ), )


def hotel_name():
    return html.Div([

        html.Div(id='name', children=mf.get_address(df, '11 Cadogan Gardens'), style={
            'textAlign': 'left',
            'color': colors['text'],
            'font-size': '30px',
            'margin-left': '20px', })

    ])


def address():
    return html.Div([

        html.Div(children='''Address: ''', style={
            'textAlign': 'left',
            'color': colors['text'],
            'font-size': '15px',
            'margin-left': '20px',
        }),

        html.Div(id='address', children=mf.get_address(df, '11 Cadogan Gardens'), style={
            'textAlign': 'left',
            'color': colors['text'],
            'font-size': '15px',
            'margin-left': '20px', })

    ])


def average_score():
    return html.Div([

        html.Div(children='''Rating: ''', style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size': '15px',
        }),

        html.Div(id='rating', children=mf.get_average_score(df, '11 Cadogan Gardens'), style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size': '30px'})

    ])


def num_review():
    return html.Div([

        html.Div(children='''Total Number of Reviews: ''', style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size': '15px',
        }),

        html.Div(id='num_review', children=mf.get_num_review(df, '11 Cadogan Gardens'), style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size': '30px'})

    ])


# ----------------- Plot Coordinates ---------------------#

def plot_coordinate(value='11 Cadogan Gardens'):
    search_data = df[df['Hotel_Name'] == value]

    lat = search_data.lat.values[0]
    lng = search_data.lng.values[0]
    name = search_data.Hotel_Name.values[0]
    address_ = search_data.Hotel_Address.values[0]

    markers = [dl.Marker(position=[lat, lng],
                         children=[dl.Popup('Name: ' + name + ', Address: ' + address_, )])]

    return html.Div([dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer")] +
                            [dl.LayerGroup(markers)],
                            center=[lat, lng], zoom=14,
                            id="map",
                            style=MAP_STYLE
                            ),
                     ]),


def word_correlation():
    return html.Div(
        dcc.Graph(id='word_correlation', figure=net.word_correlation_plot(df, '11 Cadogan Gardens', 'staff'),
                  style=WORD_CORRELATION_STYLE))


def wordcloud_rend():
    return html.Div(
        dcc.Graph(id='wordcloud', figure=wc.wordcloud_draw(df, '11 Cadogan Gardens'), style=WORDCLOUD_STYLE),
    )


# the style arguments for the main content page.

aspects = ['staff', 'room', 'breakfast', 'service', 'view', 'restaurant', 'bathroom', 'pool']

CONTENT_STYLE = {
    'margin-left': '5%',
    'margin-right': '5%',
    'padding': '20px 10p',
    'backgroundColor': '#EDF7F9'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

MAP_STYLE = {'width': '100%',
             'height': '30vh',
             "display": "inline-block"
             }

RADAR_GRAPH_STYLE = {'width': '100%',
                     'height': '50vh',
                     "display": "inline-block",
                     "position": "relative"
                     }

WORD_CORRELATION_STYLE = {'width': '100%',
                          'height': '40vh',
                          "display": "inline-block",
                          "position": "relative"
                          }
WORDCLOUD_STYLE = {'width': '100%',
                   'height': '40vh',
                   "display": "inline-block",
                   "position": "relative"
                   }

CARD_HEADER_STYLE = {'backgroundColor': '#B4D7E6'}

colors = {
    'background': '#111111',
    'text': '#3C91B1'

}

dropdownlist = [{'label': i, 'value': i} for i in df['Hotel_Name']]
aspectsdropdownlist = [{'label': i, 'value': i} for i in aspects]

dropdown_1 = dcc.Dropdown(id='dropdown',
                          options=dropdownlist,
                          value='11 Cadogan Gardens')

dropdown_2 = dcc.Dropdown(id='aspect_dropdown',
                          options=aspectsdropdownlist,
                          value='staff')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

card = dbc.Card(
    [dbc.CardHeader("Header"), dbc.CardBody("Body")], className="h-100"
)

graph_card = dbc.Card(
    [dbc.CardHeader("Here's a graph"), dbc.CardBody("An amazing graph")],
    className="h-100",
)

content = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Row(
                        [

                            dbc.Col(
                                [
                                    dbc.Card(
                                        [dbc.CardHeader(html.Div(children=["Hotel Name", html.Br(), dropdown_1]),
                                                        style=CARD_HEADER_STYLE),
                                         dbc.CardBody(plot_coordinate()), html.Hr()], className="h-100"
                                    )
                                ], md=6

                            ),

                            dbc.Col(
                                [
                                    dbc.Card(
                                        [dbc.CardHeader("Hotel Information", style=CARD_HEADER_STYLE),
                                         dbc.CardBody([hotel_name(), address()])
                                         ], className="h-100"
                                    )
                                ], md=4

                            ),

                            dbc.Col(
                                [
                                    dbc.Card(
                                        [dbc.CardHeader("Score", style=CARD_HEADER_STYLE),
                                         dbc.CardBody([average_score(), html.Br(), html.Br(), num_review()])],
                                        className="h-100"
                                    )

                                ], md=2),
                        ],

                        style={"height": "400px"}),

                    html.Br(),

                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [
                                            dcc.Tabs(
                                                [
                                                    dcc.Tab(label='Hotel Facilities Sentiment Score', children=[
                                                        radar_graph()

                                                    ], style=CARD_HEADER_STYLE),

                                                    dcc.Tab(label='Word Correlation',
                                                            children=
                                                            [dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            html.Div(dropdown_2)
                                                                        ])
                                                                ]),

                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            [
                                                                                html.Div(word_correlation())
                                                                            ])
                                                                    ])

                                                            ], style=CARD_HEADER_STYLE),
                                                ])
                                        ], className="h-100"
                                    )
                                ], md=8

                            ),
                            dbc.Col(
                                [
                                    dbc.Card(
                                        [dbc.CardHeader(html.Div(children=["Word Cloud", html.Br()]),
                                                        style=CARD_HEADER_STYLE),
                                         dbc.CardBody(wordcloud_rend())  # word_correlation())
                                         ], className="h-100"
                                    )
                                ]),

                        ],

                        style={"height": "450px"}
                    ),

                    html.Br(),

                ],
                width=11,
            ),
        ],
        justify="center",
    ),
    fluid=True,
    className="mt-3",
)

layout = html.Div(
    [
        html.Br(),
        html.H2(
            children='Sentiment Analysis on Hotel Reviews Data in Europe',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Br(),

        html.Div(children=['''This dashboard aims to provide information about 
        the quality of hotel facilities in the capitals of European countries 
        based on customer reviews from Booking.com. The scoring of each facilities 
        is done by performing sentiment analysis to measure how good or how 
        bad the facilities are provided (see “Hotel Facilities Sentiment Score” tab). 
        Topic modelling is used to determine the relevant facilities 
        provided by the hotels (see “Word Correlation” tab). '''],
                 style={'textAlign': 'center',
                        'color': colors['text']
                        }
                 ),

        html.Div(children=[' Data Source: ', dcc.Link('\nKaggle. ', href='https://www.kaggle.com/jiashenliu/515k-hotel-reviews-data-in-europe')], style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size': '12px',
        }),

        html.Br(),

        html.Div(children=['''Project by Ariqleesta (LBB Algoritma).'''], style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size': '12px',
        }),
        html.Div(children=[
                           dcc.Link('\nLinkedIn, ', href='https://www.linkedin.com/in/ariqleesta/'),
                           dcc.Link('\nGitHub ', href='https://github.com/ariqleesta')], style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size': '12px',
        }),
        html.Hr(),
        content
    ],
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([layout], style=CONTENT_STYLE)

app.title = "Hotel Reviews in Europe"


@app.callback(
    Output('radar_graph', 'figure'),
    [Input('dropdown', 'value')])
def update_figure(value):
    return mf.sentiment_radar(df, value)


@app.callback(
    Output('name', 'children'),
    [Input('dropdown', 'value')])
def update_name(value):
    return mf.get_hotel_name(value)


@app.callback(
    Output('address', 'children'),
    [Input('dropdown', 'value')])
def update_address(value):
    return mf.get_address(df, value)


@app.callback(
    Output('rating', 'children'),
    [Input('dropdown', 'value')])
def update_rating(value):
    return mf.get_average_score(df, value)


@app.callback(
    Output('num_review', 'children'),
    [Input('dropdown', 'value')])
def update_num_review(value):
    return mf.get_num_review(df, value)


@app.callback(
    Output('word_correlation', 'figure'),
    [Input('dropdown', 'value'), Input('aspect_dropdown', 'value')])
def update_word_correlation(value1, value2):
    return net.word_correlation_plot(df, value1, value2)


@app.callback(
    Output('wordcloud', 'figure'),
    [Input('dropdown', 'value')])
def update_word_correlation(value):
    return wc.wordcloud_draw(df, value)


@app.callback(
    Output('map', 'children'),
    [Input('dropdown', 'value')])
def update_coordinate(value):
    return plot_coordinate(value)


#if __name__ == '__main__':
#    app.run_server(host="127.0.0.1", port=8080, )
if __name__ == '__main__':
    app.run_server(debug=True)