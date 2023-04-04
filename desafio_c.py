import mysql.connector
import requests

# Conexão com os BD
def conectar():
    try:
        global conexao_bd1, conexao_bd2
        conexao_bd1 = mysql.connector.connect(host='localhost', database= 'bd01', user= 'root', password='G1935@@_sr')
        conexao_bd2 = mysql.connector.connect(host='localhost', database= 'bd02', user= 'root', password='G1935@@_sr')
    except mysql.connector.Error as e:
        print(f'Erro de conexão com o BD: {e}')
        raise
try:
    conectar()
    cursor1 = conexao_bd1.cursor()

    # Recuperando dados de interesse da tabela funcionarios
    cursor1.execute('SELECT ID, RG, CPF, Data_admissao, CEP FROM funcionarios ')
    dados = cursor1.fetchall()

    cursor2 = conexao_bd2.cursor()

    for funcionario in dados:
        # Armazenando dados recuperados para uso
        id_func = funcionario[0]
        rg = funcionario[1]
        cpf = funcionario[2]
        data_admissao = funcionario[3]
        cep = funcionario[4]

        try:
            # Requisição via API
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            response.raise_for_status()

            dados_endereco = response.json()
            endereco = dados_endereco['logradouro']
            bairro = dados_endereco['bairro']
            cidade = dados_endereco['localidade']
        except requests.exceptions.RequestException as e:
            print(f'Erro ao consultar CEP {cep}: {e}')
            continue

        try:
            # Atualizando dados na tabela funcionarios_fabrica
            cursor2.execute(f'UPDATE funcionarios_fabrica SET RG = "{rg}", CPF = "{cpf}", Data_admissao = "{data_admissao}", '
                            f'Data_hora_alteracao_do_registro = NOW(), CEP = "{cep}", ENDERECO = "{endereco}", '
                            f'BAIRRO = "{bairro}", CIDADE = "{cidade}" WHERE id = {id_func}')
            # conexao_bd2.commit()
        except mysql.connector.Error as e:
            print(f'Erro ao atualizar dados do funcionário {id_func} no BD: {e}')
            continue

    cursor2.execute('select * from funcionarios_fabrica')
    dados1 = cursor2.fetchall()
    for linha in dados1:
        print(linha)

except mysql.connector.Error as e:
    print(f'Erro ao conectar no BD: {e}')

# Encerrando conexão com BDs
finally:
    cursor1.close()
    conexao_bd1.close()
    print('Conexão com BD01 encerrada com sucesso!')

    cursor2.close()
    conexao_bd2.close()
    print('Conexão com BD02 encerrada com sucesso!')