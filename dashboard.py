# Importações necessárias
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__)

# dicionario do preco no varejo  - grafico 1
dados_preco = {
    'Meses': 
    ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09', '2022-10', '2022-11','2022-12',
     '2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07', '2023-08'],
    'Preco': 
    [30.25, 34.91, 35.36, 34.17, 33.13, 37.38, 32.99, 36.23, 33.86, 34.33, 37.82, 35.90, 
    34.51, 31.78, 32.17, 30.73, 35.02, 33.59, 33.96, 33.63]
}
df_preco = pd.DataFrame(dados_preco)
df_preco['Meses'] = pd.to_datetime(df_preco['Meses'])
opcoes_varejo = ['Últimos 5 meses', 'Novembro 2022 - Março 2023', 'Junho 2022 - Outubro 2022', 'Janeiro 2022 - Maio 2022']

# dicionário de tipos de café e quantidade exportada - grafico 2
dados_cafe = {
    'Anos': ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016'],
    'Cafe Arábica': [37929, 32721, 31437, 48793, 34296, 47484, 34249, 43382],
    'Cafe Robusta': [16814, 18155, 16293, 14310, 15013, 14174, 10721, 7987]
}
anos = list(dados_cafe['Anos'])

app.layout = html.Div(
    children=[
        html.H1(
            children='Produção e Consumo de Café no Brasil', style={'text-align': 'center'}
        ),
        html.Div(
            children=[
                html.H3(
                    children='Preço no varejo', style={'text-align': 'left'}
                ),
                dcc.Dropdown(
                    id='preco-dropdown',
                    options=[{'label': str(opcao), 'value': opcao} for opcao in opcoes_varejo],
                    value=opcoes_varejo[0]
                ), # ajeitar eixo para ter início 0
                dcc.Graph(
                    id="grafico-preco",
                ),
            ],
            style={
                'width': '40%',
                'margin': '5%',
                'display': 'inline-block'
            }
        ), # verificar dados do gráfico abaixo
        html.Div(
            children=[
                html.H3(
                    children='Produção por tipo de café',
                    style={'text-align': 'right'}
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
                'margin-right': '5%',
                'display': 'inline-block'
            }
        )
    ]
)

# função de retorno para o gráfico de preço
@app.callback(
    Output('grafico-preco', 'figure'),
    Input('preco-dropdown', 'value')
)
def update_preco(opcao):
    # os meses estão aparecendo em inglês, trocar se der tempo
    if opcao == opcoes_varejo[0]:
        x_filtr = list(df_preco['Meses'])[-5:]
        y_filtr = list(df_preco['Preco'])[-5:]
    elif opcao == opcoes_varejo[1]:
        x_filtr = list(df_preco['Meses'])[-10:-5]
        y_filtr = list(df_preco['Preco'])[-10:-5]
    elif opcao == opcoes_varejo[2]:
        x_filtr = list(df_preco['Meses'])[-15:-10]
        y_filtr = list(df_preco['Preco'])[-15:-10]
    else:
        x_filtr = list(df_preco['Meses'])[:5]
        y_filtr = list(df_preco['Preco'])[:5]
    return {
        'data':[{
            'x': x_filtr,
            'y': y_filtr,
            'type': 'line',
            'name': 'serie preco'
        }],
        'layout':{
            'title': '',
            'xaxis': {'title': ''},
            'yaxis': {'title': 'R$ / Kg'}
        }
    }

# função de retorno para producao por tipo
@app.callback(
    Output('grafico-cafe', 'figure'),
    Input('cafe-dropdown', 'value')
)
def update_cafe(ano_selecionado):
    cafe_arabica = dados_cafe['Cafe Arábica']
    cafe_robusta = dados_cafe['Cafe Robusta']
    
    fig = go.Figure(data=[
        go.Bar(name='Café Arábica', x=[ano_selecionado], y=[cafe_arabica[anos.index(ano_selecionado)]]),
        go.Bar(name='Café Robusta', x=[ano_selecionado], y=[cafe_robusta[anos.index(ano_selecionado)]])
    ])
    
    fig.update_layout(
        title=f'Quantidade de Café Arábica e Robusta em {ano_selecionado}',
        xaxis=dict(title='Tipo de Café'),
        yaxis=dict(title='Quantidade produzida por tipo'),
        barmode='group'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
