saldo = 0.0
extrato = []
limite_saque = 500.00
saques_realizados = 0
LIMITE_SAQUES = 3

def menu():
    print("\n====== BANCO PY ======")
    print("[1] Depositar")
    print("[2] Sacar")
    print("[3] Extrato")
    print("[0] Sair")
    return input("Escolha uma opção: ")

def depositar(valor):
    global saldo
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Valor de depósito inválido.")

def sacar(valor):
    global saldo, saques_realizados
    if saques_realizados >= LIMITE_SAQUES:
        print("Limite diário de saques atingido.")
    elif valor > limite_saque:
        print(f"Limite por saque é de R$ {limite_saque:.2f}")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif valor > 0:
        saldo -= valor
        saques_realizados += 1
        extrato.append(f"Saque: R$ {valor:.2f}")
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
