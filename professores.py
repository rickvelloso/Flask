from flask import Blueprint, redirect, render_template, request, url_for

from auxiliares import gerar_matricula, validar_cpf, verificar_cpf_unico, verificar_nome
from database import db
from models import DataNascimento, Professor

bp_professores = Blueprint("professores", __name__, template_folder="templates")

@bp_professores.route('/menu')
def menu():
    return render_template('menu_professores.html')

@bp_professores.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('professores_create.html')
    elif request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        dia_str = request.form.get('dia')
        mes_str = request.form.get('mes')
        ano_str = request.form.get('ano')
        sexo = request.form.get('sexo')

        # Validações e conversões de data aqui

        if dia_str is not None and mes_str is not None and ano_str is not None:
          try:
            dia = int(dia_str)
            mes = int(mes_str)
            ano = int(ano_str)
          except ValueError:
            return "Erro ao converter para int"

        else:
          return "Um ou mais valores são None"

      # Validação do nome
        nome_valido = verificar_nome(nome)

      # Validação do CPF único
        cpf_unico = verificar_cpf_unico(cpf, Professor.query.all())

      # Verificação combinada
        if not (nome_valido and cpf_unico):
          return 'Erro ao cadastrar professor. Verifique os dados.'

        data_nascimento = DataNascimento(dia=dia, mes=mes, ano=ano)
        professor = Professor(nome=nome,
                              cpf=cpf,
                              matricula=gerar_matricula(),
                              data_nascimento=data_nascimento,
                              sexo=sexo)

        db.session.add(data_nascimento)
        db.session.add(professor)
        db.session.commit()

        return redirect('recovery')

    return 'Método não suportado.'



@bp_professores.route('/recovery')
def recovery():
    professores = Professor.query.all()
    return render_template('professores_recovery.html', professores=professores)


@bp_professores.route('/update/<int:id>', methods=['GET', 'POST'])
def update_professor(id):
    professor = Professor.query.get(id)

    if professor is None:
        return 'Professor não encontrado.'

    if request.method == 'GET':
        return render_template('professores_update.html', professor=professor)

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
                return "Erro ao converter para int para novas informações de data"
        else:
            return "Um ou mais valores de data de nascimento são None"

        nova_data_nascimento = DataNascimento(dia=novo_dia,
                                              mes=novo_mes,
                                              ano=novo_ano)

        if not verificar_nome(novo_nome):
            return 'Erro: Nome inválido.'

        if not verificar_cpf_unico(novo_cpf, Professor.query.filter(Professor.id != id).all()):
            return 'Erro: CPF já cadastrado para outro professor.'

        professor.nome = novo_nome
        professor.cpf = novo_cpf
        professor.data_nascimento = nova_data_nascimento
        professor.sexo = novo_sexo

        db.session.commit()

        return redirect(url_for('professores.recovery'))

    return 'Método não suportado.'


@bp_professores.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_professor(id):
    professor = Professor.query.get(id)

    if professor is None:
        return 'Professor não encontrado.'

    if request.method == 'GET':
        return render_template('professores_delete.html', professor=professor)

    elif request.method == 'POST':
        db.session.delete(professor)
        db.session.commit()
        return redirect(url_for('professores.recovery'))

    return 'Método não suportado.'
