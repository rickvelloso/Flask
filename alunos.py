from flask import Blueprint, redirect, render_template, request, url_for

from auxiliares import (
    gerar_matricula,
    validar_cpf,
    verificar_cpf_unico,
    verificar_nome,
    verificar_sexo,
)
from database import db
from models import Aluno, DataNascimento

bp_alunos = Blueprint("alunos", __name__, template_folder="templates")


@bp_alunos.route('/menu')
def menu():
    return render_template('menu.html')

@bp_alunos.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('alunos_create.html')
  elif request.method == 'POST':
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    dia_str = request.form.get('dia')
    mes_str = request.form.get('mes')
    ano_str = request.form.get('ano')
    sexo = request.form.get('sexo')
    if dia_str is not None and mes_str is not None and ano_str is not None:
      try:
          dia = int(dia_str)
          mes = int(mes_str)
          ano = int(ano_str)
      except ValueError:
          return "Erro ao converter para int"

    else:
      return "Um ou mais valores são None"

    if not verificar_nome(nome) or not verificar_cpf_unico(
        cpf, Aluno.query.all()):
      return 'Erro ao cadastrar aluno. Verifique os dados.'

    data_nascimento = DataNascimento(dia=dia, mes=mes, ano=ano)
    aluno = Aluno(nome=nome,
                  cpf=cpf,
                  matricula=gerar_matricula(),
                  data_nascimento=data_nascimento,
                  sexo=sexo)

    db.session.add(data_nascimento)
    db.session.add(aluno)
    db.session.commit()

    return redirect('recovery')

  return 'Método não suportado.'


@bp_alunos.route('/recovery')
def recovery():
  alunos = Aluno.query.all()
  return render_template('alunos_recovery.html', alunos=alunos)


@bp_alunos.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    aluno = Aluno.query.get(id)

    if aluno is None:
        return 'Aluno não encontrado.'

    if request.method == 'GET':
        return render_template('alunos_update.html', aluno=aluno)

    elif request.method == 'POST':
        novo_nome = request.form.get('novo_nome')
        novo_cpf = request.form.get('novo_cpf')
        novo_dia_str = request.form.get('novo_dia')
        novo_mes_str = request.form.get('novo_mes')
        novo_ano_str = request.form.get('novo_ano')
        novo_sexo = request.form.get('novo_sexo')

        if (
          novo_dia_str is not None
          and novo_mes_str is not None 
          and novo_ano_str is not None
        ):
            try:
                novo_dia = int(novo_dia_str)
                novo_mes = int(novo_mes_str)
                novo_ano = int(novo_ano_str)
            except ValueError:
                return "Erro ao converter para int para novas informações de data de nascimento"
        else:
            return "Um ou mais valores de data de nascimento são None"

        nova_data_nascimento = DataNascimento(dia=novo_dia,
                                              mes=novo_mes,
                                              ano=novo_ano)

        if not verificar_nome(novo_nome):
            return 'Erro: Nome inválido.'

        if not verificar_cpf_unico(novo_cpf, Aluno.query.filter(Aluno.id != id).all()):
            return 'Erro: CPF já cadastrado para outro aluno.'

        aluno.nome = novo_nome
        aluno.cpf = novo_cpf
        aluno.data_nascimento = nova_data_nascimento
        aluno.sexo = novo_sexo

        db.session.commit()

        return redirect(url_for('alunos.recovery'))

    return 'Método não suportado.'




@bp_alunos.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
  aluno = Aluno.query.get(id)

  if aluno is None:
    return 'Aluno não encontrado.'

  if request.method == 'GET':
    return render_template('alunos_delete.html', aluno=aluno)

  elif request.method == 'POST':
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('alunos.recovery'))

  return 'Método não suportado.'
