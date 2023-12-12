import random
from itertools import zip_longest

from models import Aluno, DataNascimento


def verificar_data_nascimento(dia, mes, ano):
  dias_no_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

  if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
    dias_no_mes[1] = 29

  return 1 <= mes <= 12 and 1 <= dia <= dias_no_mes[mes - 1]


def verificar_sexo(sexo):
  return sexo.upper() in ['M', 'F']


def gerar_matricula():
  return f"20{random.randint(10000, 99999)}"


def validar_cpf(cpf):
  cpf_numeros = [int(digit) for digit in cpf if digit.isdigit()]

  if len(cpf_numeros) != 11:
    return False

  soma_produtos = sum(
      a * b
      for a, b in zip_longest(cpf_numeros[:9], range(10, 1, -1), fillvalue=0)
  )
  primeiro_dv = (soma_produtos * 10) % 11 % 10

  soma_produtos1 = sum(
      a * b
      for a, b in zip_longest(cpf_numeros[:10], range(11, 1, -1), fillvalue=0)
  )
  segundo_dv = (soma_produtos1 * 10) % 11 % 10

  return primeiro_dv == cpf_numeros[9] and segundo_dv == cpf_numeros[10]


def verificar_cpf_unico(cpf, lista_alunos):
  cpf = ''.join(filter(str.isdigit, cpf))

  if not validar_cpf(cpf):
    print("CPF inválido.")
    return False

  if any(aluno.cpf == cpf for aluno in lista_alunos):
    print("CPF já cadastrado para outro aluno.")
    return False

  return True


def verificar_nome(nome):
  return isinstance(nome, str) and nome.strip() != "" and all(
      c.isalpha() or c.isspace() for c in nome)
