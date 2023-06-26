import random
from statistics import LinearRegression
import time
from flask import Flask, jsonify, request
import mysql.connector
import pandas as pd

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '6713Mauricio1993@',
    'database': 'dados',
    'autocommit': True  # Ativa o modo de autocommit para evitar problemas de transações
}

# Função para estabelecer a conexão com o banco de dados
def conectar_bd():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as error:
        print(f'Erro ao conectar ao banco de dados: {error}')
        return None

# Função para executar uma consulta no banco de dados
def executar_consulta(query, parametros=None):
    conn = conectar_bd()
    if conn:
        try:
            cursor = conn.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as error:
            print(f'Erro ao executar consulta: {error}')
        finally:
            cursor.close()
            conn.close()
    return None
#-======================================================================
def executar_comando(query, valores=None):
    try:
        # Configurar a conexão com o banco de dados
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='6713Mauricio1993@',
            database='dados'
        )
        
        cursor = cnx.cursor()
        
        # Executar o comando SQL
        if valores:
            cursor.execute(query, valores)
        else:
            cursor.execute(query)
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
        return True
    except Exception as e:
        print(f"Erro ao executar o comando: {e}")
        return False
#========================================================================

# Rota para obter todos os dados do banco de dados
@app.route('/dados', methods=['GET', 'POST'])
def obter_dados():
    if request.method == 'GET':
        # Lógica para obter os dados existentes do banco
        query = 'SELECT * FROM DailyDelhiClimateTrain'
        dados = executar_consulta(query)
        
        if dados:
            resultados = []
            for registro in dados:
                resultado = {
                    'data': registro[1],
                    'temperatura' : registro[2],
                    'umidade': registro[3],
                    'velocidade_do_vento': registro[4],
                    'pressao_media': registro[5],
                    # Adicione mais campos conforme necessário
                }
                resultados.append(resultado)
            return jsonify(resultados)
        else:
            return jsonify({'message': 'Nenhum dado encontrado'})
    
    elif request.method == 'POST':
        # Lógica para adicionar novos dados ao banco
        if 'data' in request.json and 'temperatura' in request.json and 'umidade' in request.json and 'velocidade_do_vento' in request.json and 'pressao_media' in request.json:
            data = request.json['data']
            temperatura = request.json['temperatura']
            umidade = request.json['umidade']
            velocidade_do_vento = request.json['velocidade_do_vento']
            pressao_media = request.json['pressao_media']
            
            # Lógica para inserir os dados no banco de dados
            
            # Exemplo de consulta SQL para inserir os dados
            query = "INSERT INTO DailyDelhiClimateTrain (data, temperatura, umidade, velocidade_do_vento, pressao_media) VALUES (%s, %s, %s, %s, %s)"
            valores = (data, temperatura, umidade, velocidade_do_vento, pressao_media)
            executar_comando(query, valores)
            
            return jsonify({'message': 'Dados adicionados com sucesso'})
        else:
            return jsonify({'message': 'Parâmetros inválidos'})


#==========================================================================================


# Função para obter os dados do banco de dados
def obter_dados():
    query = 'SELECT * FROM DailyDelhiClimateTrain'
    dados = executar_consulta(query)
    if dados:
        df = pd.DataFrame(dados, columns=['data', 'temperatura', 'umidade', 'velocidade_do_vento', 'pressao_media'])
        return df
    return None

#=================================================================

if __name__ == '__main__':
    app.run()
