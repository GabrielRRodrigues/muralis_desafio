import mysql.connector
import requests

# Conexão com os BD
conexao_bd1 = mysql.connector.connect(host='localhost', database= 'bd01', user= 'root', password='G1935@@_sr')
conexao_bd2 = mysql.connector.connect(host='localhost', database= 'bd02', user= 'root', password='G1935@@_sr')

if conexao_bd1.is_connected():
    cursor1 = conexao_bd1.cursor()

    # Recuperando dados de interesse da tabela funcionarios
    cursor1.execute('SELECT ID, RG, CPF, Data_admissao, CEP FROM funcionarios ')
    dados = cursor1.fetchall()

    if conexao_bd2.is_connected():
        cursor2 = conexao_bd2.cursor()
        try:
            for funcionario in dados:
                # Armazenando dados recuperados para uso
                id_func = funcionario[0]
                rg = funcionario[1]
                cpf = funcionario[2]
                data_admissao = funcionario[3]
                cep = funcionario[4]

                # Requisição via API
                response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
                if response.status_code == 200:
                    dados_endereco = response.json()
                    endereco = dados_endereco['logradouro']
                    bairro = dados_endereco['bairro']
                    cidade = dados_endereco['localidade']
                else:
                    print(f'Erro ao consultar CEP {cep}')

                # Atualizando dados na tabela funcionarios_fabrica
                cursor2.execute(f'UPDATE funcionarios_fabrica SET RG = "{rg}", CPF = "{cpf}", '
                                f'Data_admissao = "{data_admissao}", Data_hora_alteracao_do_registro = NOW(), '
                                f'CEP = "{cep}", ENDERECO = "{endereco}", BAIRRO = "{bairro}", CIDADE = "{cidade}" WHERE id = {id_func}')

                # conexao_bd2.commit()
            cursor2.execute('select * from funcionarios_fabrica')
            dados1 = cursor2.fetchall()
            for linha in dados1:
                print(linha)

        except Exception as e:
            print(f'Erro: {e}')

# Encerrando conexão com BDs
if conexao_bd1.is_connected():
    cursor1.close()
    conexao_bd1.close()
    print('Conexão BD01 encerrada!')

if conexao_bd2.is_connected():
    cursor2.close()
    conexao_bd2.close()
    print('Conexão BD02 encerrada!')


