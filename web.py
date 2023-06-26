# streamlit run web.py
from PIL import Image
from flask import Request, request
from matplotlib import offsetbox
import numpy as np
import pandas as pd
import requests
import requests
import streamlit as st
import streamlit as st
import matplotlib.pyplot as plt

# Configurando o tema do Streamlit
def set_background_color(color):
    hex_color = f"#{color}"
    custom_css = f"""
        <style>
        .stApp {{
            background-color: {hex_color};
        }}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Definindo o fundo verde claro
set_background_color("CCFFCC")




# Função para fazer uma requisição GET para a API Flask e obter os dados
def obter_dados():
    response = requests.get('http://127.0.0.1:5000/dados') 
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        return None
    

# Função para exibir todos  os dados do banco no Streamlit
def exibir_dados(df):
    if df is not None:
        st.dataframe(df)
    else:
        st.write('Nenhum dado encontrado')




#=========================================================================================
# Função para exibir os dados obtidos da API Flask no Streamlit Filtro

def exibir_temperatura_umidade(dados, temp_min, temp_max, umi_min, umi_max):
    # Criação de listas vazias para armazenar os dados

    datas = []
    temperaturas = []
    umidades = []

    if dados:
        for registro in dados:
            temperatura = registro['temperatura']
            umidade = registro['umidade']
            if temp_min <= temperatura <= temp_max and umi_min <= umidade <= umi_max:
                datas.append(registro['data'])
                temperaturas.append(registro['temperatura'])
                umidades.append(registro['umidade'])
                # Adicione mais campos conforme necessário

        # Criação do DataFrame
        df = pd.DataFrame({'Data': datas, 'Temperatura': temperaturas, 'Umidade': umidades})

        # Exibindo o DataFrame
        st.dataframe(df)

    else:
        st.write('Nenhum dado encontrado')



#=======================grafico do filtro========================================
def grafico_temperatura(dados, temp_min, temp_max, umi_min, umi_max):
    datas = []
    temperaturas = []
    umidades = []

    if dados:
        for registro in dados:
            temperatura = registro['temperatura']
            umidade = registro['umidade']
            if temp_min <= temperatura <= temp_max and umi_min <= umidade <= umi_max:
                temperaturas.append(temperatura)
                umidades.append(umidade)
    
        if temperaturas:
            st.write('---')
            st.title('Gráfico da Análise:')
            fig, ax1 = plt.subplots()

            # Plot da temperatura
            ax1.plot(temperaturas, '-o', color='b')
            ax1.set_ylabel('Temperatura (°C)', color='b')
            ax1.tick_params(axis='y', colors='b')

            # Plot da umidade
            ax2 = ax1.twinx()
            ax2.plot(umidades, '-o', color='g')
            ax2.set_ylabel('Umidade (%)', color='g')
            ax2.tick_params(axis='y', colors='g')

            ax1.set_xlabel('Período')
            ax1.set_title('Variação da Temperatura e Umidade')

            # Ajustando espaçamento entre os dados
            ax1.autoscale(enable=True, axis='both', tight=True)
            ax2.autoscale(enable=True, axis='both', tight=True)

            st.pyplot(fig)
        else:
            st.write('Nenhum dado encontrado')
    else:
        st.write('Nenhum dado encontrado')




#=================================================================
image = Image.open('img/1.png')
st.image(image,width= 800)

# Configuração do título da página do Streamlit
#==============================================================
st.title('Consumindo API Flask')

#========================================Adicionar dados========================================
st.subheader('Adicionar Dados')
# Obter os dados do usuário via teclado
data = st.date_input('Date')
temperatura = st.number_input('Temperatura', min_value=0.0)
umidade = st.number_input('Umidade', min_value=0.0)
velocidade_do_vento = st.number_input('Velocidade do Vento', min_value=0.0)
pressao_media = st.number_input('Pressão Média', min_value=0.0)

# Verificar se os dados foram preenchidos
if st.button('Enviar'):
    # Criar o objeto com os dados
    dados = {
        'data': str(data),
        'temperatura': temperatura,
        'umidade': umidade,
        'velocidade_do_vento': velocidade_do_vento,
        'pressao_media': pressao_media
        # Adicione mais campos conforme necessário
    }

    # Fazer a requisição POST
    url= 'http://127.0.0.1:5000/dados'
    response = requests.post(url, json=dados)

    # Verificar o código de resposta
    if response.status_code == 201:
        st.write('Dados enviados com sucesso!')

    

#=======================================================================================


st.subheader(' Datas coletados')

textoN1='Consultar dados'
dados = obter_dados()
exibir_dados(dados)

st.subheader('Consultar Temperatura e Umidade ideal para plantio')
st.text('TEMPERATURA IDEAL PARA O PLANTIO É ENTRE 24 A 27°C' )
st.text('E A UMIDADE IDEAL É ENTRE 50 A 70% ')
if st.button(f"**{textoN1}**"):
    dados = obter_dados()
    exibir_temperatura_umidade(dados, 24, 27,50,70)
    grafico_temperatura(dados, 24, 27,50,70)
   
    
#===============================Buscar temperatura por cidade em tempo real ===========================
API_KEY = '07e876524007f97c2e34d32b70b4ca87'

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def display_weather_data(weather_data):
    if 'list' in weather_data:
        city = weather_data['city']['name']
        temperatures = []
        humidities = []
        wind_speeds = []
        pressures = []
        days = []

        for forecast in weather_data['list']:
            date_time = forecast['dt_txt']
            temperature = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            wind_speed = forecast['wind']['speed']
            pressure = forecast['main']['pressure']

            if date_time.endswith('12:00:00'):
                days.append(date_time.split()[0])
                temperatures.append(temperature)
                humidities.append(humidity)
                wind_speeds.append(wind_speed)
                pressures.append(pressure)

        st.header('Informações Climáticas')
        st.subheader('Cidade: ' + city)

        # Configurações do gráfico
        fig, ax1 = plt.subplots(figsize=(10, 6))
        x = np.arange(len(days))

        # Plot da temperatura
        ax1.plot(x, temperatures, 'b-o', label='Temperatura')
        ax1.set_ylabel('Temperatura (°C)', color='b')
        ax1.tick_params(axis='y', colors='b')

        # Plot da umidade
        ax2 = ax1.twinx()
        ax2.plot(x, humidities, 'g-o', label='Umidade')
        ax2.set_ylabel('Umidade (%)', color='g')
        ax2.tick_params(axis='y', colors='g')


        # Configurações do eixo x
        ax1.set_xticks(x)
        ax1.set_xticklabels(days)
        ax1.set_xlabel('Dia da Semana')

        # Título e legenda
        ax1.set_title('Gráficos Climatológicos', fontsize=14)
        ax1.legend(loc='upper left', fontsize='medium', bbox_to_anchor=(0, 1))

        # Ajustando o layout
        plt.tight_layout()

        # Exibindo o gráfico
        st.pyplot(fig)

        # Exibindo informações em uma tabela na barra lateral
        st.sidebar.title('Informações do Gráfico')
        data_table = {'Dia': days, 'Temperatura (°C)': temperatures, 'Umidade (%)': humidities, 'Velocidade do Vento (m/s)': wind_speeds, 'Pressão Média (hPa)': pressures}
        st.sidebar.table(data_table)

    else:
        st.write('Falha ao obter dados climáticos. Verifique se o nome da cidade está correto.')


city = st.text_input('Para obter informações climáticas, digite o nome da cidade:')
if city:
    weather_data = get_weather_data(city)
    display_weather_data(weather_data)


#======================================================================
