import json
import csv
import time
from datetime import datetime

CAMPOS = ["data", "sessao", "origem", "pergunta", "id_orientacao",
          "encontrou", "ajudou", "tentativas", "tempo", "nota"]


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.caminho_historico = "data/historico.json"
        self.caminho_csv = "data/atendimentos.csv"
        self.sessao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.carregar_historico()

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            print("Aviso: o arquivo " + self.caminho_historico + " está corrompido. Começando um histórico novo.")
            return
        except OSError:
            print("Aviso: não foi possível abrir o histórico.")
            return

        if type(dados) != list:
            print("Aviso: o histórico está em um formato inesperado. Começando um histórico novo.")
            return

        for item in dados:
            if type(item) == dict:
                completo = True
                for campo in CAMPOS:
                    if campo not in item:
                        completo = False
                if completo:
                    self.historico.append(item)

    def salvar_historico(self):
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar o histórico.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo):
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sessao": self.sessao,
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo": tempo,
            "nota": None
        }
        self.historico.append(atendimento)
        self.salvar_historico()

    def tem_dado_pessoal(self, texto):
        if "@" in texto:
            return True
        digitos = 0
        for letra in texto:
            if letra.isdigit():
                digitos = digitos + 1
        return digitos >= 8

    def pedir_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta == "s":
                return True
            if resposta == "n":
                return False
            print("Resposta inválida. Digite s para sim ou n para não.")

    def ler_numero(self, texto, maximo):
        if texto.isdigit():
            numero = int(texto)
            if numero >= 0 and numero <= maximo:
                return numero
        return None

    def mostrar_resultado(self, resultados):
        melhor_pontos = resultados[0][0]
        melhor = resultados[0][1]
        if melhor_pontos >= 6:
            confianca = "ALTA"
        else:
            confianca = "MÉDIA"

        print("")
        print("Confiança da resposta: " + confianca + " (" + str(melhor_pontos) + " pontos)")
        print("")
        melhor.exibir()

        alternativas = []
        for i in range(1, len(resultados)):
            if len(alternativas) < 2 and resultados[i][0] >= 3:
                alternativas.append(resultados[i])

        if len(alternativas) > 0:
            print("")
            print("Outras orientações que podem ajudar:")
            for pontos, orientacao in alternativas:
                print("  - " + orientacao.titulo + " (" + str(pontos) + " pontos)")

    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""

        while True:
            print("")
            texto = input("Digite sua dúvida (0 para voltar): ").strip()

            if texto == "0":
                if tentativas > 0:
                    tempo = round(time.time() - inicio, 1)
                    self.registrar("pergunta", ultima_pergunta, None, False, False, tentativas, tempo)
                return

            if texto == "":
                print("Atenção: você não digitou nada. Tente de novo.")
            elif self.tem_dado_pessoal(texto):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
            else:
                tentativas = tentativas + 1
                ultima_pergunta = texto
                resultados = self.base.buscar(texto)

                if len(resultados) == 0 or resultados[0][0] < 3:
                    print("")
                    print("Não encontrei uma orientação para essa dúvida.")
                    print("Tente usar outras palavras ou escolha uma categoria no menu.")
                    print("Categorias disponíveis: " + ", ".join(self.base.categorias()))
                    tempo = round(time.time() - inicio, 1)
                    self.registrar("pergunta", texto, None, False, False, 1, tempo)
                    inicio = time.time()
                    tentativas = 0
                    ultima_pergunta = ""
                else:
                    tempo = round(time.time() - inicio, 1)
                    self.mostrar_resultado(resultados)
                    print("")
                    ajudou = self.pedir_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                    self.registrar("pergunta", texto, resultados[0][1].id, True, ajudou, tentativas, tempo)
                    inicio = time.time()
                    tentativas = 0
                    ultima_pergunta = ""

    def navegar(self):
        categorias = self.base.categorias()
        while True:
            print("")
            print("Categorias:")
            for i in range(len(categorias)):
                print(str(i + 1) + " - " + categorias[i])
            print("0 - Voltar")
            opcao = input("Escolha uma categoria: ").strip()
            numero = self.ler_numero(opcao, len(categorias))

            if numero == 0:
                return
            elif numero is None:
                print("Opção inválida. Digite um número da lista.")
            else:
                self.navegar_categoria(categorias[numero - 1])

    def navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            inicio = time.time()
            print("")
            print("Categoria: " + categoria)
            for i in range(len(orientacoes)):
                print(str(i + 1) + " - " + orientacoes[i].titulo)
            print("0 - Voltar")
            opcao = input("Escolha uma orientação: ").strip()
            numero = self.ler_numero(opcao, len(orientacoes))

            if numero == 0:
                return
            elif numero is None:
                print("Opção inválida. Digite um número da lista.")
            else:
                tempo = round(time.time() - inicio, 1)
                orientacao = orientacoes[numero - 1]
                print("")
                orientacao.exibir()
                print("")
                ajudou = self.pedir_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", "categoria: " + categoria, orientacao.id, True, ajudou, 1, tempo)

    def indicadores(self):
        print("")
        print("Indicadores")
        total = len(self.historico)
        if total == 0:
            print("Ainda não há atendimentos registrados.")
            return

        encontradas = 0
        ajudaram = 0
        soma_tempo = 0
        soma_tentativas = 0
        notas = {}
        sem_solucao = []

        for atendimento in self.historico:
            if atendimento["encontrou"]:
                encontradas = encontradas + 1
                soma_tempo = soma_tempo + atendimento["tempo"]
            if atendimento["ajudou"]:
                ajudaram = ajudaram + 1
            else:
                sem_solucao.append(atendimento["pergunta"])
            soma_tentativas = soma_tentativas + atendimento["tentativas"]
            if atendimento["nota"] is not None:
                notas[atendimento["sessao"]] = atendimento["nota"]

        print("Total de atendimentos: " + str(total))
        print("Resposta encontrada: " + str(round(encontradas / total * 100, 1)) + "%")
        print("Taxa de acerto (ajudou): " + str(round(ajudaram / total * 100, 1)) + "%")

        if encontradas > 0:
            print("Tempo médio para encontrar: " + str(round(soma_tempo / encontradas, 1)) + " segundos")
        else:
            print("Tempo médio para encontrar: sem dados")

        print("Tentativas por atendimento: " + str(round(soma_tentativas / total, 1)))

        if len(notas) > 0:
            soma_notas = 0
            for nota in notas.values():
                soma_notas = soma_notas + nota
            print("Facilidade de uso (1 a 5): " + str(round(soma_notas / len(notas), 1)))
        else:
            print("Facilidade de uso (1 a 5): ainda sem notas")

        print("Dúvidas sem solução:")
        if len(sem_solucao) == 0:
            print("  nenhuma")
        else:
            for duvida in sem_solucao:
                print("  - " + duvida)

    def pedir_nota(self):
        teve_atendimento = False
        for atendimento in self.historico:
            if atendimento["sessao"] == self.sessao:
                teve_atendimento = True

        if not teve_atendimento:
            return

        print("")
        while True:
            nota = input("De 1 a 5, qual foi a facilidade de usar o assistente? ").strip()
            if nota in ["1", "2", "3", "4", "5"]:
                break
            print("Nota inválida. Digite um número de 1 a 5.")

        for atendimento in self.historico:
            if atendimento["sessao"] == self.sessao:
                atendimento["nota"] = int(nota)
        self.salvar_historico()

    def exportar_csv(self):
        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow(atendimento)
            print("")
            print("Atendimentos exportados para " + self.caminho_csv)
        except OSError:
            print("Aviso: não foi possível salvar o arquivo " + self.caminho_csv + ".")
