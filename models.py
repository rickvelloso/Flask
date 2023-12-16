from database import db


class DataNascimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)

class Aluno(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(80), nullable=False)
  cpf = db.Column(db.String(11), nullable=False, unique=True)
  matricula = db.Column(db.String(10), nullable=False, unique=True)
  data_nascimento_id = db.Column(
      db.Integer,
      db.ForeignKey('data_nascimento.id'),
      nullable=False
  )
  sexo = db.Column(db.String(1), nullable=False)
  ativo = db.Column(db.Boolean, default=True)

  data_nascimento = db.relationship('DataNascimento', backref='aluno')

  def exibir_informacoes(self):
    return (
        f"Nome: {self.nome}\n"
        f"CPF: {self.cpf}\n"
        f"Matrícula: {self.matricula}\n"
        f"Data de Nascimento: "
        f"{self.data_nascimento.dia}/{self.data_nascimento.mes}/{self.data_nascimento.ano}\n"
        f"Sexo: {self.sexo}\n"
        f"Ativo: {'Sim' if self.ativo else 'Não'}"
    )
class Professor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(80), nullable=False)
  cpf = db.Column(db.String(11), nullable=False, unique=True)
  matricula = db.Column(db.String(10), nullable=False, unique=True)
  data_nascimento_id = db.Column(
      db.Integer,
      db.ForeignKey('data_nascimento.id'),
      nullable=False
  )
  sexo = db.Column(db.String(1), nullable=False)
  ativo = db.Column(db.Boolean, default=True)

  data_nascimento = db.relationship('DataNascimento', backref='professor')

  def exibir_informacoes(self):
      return (
          f"Nome: {self.nome}\n"
          f"CPF: {self.cpf}\n"
          f"Matrícula: {self.matricula}\n"
          f"Data de Nascimento: "
          f"{self.data_nascimento.dia}/{self.data_nascimento.mes}/{self.data_nascimento.ano}\n"
          f"Sexo: {self.sexo}\n"
          f"Ativo: {'Sim' if self.ativo else 'Não'}"
      )
