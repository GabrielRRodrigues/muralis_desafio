from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

# Configuração do banco de dados
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'funcionarios'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicialização do objeto MySQL
mysql = MySQL(app)

# Habilita o CORS para permitir requisições de qualquer origem
CORS(app)


# Rota para listar todos os funcionários
@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM funcionarios_fabrica")
    rows = cur.fetchall()
    return jsonify(rows)


# Rota para retornar um funcionário por ID
@app.route('/funcionarios/<int:id>', methods=['GET'])
def buscar_funcionario(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM funcionarios_fabrica WHERE id={id}")
    row = cur.fetchone()
    return jsonify(row)


# Rota para cadastrar um novo funcionário
@app.route('/funcionarios', methods=['POST'])
def cadastrar_funcionario():
    nome = request.json['nome']
    rg = request.json['rg']
    cpf = request.json['cpf']
    data_admissao = request.json['data_admissao']
    cep = request.json['cep']
    endereco = request.json['endereco']
    bairro = request.json['bairro']
    cidade = request.json['cidade']

    cur = mysql.connection.cursor()
    cur.execute(
        f"INSERT INTO funcionarios_fabrica (nome, rg, cpf, data_admissao, cep, endereco, bairro, cidade) VALUES ('{nome}', '{rg}', '{cpf}', '{data_admissao}', '{cep}', '{endereco}', '{bairro}', '{cidade}')")
    mysql.connection.commit()

    return jsonify({'mensagem': 'Funcionário cadastrado com sucesso!'})


# Rota para atualizar um funcionário por ID
@app.route('/funcionarios/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    nome = request.json['nome']
    rg = request.json['rg']
    cpf = request.json['cpf']
    data_admissao = request.json['data_admissao']
    cep = request.json['cep']
    endereco = request.json['endereco']
    bairro = request.json['bairro']
    cidade = request.json['cidade']

    cur = mysql.connection.cursor()
    cur.execute(
        f"UPDATE funcionarios_fabrica SET nome='{nome}', rg='{rg}', cpf='{cpf}', data_admissao='{data_admissao}', cep='{cep}', endereco='{endereco}', bairro='{bairro}', cidade='{cidade}' WHERE id={id}")
    mysql.connection.commit()

    return jsonify({'mensagem': 'Funcionário atualizado com sucesso!'})


# Rota para deletar um funcionário por ID
@app.route('/funcionarios/<int:id>', methods=['DELETE'])
def deletar_funcionario(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM funcionarios_fabrica WHERE id={id}")
    mysql.connection.commit()

    return jsonify({'mensagem': 'Funcionário deletado com sucesso!'})

# Rota para deletar todos os funcionários
