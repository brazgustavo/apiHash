from flask import Flask
from models.model import db
from routes.route import cliente_bp,aluno_bp,login_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres://ptqcufynekqnis:e6be8555f05656726f626cce0e87afe37ba8e5f9d5d399ec2e678eeec538f760@ec2-54-234-13-16.compute-1.amazonaws.com:5432/d2p2bohhvlddfq'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '29cecf8afd6176f06bb3f55472d490d1'

db.init_app(app)
app.register_blueprint(cliente_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(login_bp)
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
