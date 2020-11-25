import pandas as pd
import dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(SeleccionFecha), className="w-100", md=12) ], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(FreqHistGraph)), ], style={"marginTop": 30}),
        dbc.Row([dbc.Col(dbc.Card(AnalisisTopicos)), ], style={"marginTop": 30}),
    ],
    className="mt-12",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = 'Comparacion imagenes Pokemon'
server = app.server

app.layout = html.Div(children=[
    BODY])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
