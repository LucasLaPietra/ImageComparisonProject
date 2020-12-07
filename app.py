import pandas as pd
import dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from metodos import extraerVector,tensorToString,resizeImagen,obtenerPokemonSimil

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
app.title = 'Comparacion imagenes Pokemon'

BarraSuperior = dbc.Navbar(
    children=[
        html.Div(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col([
                        html.A(html.Img(className="logo", src=app.get_asset_url("LogoUTN.png")),
                               href='http://www.frcu.utn.edu.ar/')
                    ], md=2),
                    dbc.Col([
                        html.H1(children='Comparacion de imagenes de Pokemon'),
                        html.H5(children='Por Lucas La Pietra, Nadia Chrispens, Kevin Pavon y Carlos Velazquez')
                    ])
                ],
                align="center",
                no_gutters=True
            )
        )
    ],
    color="primary",
    dark=True,
    sticky="top"
)

BODY = dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                html.H2(children='Ingrese foto de Pokemon a comparar:'),
                dcc.Upload(
                    id='upload-image',
                    children=html.Div([
                        'Arrastre o ',
                        html.A('Seleccione una imagen')
                    ]),
                    style={
                        'width': '100%',
                        'height': '150px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False,
                ),
            ], width=12

            ), justify="center", className='imageRow'
        ),
        dbc.Row(
            [
                dbc.Col([
                    dbc.CardHeader(html.H5("Nuestro Pokemon")),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.Col([
                                    html.Img(id='imagenPropia',className="pokemon",src=app.get_asset_url("Unown-Question.png")),
                                ])
                            )
                        ])
                ], md=5),
                dbc.Col([
                    html.Img(className="arrow", src=app.get_asset_url("arrow.png"))
                ], md=2),
                dbc.Col([
                    dbc.CardHeader(html.H5("Pokemon Resultado")),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                dbc.Col([
                                    html.Img(id='imagenResultado',className="pokemon", src=app.get_asset_url("Unown-Question.png")),
                                    html.H4(id='textoResultado',children='ninguna coincidencia')
                                ])
                            )
                        ])
                ], md=5)
            ],
            align="center",
            no_gutters=True
        )
    ],
    className="mt-12",
)

server = app.server

app.layout = html.Div(children=[
    BarraSuperior,
    BODY])

@app.callback([Output('imagenPropia', 'src'),Output('imagenResultado', 'src'),Output('textoResultado', 'children')],
              Input('upload-image', 'contents'),Input('upload-image', 'filename'))
def update_graph(contents, filename):
    if contents:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            imagensubida=contents
            pokemonsimilar=obtenerPokemonSimil(contents)
            imagenresultado=app.get_asset_url(pokemonsimilar[2])
            textoresultado=f'Pokemon: {pokemonsimilar[1]}, Distancia:{pokemonsimilar[0]}'
            return imagensubida,imagenresultado,textoresultado
    else:
        imagennosubida = app.get_asset_url("Unown-Question.png")
        textoresultado = 'ninguna coincidencia'
        return imagennosubida,imagennosubida,textoresultado


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
