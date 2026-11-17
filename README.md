# Citizen Assist AI

Assistente de terminal em Python que orienta **jovens no primeiro emprego** sobre documentos e direitos básicos, usando apenas informações verificadas, sempre com fonte, data de verificação e aviso de que não é um canal oficial. Projeto da Global Solution 2026.2 (FIAP), desafio CitizenTech.

## Integrantes

| Nome | RM |
|------|----|
| Filipe Gunther | 571331 |
| Lucas Pinheiro | 573497 |
| Guilherme Guimarães | 572957 |

## Público e problema

**Público:** jovens de 14 a 24 anos que estão buscando o primeiro emprego.

**Problema:** as informações sobre carteira de trabalho digital, CPF, título de eleitor, alistamento militar e direitos do Jovem Aprendiz estão espalhadas em vários sites, em linguagem técnica e misturadas com páginas falsas que cobram por serviços gratuitos. O assistente reúne tudo em respostas curtas, em linguagem simples, com a fonte oficial.

## ODS relacionados

* **ODS 8** – Trabalho decente e crescimento econômico (acesso ao primeiro emprego e aos direitos do trabalhador)
* **ODS 10** – Redução das desigualdades (informação clara para quem tem menos acesso)
* **ODS 16** – Paz, justiça e instituições eficazes (acesso a serviços públicos e combate a golpes)

## Como executar

Só é preciso ter o Python 3 instalado. Não usa bibliotecas externas.

```
python main.py
```

Menu principal: 1) Fazer uma pergunta, 2) Navegar por categorias, 3) Ver indicadores, 4) Exportar atendimentos para CSV, 0) Sair (ao sair, pede a nota de facilidade de 1 a 5).

## Estrutura do repositório

```
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

## Classes (composição)

```
Assistente
 └── base: BaseConhecimento
      └── orientacoes: [Orientacao, Orientacao, ...]
```

* **Orientacao**: guarda os dados de um registro do JSON e exibe na tela (`exibir()`).
* **BaseConhecimento**: lê o JSON (`carregar()`), lista categorias (`categorias()`, `por_categoria()`) e busca (`pontuar()`, `buscar()`).
* **Assistente**: faz o atendimento (`perguntar()`, `navegar()`), guarda o histórico (`registrar()`), calcula os indicadores (`indicadores()`) e exporta o CSV (`exportar_csv()`).

## Regra de pontuação

Pergunta, palavras-chave e título são normalizados (minúsculas, sem acentos, sem pontuação) antes de comparar.

| Regra | Resultado |
|-------|-----------|
| Palavra-chave da orientação aparece na pergunta | +3 pontos |
| Palavra da pergunta (4 letras ou mais, fora da lista de palavras comuns) aparece no título | +1 ponto (cada palavra conta uma vez) |
| Melhor orientação com 6 pontos ou mais | Confiança ALTA |
| Melhor orientação com 3 a 5 pontos | Confiança MÉDIA |
| Nenhuma orientação com 3 pontos ou mais | "Não encontrei": sugere outras palavras e as categorias |

`buscar()` devolve uma lista de tuplas `(pontos, orientacao)` da maior para a menor pontuação. O assistente mostra a melhor e até duas alternativas com 3 pontos ou mais.

**Ajuste da equipe:** além do que o PDF sugere, a lista `PALAVRAS_COMUNS` ignora palavras como "como", "para" e "quero" na pontuação pelo título, e o `normalizar()` também troca `-` e `/` por espaço (para casar "gov.br" com "gov br").

Exemplo: em "Quero ser jovem aprendiz", a orientação 10 recebe +3 por `jovem aprendiz`, +3 por `ser jovem aprendiz`, +1 por "jovem" e +1 por "aprendiz" no título: **8 pontos, confiança ALTA**.

## Regras de atendimento

* Entradas inválidas (vazio, letras, número fora da faixa, s/n inválido) nunca encerram o programa.
* Pergunta com 8 ou mais dígitos ou com `@` é recusada e **não é registrada**.
* Toda resposta mostra fonte, data de verificação e o aviso "este assistente NÃO é um canal oficial".
* JSON ausente ou corrompido não trava o programa (mensagem de erro ou histórico novo).

## Histórico, indicadores e CSV

Cada atendimento é salvo em `data/historico.json` (data, sessão, origem, pergunta, id da orientação, encontrou, ajudou, tentativas, tempo em segundos e nota). A opção 3 do menu mostra: resposta encontrada (%), taxa de acerto (%), tempo médio para encontrar, tentativas por atendimento, facilidade de uso (1 a 5) e a lista de dúvidas sem solução. A opção 4 exporta tudo para `data/atendimentos.csv` com `csv.DictWriter`.

## Integrações com outras disciplinas

Nenhuma. (Se a equipe integrar algo, descreva aqui.)

## Fontes consultadas

* https://www.gov.br/pt-br/servicos/inscrever-no-cpf
* https://www.gov.br/pt-br/servicos
* https://www.tse.jus.br (Título Net, e-Título)
* https://alistamento.eb.mil.br/
* https://www.gov.br
* https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho
* https://www.gov.br/pt-br/servicos/buscar-emprego-no-sistema-nacional-de-emprego-sine
* https://www.gov.br/trabalho-e-emprego/pt-br
* https://www.caixa.gov.br/beneficios-trabalhador/fgts/
* https://www.caixa.gov.br/extrato-fgts

Todas as 14 orientações foram conferidas pela equipe em 14/11/2026 (campo `verificado_em`).

## Resultado do teste com usuários

**O teste com pessoas de fora da equipe não foi realizado.** O enunciado pede 3 pessoas e 10 atendimentos, mas a equipe não conseguiu aplicar o teste no prazo. Para demonstrar o funcionamento do histórico, dos indicadores e do CSV, os arquivos em `data/` contêm atendimentos feitos **pelos próprios integrantes**. Esses números não representam o uso por pessoas reais.

Indicadores do uso da equipe (opção 3 do menu):

| Indicador | Resultado |
|-----------|-----------|
| Total de atendimentos | 10 |
| Resposta encontrada (%) | 80,0% |
| Taxa de acerto (%) | 70,0% |
| Tempo médio para encontrar (s) | 6,6 |
| Tentativas por atendimento | 1,0 |
| Facilidade de uso (1 a 5) | 5,0 (uma sessão, nota dada por um integrante) |

**Dúvidas sem solução:**

* "Como consultar meu FGTS?" (a orientação 13 foi encontrada, mas o integrante marcou que não respondeu a dúvida)
* "preciso de emprego"
* "quanto ganha um aprendiz"

**Melhoria feita a partir dos testes da equipe:** a pergunta "preciso de emprego" não era encontrada (só 1 ponto). A palavra-chave `emprego` foi adicionada à orientação 9 (vagas de emprego no Sine), e a pergunta passou a ser encontrada.

## Limitações

* A busca é por regras: só entende palavras-chave que estão no JSON, não interpreta sentido nem erros de digitação.
* Não foi testado com usuários reais (ver seção acima), então a cobertura de palavras-chave pode deixar de fora formas de perguntar que a equipe não previu.
* Responde apenas os 14 temas da base; dúvidas fora dela ficam sem resposta.
* Os requisitos e os prazos dos serviços públicos podem mudar; por isso cada resposta mostra a data de verificação.
* Não é um canal oficial e não substitui o atendimento dos órgãos públicos.

## Vídeo técnico

Link (YouTube, não listado): PREENCHER
