from abc import ABC, abstractmethod
from datetime import datetime

# Interface
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        print("Saque inválido ou saldo insuficiente.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        print("Valor de depósito inválido.")
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if valor > self.limite:
            print("Valor excede o limite de saque.")
            return False
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques diário atingido.")
            return False
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False

# ---------------------- MENU E OPERAÇÕES ----------------------

def menu():
    return input("""
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo usuário
[c] Nova conta
[l] Listar contas
[q] Sair
=> """)

def encontrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def criar_usuario(usuarios):
    cpf = input("CPF (somente números): ")
    if encontrar_usuario(cpf, usuarios):
        print("Usuário já existe.")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro, cidade/UF): ")

    novo_usuario = Cliente(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")

def criar_conta(numero_conta, usuarios, contas):
    cpf = input("CPF do usuário: ")
    usuario = encontrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado.")
        return

    conta = ContaCorrente(usuario, numero_conta)
    usuario.adicionar_conta(conta)
    contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print(f"Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {conta.cliente.nome}")

# ---------------------- EXECUÇÃO PRINCIPAL ----------------------

usuarios = []
contas = []
contador_conta = 1

while True:
    opcao = menu()

    if opcao == "d":
        cpf = input("CPF do cliente: ")
        usuario = encontrar_usuario(cpf, usuarios)
        if not usuario or not usuario.contas:
            print("Cliente não encontrado ou sem conta.")
            continue

        valor = float(input("Valor do depósito: "))
        transacao = Deposito(valor)
        usuario.realizar_transacao(usuario.contas[0], transacao)

    elif opcao == "s":
        cpf = input("CPF do cliente: ")
        usuario = encontrar_usuario(cpf, usuarios)
        if not usuario or not usuario.contas:
            print("Cliente não encontrado ou sem conta.")
            continue

        valor = float(input("Valor do saque: "))
        transacao = Saque(valor)
        usuario.realizar_transacao(usuario.contas[0], transacao)

    elif opcao == "e":
        cpf = input("CPF do cliente: ")
        usuario = encontrar_usuario(cpf, usuarios)
        if not usuario or not usuario.contas:
            print("Cliente não encontrado ou sem conta.")
            continue

        conta = usuario.contas[0]
        print("\n====== EXTRATO ======")
        if not conta.historico.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for t in conta.historico.transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
        print(f"Saldo atual: R$ {conta.saldo:.2f}")
        print("=======================")

    elif opcao == "u":
        criar_usuario(usuarios)

    elif opcao == "c":
        criar_conta(contador_conta, usuarios, contas)
        contador_conta += 1

    elif opcao == "l":
        listar_contas(contas)

    elif opcao == "q":
        print("Saindo...")
        break

    else:
        print("Opção inválida.")
