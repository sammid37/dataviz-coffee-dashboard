# Importações necessárias
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__)

dados_preco = {
    'Meses': ['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07', '2023-08'],
    'Preco': [34.51, 31.78, 32.17, 30.73, 35.02, 33.59, 33.96, 33.63]
}

df_preco = pd.DataFrame(dados_preco)
df_preco['Meses'] = pd.to_datetime(df_preco['Meses'])
anos = df_preco['Meses'].dt.year.unique()

# Dicionário de tipos de café e quantidade exportada
dados_cafe = {
    'Anos': ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016'],
    'Cafe Arábica': [37929, 32721, 31437, 48793, 34296, 47484, 34249, 43382],
    'Cafe Robusta': [16814, 18155, 16293, 14310, 15013, 14174, 10721, 7987]
}

app.layout = html.Div(
    children=[
        html.H1(
            children='Produção e Consumo de Café no Brasil', style={'text-align': 'center'}
        ),
        html.Div(
            children=[
                html.H3(
                    children='Preço no varejo', style={'text-align': 'center'}
                ),
                dcc.Dropdown(
                    id='preco-dropdown',
                    options=[{'label': str(ano), 'value': ano} for ano in anos],
                    value=anos[0]
                ),
                dcc.Graph(
                    id="grafico-preco",
                ),
            ],
            style={
                'width': '40%',
                'margin': '0',
                'display': 'inline-block'
            }
        ),
        html.Div(
            children=[
                html.H3(
                    children='Tipos de Café Mais Produzidos',
                    style={'text-align': 'center'}
                ),
                dcc.Dropdown(
                    id='cafe-dropdown',
                    options=[{'label': str(ano), 'value': ano} for ano in anos],
                    value=anos[0]
                ),
                dcc.Graph(
                    id="grafico-cafe",
                ),
            ],
            style={
                'width': '40%',
                'margin-left': '50',
                'display': 'inline-block'
            }
        )
    ]
)

# Função de retorno para o gráfico de preço
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

# Atualize a função de retorno para o gráfico de barras (Tipos de Café Mais Exportados)
@app.callback(
    Output('grafico-cafe', 'figure'),
    Input('cafe-dropdown', 'value')
)
def update_cafe(ano_selecionado):
    cafe_arabica = dados_cafe['Cafe Arábica']
    cafe_robusta = dados_cafe['Cafe Robusta']
    
    fig = go.Figure(data=[
        go.Bar(name='Café Arábica', x=[ano_selecionado], y=[cafe_arabica[anos.tolist().index(ano_selecionado)]]),
        go.Bar(name='Café Robusta', x=[ano_selecionado], y=[cafe_robusta[anos.tolist().index(ano_selecionado)]])
    ])
    
    fig.update_layout(
        title=f'Quantidade de Café Arábica e Robusta em {ano_selecionado}',
        xaxis=dict(title='Tipo de Café'),
        yaxis=dict(title='Quantidade Produzida por tipo'),
        barmode='group'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
