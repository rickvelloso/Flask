from flask import Flask, redirect, render_template, url_for
from flask_migrate import Migrate

from alunos import bp_alunos
from database import db
from models import Aluno, DataNascimento

app = Flask(__name__, static_folder='static')
conexao = "sqlite:///meubanco.sqlite"
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(bp_alunos, url_prefix='/alunos')

migrate = Migrate(app, db)

@app.route('/')
def index():
    return redirect(url_for('alunos.menu'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)