from dash import Dash, html, dcc, Input, Output

import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as mpl

import geobr

import plotly.graph_objects as go
import plotly as plt
import plotly.express as px

import json

from urllib.request import urlopen


app = Dash(__name__)

######################## Dados ########################


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
preco_max = max(list(df_preco['Preco']))
opcoes_varejo = ['Últimos 5 meses', 'Novembro 2022 - Março 2023', 'Junho 2022 - Outubro 2022', 'Janeiro 2022 - Maio 2022']

# dicionário de tipos de café e quantidade exportada - grafico 2
dados_cafe = {
	'Anos': ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016'],
	'Cafe Arábica': [37929, 32721, 31437, 48793, 34296, 47484, 34249, 43382],
	'Cafe Robusta': [16814, 18155, 16293, 14310, 15013, 14174, 10721, 7987]
}
anos_cafe = list(dados_cafe['Anos'])

# dicionario do consumo per capita - grafico 3
dados_per_capita = {
	'Anos': [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 
						2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
	'Café Verde': [4.65, 5.01, 5.14, 5.34, 5.53, 5.64, 5.81, 6.02, 6.10, 6.23, 
									6.09, 6.12, 6.12, 6.29, 6.38, 6.02, 5.95, 5.99, 6.06, 5.96],
	'Café Torrado': [3.72, 4.01, 4.11, 4.27, 4.42, 4.51, 4.65, 4.81, 4.88, 4.98, 
										4.87, 4.89, 4.90, 5.03, 5.10, 4.82, 4.76, 4.79, 4.84, 4.77]
}
opcoes_per_capita = ['2018 - 2022', '2013 - 2017', '2008 - 2012', '2003 - 2007']

especies_cafe = [
	'Robusta',
	'Arabica',
	# 'Sub-total',
	'Cerrado - Arabica',
	'Planalto - Arabica',
	'Atlântico - Robusta',
	'Sul e Centro-Oeste - Arabica',
	'Triângulo, Alto Paranaíba e Noroeste - Arabica',
	'Zona da Mata, Rio Doce e Central - Arabica',
	'Zona da Mata, Rio Doce e Central - Robusta',
	'Norte, Jequitinhonha e Mucuri - Arabica',
	'Norte, Jequitinhonha e Mucuri - Robusta'
]

estados_regioes = {
	'RO': {
		'Robusta': {
			2023: 3.132,
			2022: 2.801,
			2021: 2.263,
			2020: 2.445,
			2019: 2.199,
			2018: 1.978,
			2017: 1.938,
			2016: 1.627,
			2015: 1.724,
			2014: 1.477,
			2013: 1.357,
			2012: 1.367,
			2011: 1.428,
			2010: 2.369,
			2009: 1.547,
			2008: 1.876,
			2007: 1.482,
			2006: 1.263,
			2005: 1.772,
			2004: 1.760,
			2003: 2.500,
			2002: 2.100,
			2001: 1.910,
		},
	},
	'AM': {
		'Arabica': {
			2021:31,
			2020:31,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Robusta': {
			2023:0,
			2022:0,
			2021:45,
			2020:45,
			2019:0,
			2018:0,
			2017:8,
			2016:6,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'PA': {
		'Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:6,
			2016:9,
			2015:17,
			2014:69,
			2013:122,	
			2012:167,	
			2011:184,	
			2010:229,	
			2009:228,	
			2008:233,	
			2007:266,	
			2006:280,	
			2005:330,	
			2004:220,	
			2003:220,	
			2002:310,	
			2001:250,
		},
	},
	'BA': {
		'Cerrado - Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Planalto - Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Atlântico - Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'MT': {
		'Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'GO': {
		'Arabica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'MG': {
		'Sul e Centro-Oeste - Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Triângulo, Alto Paranaíba e Noroeste - Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Zona da Mata, Rio Doce e Central - Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Zona da Mata, Rio Doce e Central - Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Norte, Jequitinhonha e Mucuri - Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Norte, Jequitinhonha e Mucuri - Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'ES': {
		'Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'RJ': {
		'Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'SP': {
		'Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'PR': {
		'Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'OUTROS': {
		'Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	},
	'BR': {
		'Arábica': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
		'Robusta': {
			2023:0,
			2022:0,
			2021:0,
			2020:0,
			2019:0,
			2018:0,
			2017:0,
			2016:0,
			2015:0,
			2014:0,
			2013:0,	
			2012:0,	
			2011:0,	
			2010:0,	
			2009:0,	
			2008:0,	
			2007:0,	
			2006:0,	
			2005:0,	
			2004:0,	
			2003:0,	
			2002:0,	
			2001:0,
		},
	}
}

df_especie_regiao = pd.DataFrame(estados_regioes)

######################## Estrutura do dashboard ########################

app.layout = html.Div(
	children=[
		html.H1(
			children='Produção e Consumo de Café no Brasil', 
			style={'text-align': 'center'}
		),
		##### div da primeira linha #####
		html. Div(
			children = [
				html.Div(
					children=[
						html.H3(
							children='Preço no varejo', style={'text-align': 'left'}
						),
						dcc.Dropdown(
							id='preco-dropdown',
							options=[{'label': str(opcao), 'value': opcao} for opcao in opcoes_varejo],
							value=opcoes_varejo[0]
						), 
						dcc.Graph(
							id="grafico-preco",
						)
					],
					style={
						'width': '40%',
						'margin-left': '5%',
						'display': 'inline-block',
						'padding': '10px'
					}
				),
				html.Div(
					children=[
						html.H3(children='Produção por tipo de café',style={'text-align': 'right'}),
						dcc.Dropdown(
							id='cafe-dropdown',
							options=[{'label': str(ano), 'value': ano} for ano in anos_cafe],
							value=anos_cafe[0]
						),
						dcc.Graph(id="grafico-cafe",)
					],
					style={
						'width': '40%',
						'margin-right': '5%',
						'display': 'inline-block',
						'padding': '10px'
					}
				)
			]
		),
		##### div da segunda linha #####
		html.Div(
			children = [
				html.Div(
					children = [
						html.H3(children='Consumo per capita',style={'text-align': 'left'}),
						dcc.Dropdown(
							id='percapita-dropdown',
							options=[{'label': str(ano), 'value': ano} for ano in opcoes_per_capita], 
							value=opcoes_per_capita[0]
						),
						dcc.Graph(
							id="grafico-percapita",
						),
					],
					style={
						'width': '40%',
						'margin': '5%',
						'display': 'inline-block'
					}
				),
				html.Div(
					children = [
						html.H3(children='Quantidade de produção por tipo de café',style={'text-align': 'right'}),
						dcc.Dropdown(
							id="mapa-dropdown",
							options=[{'label': especie, 'value': especie} for especie in df_especie_regiao.columns],
            	value=df_especie_regiao.columns[0]
						),
						dcc.Graph(
							id="grafico-mapa",
						)
					],
					style = {
						'width': '40%',
						'margin': '5%',
						'display': 'inline-block'
					}
				)
			]
		),
		#### div terceira Linha
		html.Div(
			children=[
				html.Div(
					children = [
						html.H3(children='Exportações por espécie', style = {'text-aling': 'left'})
					],
					style = {
						'width': '40%',
						'margin': '5%',
						'display': 'inline-block'
					}
				),
				html.Div(
					children = [
						html.H3(children='Exportações por  estado final', style = {'text-aling': 'right'})
					],
					style = {
						'width': '40%',
						'margin': '5%',
						'display': 'inline-block'
					}
				),
			]
		)
	]
)

######################## Funções de retorno ########################

# função de retorno para o gráfico de preço [1]
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
			'title': f'Preço no varejo do Kg de café - {opcao}',
			'xaxis': {'title': ''},
			'yaxis': {'title': 'R$ / Kg', 'range': [0, preco_max]}
		}
	}

# função de retorno para producao por tipo [2]
@app.callback(
	Output('grafico-cafe', 'figure'),
	Input('cafe-dropdown', 'value')
)
def update_cafe(ano_selecionado):
	cafe_arabica = dados_cafe['Cafe Arábica']
	cafe_robusta = dados_cafe['Cafe Robusta']
	
	fig = go.Figure(data=[
		go.Bar(name='Café Arábica', x=[ano_selecionado], y=[cafe_arabica[anos_cafe.index(ano_selecionado)]]),
		go.Bar(name='Café Robusta', x=[ano_selecionado], y=[cafe_robusta[anos_cafe.index(ano_selecionado)]])
	])
	
	fig.update_layout(
		title=f'Quantidade de Café Arábica e Robusta em {ano_selecionado}',
		xaxis=dict(title=''),
		yaxis=dict(title='Quantidade produzida por tipo'),
		barmode='group'
	)
	
	return fig

# função de retorno para o gráfico do consumo per capita [3]
@app.callback(
	Output('grafico-percapita', 'figure'),
	Input('percapita-dropdown', 'value')
)
def update_percapita(opcao):
	cafe_verde = dados_per_capita['Café Verde']
	cafe_torrado = dados_per_capita['Café Torrado']
	anos = list(dados_per_capita['Anos'])

	if opcao == opcoes_per_capita[0]:
		x_filtr = anos[-5:]
	elif opcao == opcoes_per_capita[1]:
		x_filtr = anos[-10:-5]
	elif opcao == opcoes_per_capita[2]:
		x_filtr = anos[-15:-10]
	else:
		x_filtr = anos[:5]


	fig = go.Figure()
	for i in range(5):  
		ano = x_filtr[i]
		quantidade_verde= cafe_verde[anos.index(ano)]
		quantidade_torrado = cafe_torrado[anos.index(ano)]

		fig.add_trace(go.Bar(
			name=f'Café Verde - {ano}',
			x=[ano+0.1],
			y=[quantidade_verde],
			offset=i,
			width = 0.4,
			customdata=[ano], 
			marker=dict(color='green') 
		))

		fig.add_trace(go.Bar(
			name=f'Café Torrado - {ano}',
			x=[ano+0.5],
			y=[quantidade_torrado],
			offset=i,
			width = 0.4,
			customdata=[ano],  
			marker=dict(color='brown')
		))

	fig.update_layout(
		title=f'Consumo per capita de café verde e torrado ({opcao})',
		xaxis=dict(title=''),
		yaxis=dict(title='Kg / habitante ano', range = [0, 7]),
		barmode='group',
		width = 500
	)
	return fig


# função de retorno para o gráfico Quantidade de produção por tipo de café [4]
@app.callback(
	Output('mapa-grafico', 'figure'),
	Input('mapa-dropdown', 'value')
)
def update_mapa(opcao):
	# Carregue o shapefile dos estados do Brasil
	brasil = gpd.read_file('/BR_UF_2022.shp')
	df_merged = brasil.set_index('PR').join(df_especie_regiao)
	# Crie um gráfico interativo com o Plotly Express
	fig = px.choropleth(
		df_merged,
		geojson=df_merged.geometry,
		locations=df_merged.index,
		color=opcao + '_2023',  # Escolha o ano desejado
		color_continuous_scale='Viridis',  # Escolha uma escala de cores
		hover_name='nome',  # Nome do estado a ser exibido no hover
		projection='mercator'  # Projeção do mapa
	)

	# Personalize o layout do gráfico, se necessário
	fig.update_geos(fitbounds="locations", visible=False)

	return fig

	
if __name__ == '__main__':
	app.run_server(debug=True)
