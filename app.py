import pandas as pd
import dash
from dash.dependencies import Output, Input, State
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
                                    html.H4(id='textoResultado',children='ninguna coincidencia'),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Ver 5 mas cercanos", id="popover-target"
                                            ),
                                            dbc.Popover(
                                                [
                                                    dbc.PopoverHeader("5 mas cercanos"),
                                                    dbc.PopoverBody("Cargue una imagen para ver informacion", id="contenidopopover"),
                                                ],
                                                id="popover",
                                                is_open=False,
                                                target="popover-target",
                                            ),
                                        ]
                                    )
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

@app.callback([Output('imagenPropia', 'src'),Output('imagenResultado', 'src'),Output('textoResultado', 'children'),
               Output('contenidopopover', 'children')],
              Input('upload-image', 'contents'),Input('upload-image', 'filename'))
def update_graph(contents, filename):
    if contents:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            imagensubida=contents
            pokemonsimilar=obtenerPokemonSimil(contents)
            imagenresultado=app.get_asset_url(pokemonsimilar[0][2])
            textoresultado=f'Pokemon: {pokemonsimilar[0][1]}, Distancia:{pokemonsimilar[0][0]}'
            textopopover = f'Pokemon: {pokemonsimilar[0][1]}, Distancia:{pokemonsimilar[0][0]} \n ' \
                           f'Pokemon: {pokemonsimilar[1][1]}, Distancia:{pokemonsimilar[1][0]} \n' \
                           f'Pokemon: {pokemonsimilar[2][1]}, Distancia:{pokemonsimilar[2][0]} \n' \
                           f'Pokemon: {pokemonsimilar[3][1]}, Distancia:{pokemonsimilar[3][0]} \n' \
                           f'Pokemon: {pokemonsimilar[4][1]}, Distancia:{pokemonsimilar[4][0]} \n'
            return imagensubida,imagenresultado,textoresultado,textopopover
    else:
        imagennosubida = app.get_asset_url("Unown-Question.png")
        textoresultado = 'ninguna coincidencia'
        textopopover= 'Cargue una imagen para ver informacion'
        return imagennosubida,imagennosubida,textoresultado,textopopover

@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
