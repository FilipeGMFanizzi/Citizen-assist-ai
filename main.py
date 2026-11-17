import os
from base_conhecimento import BaseConhecimento
from assistente import Assistente


def mostrar_menu():
    print("")
    print("Menu principal")
    print("1 - Fazer uma pergunta")
    print("2 - Navegar por categorias")
    print("3 - Ver indicadores")
    print("4 - Exportar atendimentos para CSV")
    print("0 - Sair")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Não foi possível iniciar sem a base de conhecimento.")
        return

    assistente = Assistente("Citizen Assist AI", base)

    print("=== " + assistente.nome + " ===")
    print("Orientações para jovens no primeiro emprego.")
    print("Aviso: este assistente NÃO é um canal oficial.")
    print("Nunca digite CPF, telefone ou e-mail.")

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.pedir_nota()
            print("")
            print("Obrigado por usar o " + assistente.nome + ". Até logo!")
            break
        else:
            print("Opção inválida. Digite um número do menu.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("")
        print("Programa encerrado.")
