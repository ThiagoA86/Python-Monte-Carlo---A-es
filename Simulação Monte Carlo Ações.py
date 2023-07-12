#!/usr/bin/env python
# coding: utf-8

#Importações
import numpy as np
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
from scipy.stats import norm
import math
#Grafico matplotlib
import matplotlib.pyplot as plt
#Grafico Plotly interativo
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

pio.renderers.default='browser'
#Criando o periodo de inicio 10 anos antes
startdate=datetime(2013,7,12)
yf.pdr_override()

#Escolhendo o ação Itaú Preferencial
tickers = 'GGBR3.SA'
#Criando o Data Frame
data = pd.DataFrame()
#Colentando os dados pelo yahoo finance o fechamento ajustado
data[tickers] = pdr.DataReader(tickers,data_source='yahoo',start=startdate)['Adj Close']
maximo = int(data.max().max())
minimo = int(data.min().min())
intervalo_sup = int(maximo*1.35)
numero_O= data.size
sturge = 1+(3.3*math.log(numero_O,10))
intervalo=int((maximo-minimo)/sturge)


# Retorno Logaritmo natural
log_retorno = np.log(1+data.pct_change())
#log_retorno.tail()

#Grafico da Parcial
#plt.plot(figsize=(10,6))
#data.plot(figsize=(10,6))
#log_retorno.plot(figsize=(10,6))

#Media dos retornos
u = log_retorno.mean()
print(u)

#Variância dos retornos
var =log_retorno.var()
print(var)

#Drift
drift = u-(0.5*var)
#drift

#Desvio padrão
stdev = log_retorno.std()
print(stdev)
type(drift)
type(stdev)

#transformar em Numpy
drift.values
stdev.values

#norm.ppf(0.95) - Distribuição normal 95% de confiança
#Gerar numero aleatorio 0 a 1
#x = np.random.rand(10,2)
#norm.ppf(x)
#Z = norm.ppf(np.random.rand(10,2))
#Z
#Intervalo de um 1 ano (250) sessões B3 e 10 simulaçoes de previsoes Monte Carlo
t_intervalo = 250
interacao = 10
#Retorno diario usando o Drift
retorno_diario = np.exp(drift.values+stdev.values*norm.ppf(np.random.rand(t_intervalo,interacao)))
# Simulação para 250 dias para 10 simulação
#print(retorno_diario)

#Pegando o valor do ultimo pregão. Usamos os ultimos 10 anos para ter a estatistica de comportamento e ultimo pregão para fazer o proximo ano de previsão.
s0 = data.iloc[-1]
#s0

# Cria matriz da mesma dimensão apenas com zeros
lista_preco = np.zeros_like(retorno_diario)
#lista_preco

# Preenche a primeira linha com ultimo preço dessa ação
lista_preco[0]=s0
#lista_preco

#Preço no dia t menos o preço t-1 * Retorno diario. Vai preenchendo com o Drift simulado os outros dias.

for t in range(1,t_intervalo):
    lista_preco[t]=lista_preco[t-1]*retorno_diario[t]

#Ultimo preço, primeira simulação, preço da ultima simulação
#print(lista_preco[:,0])
#print(lista_preco[1])
#print(lista_preco[249])

#Grafico das dez possiveis simulaçao da ação com Matplot retire caso não precise
plt.figure(figsize=(10,6))
plt.plot(lista_preco)
plt.title('Simulação da '+tickers)
plt.xlabel("Dias", fontsize=14)
plt.xticks(range(0,255,20),rotation=45)
#plt.xticks(range(0,250,25))
plt.yticks(range(minimo,intervalo_sup,intervalo))
plt.ylabel('Valor da Ação', fontsize=14)
for i in range(0,10):
    plt.plot(lista_preco[:,i],label=f'Simulação {(i+1)}')
plt.legend(loc=(0.1, 0.5))
#Local salvará a figura.
plt.savefig('C:/Python Finanças/imagem/'+tickers+'.png')
plt.show()

#grafico interativo com browser Plotly retire caso não precise
fig = go.Figure()
for i in range(0,10):
    fig.add_trace(go.Scatter(y=lista_preco[:,i], name=f'Simulação {(i+1)}'))
fig.update_xaxes(title_text='Dias',range=[0,255],dtick=25)
fig.update_yaxes(title_text='Preço da Ação',range=[minimo,intervalo_sup],dtick=intervalo)
fig.update_layout(title=f'Simulação da {tickers}')
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()





