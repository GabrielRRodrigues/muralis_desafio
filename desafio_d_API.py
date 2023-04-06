import logging

import mysql.connector
import requests
from datetime import datetime
from flask import Flask, request, make_response, jsonify
from logging.handlers import TimedRotatingFileHandler
from logging import info, basicConfig

app = Flask(__name__)

handler = TimedRotatingFileHandler(r'LOGS\api.log', when='d', interval=1, backupCount=2, encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
)


def _conectar():  # Conexão com o BD BD02
    try:
        global conexao_bd2
        conexao_bd2 = mysql.connector.connect(
            host='localhost',
            database='bd02',
            user='root',
            password='G1935@@_sr')
        info('BD acessado!')
        cursor = conexao_bd2.cursor()
        return cursor
    except mysql.connector.Error as e:
        print(f'Erro de conexão com o BD: {e}')


def _busca_cep(cep):  # Consulta o CEP na API ViaCEP
    dados_endereco_tratados = []
    try:
        # Requisição via API
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        response.raise_for_status()

        dados_endereco = response.json()

        dados_endereco_tratados.append(dados_endereco['logradouro'])
        dados_endereco_tratados.append(dados_endereco['bairro'])
        dados_endereco_tratados.append(dados_endereco['localidade'])

        return dados_endereco_tratados
    except requests.exceptions.RequestException as e:
        return f'Erro ao consultar CEP {cep}: {e}'

# Indicação de rota HTTP e tipo da solicitação
@app.route('/cadastrar_funcionario/', methods=['POST'])
def cadastrar_funcionario():
    funcionario = request.json
    nome = funcionario['nome'].title()
    rg = funcionario['rg'].replace('.', '').replace('-', '')
    cpf = funcionario['cpf'].replace('.', '').replace('-', '')
    data_admissao_datetime = datetime.strptime(funcionario['data_admissao'], '%d/%m/%Y')
    data_admissao_formatada = data_admissao_datetime.strftime('%Y-%m-%d')
    cep = funcionario['cep'].replace('-', '')
    dados_endereco_tratados = _busca_cep(cep)

    cursor_create = _conectar()

    try:
        cursor_create.execute(f'INSERT INTO funcionarios_fabrica (ID, Nome, RG, CPF, Data_admissao, '
                              f'Data_hora_alteracao_do_registro, CEP, ENDERECO, BAIRRO, CIDADE) VALUES (default, '
                              f'"{nome}", "{rg}", "{cpf}", "{data_admissao_formatada}", NOW(), "{cep}", '
                              f'"{dados_endereco_tratados[0]}", "{dados_endereco_tratados[1]}", '
                              f'"{dados_endereco_tratados[2]}")')
        conexao_bd2.commit()
        info('Funcionário cadastrado!')

        return make_response(
            jsonify(funcionario)
        )
    except mysql.connector.errors as e:
        return f'Erro ao cadastrar funcionário: {e}'
    finally:
        cursor_create.close()
        conexao_bd2.close()


@app.route('/buscar_funcionario/<int:ID>', methods=['GET'])
def buscar_funcionario(ID):
    cursor_read = _conectar()
    try:
        cursor_read.execute(f'SELECT * FROM funcionarios_fabrica WHERE ID = {ID}')
        funcionario = cursor_read.fetchall()
        info('Funcionário consultado!')

        return make_response(
            funcionario
        )
    except mysql.connector.errors as e:
        return f'Erro ao buscar funcionários: {e}'
    finally:
        cursor_read.close()
        conexao_bd2.close()


@app.route('/atualizar_funcionario/<int:ID>', methods=['PUT'])
def atualizar_funcionario(ID):
    funcionario = request.json
    nome = funcionario['nome'].title()
    rg = funcionario['rg'].replace('.', '').replace('-', '')
    cpf = funcionario['cpf'].replace('.', '').replace('-', '')
    data_admissao_datetime = datetime.strptime(funcionario['data_admissao'], '%d/%m/%Y')
    data_admissao_formatada = data_admissao_datetime.strftime('%Y-%m-%d')
    cep = funcionario['cep'].replace('-', '')
    dados_endereco_tratados = _busca_cep(cep)

    cursor_update = _conectar()

    try:
        cursor_update.execute(f'UPDATE funcionarios_fabrica SET NOME = "{nome}", RG = "{rg}", CPF = "{cpf}", '
                              f'Data_admissao = "{data_admissao_formatada}", Data_hora_alteracao_do_registro = NOW(), '
                              f'CEP = "{cep}", ENDERECO = "{dados_endereco_tratados[0]}", '
                              f'BAIRRO = "{dados_endereco_tratados[1]}", CIDADE = "{dados_endereco_tratados[2]}" '
                              f'WHERE id = {ID}')
        conexao_bd2.commit()
        info('Funcionário atualizado!')

        return make_response(
            jsonify(funcionario)
        )
    except mysql.connector.errors as e:
        return f'Erro ao buscar funcionários: {e}'
    finally:
        cursor_update.close()
        conexao_bd2.close()


@app.route('/deletar_funcionario/<int:ID>', methods=['DELETE'])
def deletar_funcionario(ID):
    cursor_delete = _conectar()
    try:
        cursor_delete.execute(f'DELETE FROM funcionarios_fabrica WHERE ID = {ID}')
        conexao_bd2.commit()
        info('Funcionário deletado!')

        return 'Funcionário deletado com sucesso!'
    except mysql.connector.errors as e:
        return f'Erro ao deletar funcionário: {e}'
    finally:
        cursor_delete.close()
        conexao_bd2.close()


if __name__ == '__main__':
    app.run(debug=True)
