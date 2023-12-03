import streamlit as st
import requests
import pandas as pd
import plotly.express as px   

st.set_page_config(layout='wide')

st.title("MINERADOR DE PRODUTOS AFILIADOS")

produtos = pd.read_csv('produto.csv')
#print(f'Produtos {produtos.shape}')
produtores = pd.read_csv('produtores.csv')
produtos = produtos.drop_duplicates()
#print(f'Produtos Drop {produtos.shape}')
produtores = produtores.drop_duplicates()

#print(produtos.shape)

juncao =  pd.merge(produtos, produtores, left_on='name', right_on='product.name')
#print(juncao.shape)

juncao['preco_produto'] = juncao['price.value']
juncao['temperature'] = juncao['temperature'].astype(float)
#juncao['affiliation.commission.price.currency'] = juncao['affiliation.commission.price.currency'].astype(float)
juncao['valor_comissao'] = juncao['affiliation.commission.price.value']
juncao['percentual_comissao'] = juncao['affiliation.commission.percentage'] 

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas', list(juncao.columns), list(juncao.columns))
    #print(colunas)

st.sidebar.title('Filtros')

categorias = juncao['category'].unique()
producters = juncao['producer.name'].unique()


categoria = st.sidebar.selectbox('Categorias dos Produtos', categorias, index=None)
produtor = st.sidebar.selectbox('Produtor', producters, index=None)
with st.sidebar.expander('Preço do Produto'):
    preco = st.sidebar.slider('Selecione o preço', 0,1000,(97,497))

with st.sidebar.expander('Temperatura'):
    temp = st.sidebar.slider('Temperatura', 1, 100,(10,50))
    #print('''@preco[0]''')

with st.sidebar.expander('% Commissão'):
    comissaopercentual = st.sidebar.slider('% Comissão', 1, 100,(1,100))
    #print(comissao_percentual)

with st.sidebar.expander('R$ Commissão'):
    valor_comissao = st.sidebar.slider('R$ Comissão', 1, 1000,(0, 100))

paginavenda = st.sidebar.checkbox('Com página de venda')

if paginavenda:
    juncao = juncao[juncao['pageSalesLink'].notna()]

if categoria:
    juncao= juncao[juncao['category']== categoria]

if produtor:
    juncao= juncao[juncao['producer.name']== produtor]

#print(juncao['percentual_comissao'])
query = '''
    @preco[0] <= preco_produto <= @preco[1] and \
    @temp[0] <= temperature <= @temp[1] and \
    @comissaopercentual[0] <= percentual_comissao <= @comissaopercentual[1] and \
    @valor_comissao[0] <= valor_comissao <= @valor_comissao[1]


'''

dados_filtrados = juncao.query(query)
#print(dados_filtrados.shape)
dados_filtrados = dados_filtrados[colunas]
st.dataframe(dados_filtrados)
st.markdown(f'Número de Registros :blue[{dados_filtrados.shape[0]}] linhas :blue[{dados_filtrados.shape[1]}] colunas')


