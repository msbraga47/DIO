from datetime import datetime

saldo = 0.0
extrato = []
limite_saque = 500.00
saques_realizados = 0
transacoes_realizadas = 0
LIMITE_SAQUES = 3
LIMITE_TRANSACOES = 10

def menu():
    print("\n====== BANCO PY ======")
    print("[1] Depositar")
    print("[2] Sacar")
    print("[3] Extrato")
    print("[0] Sair")
    return input("Escolha uma opção: ")

def transacao_permitida():
    global transacoes_realizadas
    if transacoes_realizadas >= LIMITE_TRANSACOES:
        print("Limite de transações diárias atingido.")
        return False
    return True

def registrar_transacao(tipo, valor):
    global extrato, transacoes_realizadas
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    extrato.append(f"{timestamp} - {tipo}: R$ {valor:.2f}")
    transacoes_realizadas += 1

def depositar(valor):
    global saldo
    if not transacao_permitida():
        return
    if valor > 0:
        saldo += valor
        registrar_transacao("Depósito", valor)
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor de depósito inválido.")

def sacar(valor):
    global saldo, saques_realizados
    if not transacao_permitida():
        return
    if saques_realizados >= LIMITE_SAQUES:
        print("Limite diário de saques atingido.")
    elif valor > limite_saque:
        print(f"Limite por saque é de R$ {limite_saque:.2f}")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif valor > 0:
        saldo -= valor
        saques_realizados += 1
        registrar_transacao("Saque", valor)
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor de saque inválido.")

def mostrar_extrato():
    print("\n====== EXTRATO ======")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimento in extrato:
            print(movimento)
    print(f"Saldo atual: R$ {saldo:.2f}")

# Loop principal
while True:
    opcao = menu()

    if opcao == "1":
        try:
            valor = float(input("Valor do depósito: R$ "))
            depositar(valor)
        except ValueError:
            print("Entrada inválida. Digite um número.")
    elif opcao == "2":
        try:
            valor = float(input("Valor do saque: R$ "))
            sacar(valor)
        except ValueError:
            print("Entrada inválida. Digite um número.")
    elif opcao == "3":
        mostrar_extrato()
    elif opcao == "0":
        print("Saindo... Obrigado por usar o Banco Py!")
        break
    else:
        print("Opção inválida.")
