import datetime


class Account:
    def __init__(self, nome, saldo=0):
        self.nome = nome
        self.saldo = saldo
        self.horario = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.historico = []  # lista de transações
        self.person = {
            'nome': self.nome,
            'saldo': self.saldo,
            'horario': self.horario
        }

    def depositar(self, valor, origem="Não informado"):
        self.saldo += valor
        self.person['saldo'] = self.saldo
        self.historico.append({
            'tipo': 'Depósito',
            'valor': valor,
            'origem': origem,
            'horario': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    def sacar(self, valor, destino="Não informado"):
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return
        self.saldo -= valor
        self.person['saldo'] = self.saldo
        self.historico.append({
            'tipo': 'Saque',
            'valor': valor,
            'origem': destino,
            'horario': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    def valor(self):
        return self.saldo


# --- Utilitários ---

def linha(txt=''):
    print("=" * 62)
    if txt:
        print(txt.center(60))
        print("=" * 62)

def pegar_valor(prompt):
    while True:
        try:
            entrada = input(prompt).replace(",", ".")
            valor = float(entrada)
            if valor <= 0:
                print("Digite um valor maior que zero.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Use números (ex: 150 ou 150,00).")


# --- Menu principal ---

def iniciar():
    linha(f"BEM-VINDO")

    nome = input("Nome do titular: ").strip()
    while not nome:
        print("Nome não pode ser vazio.")
        nome = input("Nome do titular: ").strip()

    saldo_inicial = pegar_valor("Saldo inicial: R$ ")
    conta = Account(nome, saldo_inicial)

    while True:
        linha(f"Olá, {conta.nome}")
        print(f"  Saldo: R$ {conta.valor():.2f}")
        print()
        print("  [1] Depositar", end= " ")
        print("  [2] Sacar")
        print("  [3] Ver saldo", end= " ")
        print("  [4] Histórico")
        print("  [5] Dados da conta", end= " ")
        print("  [0] Sair")
        print("=" * 62)

        opcao = input("Opção: ").strip()

        match opcao:
            case "1":
                valor = pegar_valor("Valor para depositar: R$ ")
                origem = input("Quem depositou? (pessoa/estabelecimento): ").strip()
                origem = origem if origem else "Não informado"
                conta.depositar(valor, origem)
                print(f"✔ Depósito de R$ {valor:.2f} de '{origem}' realizado.")

            case "2":
                valor = pegar_valor("Valor para sacar: R$ ")
                destino = input("Onde/para quem? (estabelecimento/pessoa): ").strip()
                destino = destino if destino else "Não informado"
                conta.sacar(valor, destino)

            case "3":
                print(f"  Saldo atual: R$ {conta.valor():.2f}")

            case "4":
                linha("HISTÓRICO")
                if not conta.historico:
                    print("  Nenhuma transação registrada.")
                else:
                    print(f"  {'#':<3} {'Tipo':<10} {'Valor':>10} {'Origem':<18} {'Horário'}")
                    print("  " + "-" * 62)
                    for i, t in enumerate(conta.historico, 1):
                        sinal = "+" if t['tipo'] == 'Depósito' else "-"
                        print(f"  {i:<3} {t['tipo']:<10} {sinal}R${t['valor']:>7.2f} {t['origem']:<18} {t['horario']}")
                print("=" * 62)

            case "5":
                linha("DADOS DA CONTA")
                print(f"  Titular : {conta.person['nome']}")
                print(f"  Saldo   : R$ {conta.person['saldo']:.2f}")
                print(f"  Criada  : {conta.person['horario']}")
                print("=" * 62)

            case "0":
                linha("ATÉ LOGO!")
                break

            case _:
                print("Opção inválida. Digite 0, 1, 2, 3, 4 ou 5.")


iniciar()