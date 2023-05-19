import requests
from flask import Blueprint, jsonify, request, render_template, flash, url_for
from flask_login import login_required, logout_user, login_user, LoginManager
from werkzeug.utils import redirect
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
login_manager: LoginManager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from forms import FormCriarConta,FormLogin
from models.model import Cliente, db, Usuario

cliente_bp = Blueprint('cliente', __name__)

aluno_bp = Blueprint('aluno', __name__)

login_bp = Blueprint('', __name__)

@cliente_bp.route('/cliente', methods=['GET'])
def get_exemplo():
    clientes = Cliente.query.all()
    output =[]
    if clientes:
        for cliente in clientes:
            data = {}
            data['id'] = cliente.id
            data['nome'] = cliente.nome
            data['email'] = cliente.email
            data['status'] = cliente.status
            data['valor'] = cliente.valor
            data['forma_pagamento'] = cliente.forma_pagamento
            data['parcelas'] = cliente.parcelas
            output.append(data)
        return jsonify(output)
    return {'message': 'ITEM_NOT_FOUND'}, 404

@cliente_bp.route('/cliente/<id>', methods=['GET'])
def get_cliente_by_id(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'message': 'Exemplo não encontrado'})
    data = {}
    data['id'] = cliente.id
    data['nome'] = cliente.nome
    data['email'] = cliente.email
    data['status'] = cliente.status
    data['valor'] = cliente.valor
    data['forma_pagamento'] = cliente.forma_pagamento
    data['parcelas'] = cliente.parcelas
    return jsonify(data)

@cliente_bp.route('/cliente', methods=['POST'])
def add_cliente():
    nome = request.json['nome']
    email = request.json['email']
    status = request.json['status']
    valor = request.json['valor']
    forma_pagamento = request.json['forma_pagamento']
    parcelas = request.json['parcelas']

    cliente = Cliente(nome, email, status, valor, forma_pagamento, parcelas)
    db.session.add(cliente)
    db.session.commit()
    print(f'Liberar Acesso do email: {cliente.email}')
    return jsonify({'message': 'Exemplo adicionado com sucesso'})


@aluno_bp.route('/aluno')
def aluno():
    response = requests.get('http://localhost:5000/cliente')
    alunos = response.json()
    return render_template('usuarios.html', alunos=alunos)


@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario is not None and str(usuario.senha) == str(form_login.senha.data):
            Usuario.is_active = True
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect('/aluno')
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=form_criarconta.senha.data)
        db.session.add(usuario)
        db.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('login'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@login_bp.route('/sair')
def sair():
    return redirect(url_for('login'))
