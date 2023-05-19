from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = "Cliente"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False, unique=False)
    email = db.Column(db.String(80), nullable=False, unique=False)
    status = db.Column(db.String(80), nullable=False, unique=False)
    valor = db.Column(db.Float(precision=2), nullable=False)
    forma_pagamento = db.Column(db.String(80), nullable=False, unique=False)
    parcelas = db.Column(db.Integer, nullable=False)

    def __init__(self, nome, email, status, valor, forma_pagamento, parcelas):
        self.nome = nome
        self.email = email
        self.status = status
        self.valor = valor
        self.forma_pagamento = forma_pagamento
        self.parcelas = parcelas

    def __repr__(self):
        return f'ClienteModel(nome={self.nome}, email={self.email}, status={self.status}, valor={self.valor},\
        forma_pagamento={self.forma_pagamento}, parcelas={self.parcelas})'

    def json(self):
        return {'nome': self.nome, 'email': self.email, 'status': self.status, 'valor': self.valor,'forma_pagamento': self.forma_pagamento, 'parcelas': self.parcelas}

    @classmethod
    def find_by_email(cls, email) -> "Cliente":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id) -> "Cliente":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Cliente"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()


class Usuario(db.Model):
    __tablename__ = "Usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)

    def __init__(self, username, email, senha):
        self.username = username
        self.email = email
        self.senha = senha


    def __repr__(self):
        return f'UsuarioModel(username={self.username}, email={self.email})'

    def json(self):
        return {'username': self.username, 'email': self.email, 'senha': self.senha}

    @classmethod
    def find_by_email(cls, email) -> "Usuario":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id) -> "Usuario":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Usuario"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def is_active(self):
        is_active = False
        return is_active