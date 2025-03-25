


# calculadora com funções
def soma(a, b):
    return a + b


def subtracao(a, b):
    return a - b


def multiplicacao(a, b):
    return a * b


def divisao(a, b):
    return a / b


input_a = int(input('Digite o primeiro número: '))
input_b = int(input('Digite o segundo número: '))
operacao = input('Digite a operação (+, -, *, /): ')

if operacao == '+':
    resultado = soma(input_a, input_b)
elif operacao == '-':
    resultado = subtracao(input_a, input_b)
elif operacao == '*':
    resultado = multiplicacao(input_a, input_b)
elif operacao == '/':
    resultado = divisao(input_a, input_b)
else:
    resultado = 'Operação inválida'


print(f'O resultado da operação é: {resultado}')