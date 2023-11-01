# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

estilo  = ['estilo.css']
app = Dash(__name__)

dados_preco = {
        'Meses': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07', '2023-08'],
        'Preco': [34.51, 31.78, 32.17, 30.73, 35.02, 33.59, 33.96, 33.63]
}
df_preco = pd.DataFrame(dados_preco)
df_preco['Meses'] = pd.to_datetime(dados_preco['Meses']) 
anos = df_preco['Meses'].dt.year.unique()

app.layout = html.Div(
    children = [
        html.H1(
            children ='Produção e Consumo de Café no Brasil', style={'text-align': 'center'}
        ),
        html.Div(
            children = [
                html.H3(
                    children = 'Preço no varejo', style = {'text-align': 'center'}
                ),
                dcc.Dropdown(
                    id = 'preco-dropdown',
                    options=[{'label': str(ano), 'value': ano} for ano in anos],
                    value=anos[0]
                ),
                dcc.Graph(
                    id="grafico-preco",
                ),
            ],
            style = {
                'width': '40%',  
                'margin': '0',
                'display': 'inline-block'  
            }
        ),
        html.Div(
            children = [
                html.H3(
                    children = 'Preço no varejo', style = {'text-align': 'center'}
                ),
                dcc.Dropdown(
                    id = 'preco-dropdown2',
                    options=[{'label': str(ano), 'value': ano} for ano in anos],
                    value=anos[0]
                ),
                dcc.Graph(
                    id="grafico-preco2",
                ),
            ],
            style = {
                'width': '40%',  
                'margin-left': '50',
                'display': 'inline-block'  
            }
        )
    ]
)

@app.callback(
    Output('grafico-preco', 'figure'),
    Input('preco-dropdown', 'value')
)
def update_preco(ano_selecionado):
    dados_filtrados = df_preco[df_preco['Meses'].dt.strftime('%Y') == ano_selecionado]
    return {
        'data':[{
            'x': df_preco['Meses'],
            'y': df_preco['Preco'],
            'type': 'line',
            'name': 'serie preco'
        }],
        'layout':{
            'title': '',
            'xaxis': {'title': ''},
            'yaxis': {'title': 'R$ / Kg'}
        }
    }


app.run(debug=True)
