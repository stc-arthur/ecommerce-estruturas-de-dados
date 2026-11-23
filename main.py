"""
Projeto Final - Teoria das Estruturas de Dados
Tema 2: Plataforma de Comércio Eletrônico

Estruturas de dados e o papel de cada uma no sistema:
  - Lista  (list)              -> catálogo de produtos
  - Fila   (collections.deque) -> processamento de pagamentos (FIFO)
  - Pilha  (list)              -> histórico de ações do carrinho (LIFO)
  - Árvore (dict aninhado)     -> departamentos > categorias > subcategorias

Persistência: um único arquivo texto (dados_sistema.txt), uma linha por registro,
campos separados por "|" e a primeira palavra da linha indica a estrutura.
"""

import math
import os
from collections import deque

# ----------------------------------------------------------------------------
# CONSTANTES E ESTRUTURAS EM MEMÓRIA (o sistema começa 100% vazio)
# ----------------------------------------------------------------------------
ARQUIVO = "dados_sistema.txt"
NIVEIS = ["Departamento", "Categoria", "Subcategoria"]  # nome de cada nível da árvore
MAX_NIVEIS = len(NIVEIS)                                 # a árvore tem no máximo 3 níveis
STATUS_FILA = ["Aguardando", "Em análise"]               # status possíveis enquanto o pedido espera

produtos = []                # LISTA: cada produto é um dicionário {id, nome, preco, estoque}
fila_pagamentos = deque()    # FILA: entra no fim (append), sai do início (popleft)
pilha_acoes = []             # PILHA: o topo é o ÚLTIMO elemento da lista (append / pop)
arvore = {}                  # ÁRVORE: dicionários aninhados; folha = dicionário vazio {}
contadores = {"pedido": 0, "acao": 0}  # usados para gerar IDs como PED-01 e ACAO-01


# ----------------------------------------------------------------------------
# FUNÇÕES AUXILIARES DE ENTRADA (validam o que o usuário digita)
# ----------------------------------------------------------------------------
def ler_texto(mensagem, proibidos="|"):
    """Lê um texto não vazio. Recusa os caracteres proibidos (o '|' separa campos no TXT)."""
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print("  Valor vazio. Tente novamente.")
        elif any(caractere in texto for caractere in proibidos):
            print("  Não use estes caracteres: " + " ".join(proibidos))
        else:
            return texto


def ler_inteiro(mensagem, minimo=0):
    """Lê um número inteiro maior ou igual a 'minimo'. Repete até o usuário acertar."""
    while True:
        try:
            valor = int(input(mensagem).strip())
        except ValueError:
            print("  Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"  O valor mínimo é {minimo}.")
        else:
            return valor


def ler_preco(mensagem):
    """Lê um valor em reais (aceita vírgula ou ponto) que não seja negativo."""
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
        except ValueError:
            print("  Digite um valor numérico (ex: 250.00).")
            continue
        if not math.isfinite(valor) or valor < 0:
            print("  Digite um valor válido e não negativo.")
        else:
            return valor


def confirmar(pergunta):
    """Pergunta s/n e devolve True somente se o usuário digitar 's'."""
    return input(f"{pergunta} (s/n): ").strip().lower() == "s"


def proximo_id(chave, prefixo):
    """Gera IDs sequenciais para pedidos e ações. Exemplo: PED-01, PED-02..."""
    contadores[chave] += 1
    return f"{prefixo}-{contadores[chave]:02d}"


# ----------------------------------------------------------------------------
# LISTA - CATÁLOGO DE PRODUTOS
# Regra: acesso por índice ou chave (aqui, o ID do produto).
# ----------------------------------------------------------------------------
def buscar_indice_produto(codigo):
    """Busca linear pelo ID. Devolve a posição do produto na lista ou -1 se não achar."""
    for indice, produto in enumerate(produtos):
        if produto["id"] == codigo:
            return indice
    return -1


def mostrar_produto(produto):
    print(f"  ID {produto['id']} | {produto['nome']} | "
          f"R$ {produto['preco']:.2f} | estoque: {produto['estoque']}")


def cadastrar_produto():
    """CREATE: acrescenta um produto no fim da lista (append)."""
    codigo = ler_inteiro("ID do produto: ", 1)
    if buscar_indice_produto(codigo) != -1:
        print("  Já existe um produto com esse ID.")
        return
    nome = ler_texto("Nome: ")
    preco = ler_preco("Preço (R$): ")
    estoque = ler_inteiro("Estoque: ", 0)
    produtos.append({"id": codigo, "nome": nome, "preco": preco, "estoque": estoque})
    print("  Produto cadastrado.")


def listar_produtos():
    """READ: percorre a lista inteira e mostra cada produto."""
    if not produtos:
        print("  Catálogo vazio.")
        return
    for produto in produtos:
        mostrar_produto(produto)


def consultar_produto():
    """READ: consulta um produto específico pelo ID."""
    codigo = ler_inteiro("ID do produto: ", 1)
    indice = buscar_indice_produto(codigo)
    if indice == -1:
        print("  Produto não encontrado.")
    else:
        mostrar_produto(produtos[indice])


def atualizar_produto():
    """UPDATE: localiza pelo ID e troca os dados do produto na mesma posição."""
    codigo = ler_inteiro("ID do produto: ", 1)
    indice = buscar_indice_produto(codigo)
    if indice == -1:
        print("  Produto não encontrado.")
        return
    print("  Dados atuais:")
    mostrar_produto(produtos[indice])
    produtos[indice]["nome"] = ler_texto("Novo nome: ")
    produtos[indice]["preco"] = ler_preco("Novo preço (R$): ")
    produtos[indice]["estoque"] = ler_inteiro("Novo estoque: ", 0)
    print("  Produto atualizado.")


def remover_produto():
    """DELETE: remove o produto da lista (os itens seguintes andam uma posição)."""
    codigo = ler_inteiro("ID do produto: ", 1)
    indice = buscar_indice_produto(codigo)
    if indice == -1:
        print("  Produto não encontrado.")
        return
    mostrar_produto(produtos[indice])
    if confirmar("  Remover este produto?"):
        produtos.pop(indice)
        print("  Produto removido.")


def menu_lista():
    while True:
        print("\n--- CATÁLOGO DE PRODUTOS (Lista) ---")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Consultar produto por ID")
        print("4 - Atualizar produto")
        print("5 - Remover produto")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            consultar_produto()
        elif opcao == "4":
            atualizar_produto()
        elif opcao == "5":
            remover_produto()
        elif opcao == "0":
            return
        else:
            print("  Opção inválida.")


# ----------------------------------------------------------------------------
# FILA - PROCESSAMENTO DE PAGAMENTOS (FIFO: o primeiro a entrar é o primeiro a sair)
# Regra: inserção só no FIM (append) e remoção só no INÍCIO (popleft).
# ----------------------------------------------------------------------------
def texto_pedido(pedido):
    return (f"{pedido['id']} | {pedido['cliente']} | "
            f"R$ {pedido['valor']:.2f} | {pedido['status']}")


def enfileirar_pedido():
    """CREATE: o pedido novo entra no fim da fila com status 'Aguardando'."""
    cliente = ler_texto("Nome do cliente: ")
    valor = ler_preco("Valor do pedido (R$): ")
    pedido = {"id": proximo_id("pedido", "PED"), "cliente": cliente,
              "valor": valor, "status": "Aguardando"}
    fila_pagamentos.append(pedido)
    print(f"  Pedido {pedido['id']} entrou na fila (posição {len(fila_pagamentos)}).")


def listar_fila():
    """READ: mostra a fila do início (próximo a sair) até o fim."""
    if not fila_pagamentos:
        print("  Fila vazia.")
        return
    for posicao, pedido in enumerate(fila_pagamentos, start=1):
        marca = "   <- próximo a ser processado" if posicao == 1 else ""
        print(f"  {posicao}º | {texto_pedido(pedido)}{marca}")


def ver_proximo_pedido():
    """READ: consulta o início da fila sem remover (índice 0)."""
    if not fila_pagamentos:
        print("  Fila vazia.")
        return
    print("  Próximo da fila: " + texto_pedido(fila_pagamentos[0]))


def atualizar_status_pedido():
    """UPDATE: muda só o status de um pedido. A posição dele na fila não muda."""
    if not fila_pagamentos:
        print("  Fila vazia.")
        return
    codigo = ler_texto("ID do pedido (ex: PED-01): ").upper()
    for pedido in fila_pagamentos:
        if pedido["id"] == codigo:
            for numero, status in enumerate(STATUS_FILA, start=1):
                print(f"  {numero} - {status}")
            escolha = ler_inteiro("Novo status: ", 1)
            if escolha > len(STATUS_FILA):
                print("  Opção inválida.")
                return
            pedido["status"] = STATUS_FILA[escolha - 1]
            print("  Status atualizado.")
            return
    print("  Pedido não encontrado na fila.")


def processar_pagamento():
    """DELETE: tira o pedido MAIS ANTIGO (início da fila) e registra a decisão."""
    if not fila_pagamentos:
        print("  Não há pagamentos na fila.")
        return
    pedido = fila_pagamentos.popleft()  # remove do início: complexidade O(1)
    print("  Processando: " + texto_pedido(pedido))
    if confirmar("  Aprovar o pagamento?"):
        pedido["status"] = "Aprovado"
    else:
        pedido["status"] = "Recusado"
    print(f"  Pagamento {pedido['status'].lower()}. Pedido {pedido['id']} saiu da fila.")


def menu_fila():
    while True:
        print("\n--- PAGAMENTOS (Fila - FIFO) ---")
        print("1 - Enfileirar novo pedido")
        print("2 - Listar fila")
        print("3 - Ver próximo da fila")
        print("4 - Atualizar status de um pedido")
        print("5 - Processar pagamento (remove o primeiro)")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            enfileirar_pedido()
        elif opcao == "2":
            listar_fila()
        elif opcao == "3":
            ver_proximo_pedido()
        elif opcao == "4":
            atualizar_status_pedido()
        elif opcao == "5":
            processar_pagamento()
        elif opcao == "0":
            return
        else:
            print("  Opção inválida.")


# ----------------------------------------------------------------------------
# PILHA - HISTÓRICO DE AÇÕES DO CARRINHO (LIFO: o último a entrar é o primeiro a sair)
# Regra: inserção e remoção só no TOPO (o último elemento da lista).
# ----------------------------------------------------------------------------
def registrar_acao():
    """PUSH: empilha uma nova ação no topo."""
    descricao = ler_texto("Descrição da ação (ex: Adicionou Teclado ao carrinho): ")
    acao = {"id": proximo_id("acao", "ACAO"), "descricao": descricao}
    pilha_acoes.append(acao)
    print(f"  Ação {acao['id']} registrada no topo da pilha.")


def listar_pilha():
    """READ: mostra do topo para a base (ordem inversa da inserção)."""
    if not pilha_acoes:
        print("  Pilha vazia.")
        return
    for posicao, acao in enumerate(reversed(pilha_acoes), start=1):
        marca = "TOPO ->" if posicao == 1 else "       "
        print(f"  {marca} {acao['id']} | {acao['descricao']}")


def ver_topo():
    """TOP/PEEK: consulta o topo sem remover (índice -1)."""
    if not pilha_acoes:
        print("  Pilha vazia.")
        return
    acao = pilha_acoes[-1]
    print(f"  Topo: {acao['id']} | {acao['descricao']}")


def atualizar_topo():
    """UPDATE: só o elemento do topo pode ser alterado, como manda a regra da pilha."""
    if not pilha_acoes:
        print("  Pilha vazia.")
        return
    print(f"  Ação do topo: {pilha_acoes[-1]['descricao']}")
    pilha_acoes[-1]["descricao"] = ler_texto("Nova descrição: ")
    print("  Ação do topo atualizada.")


def desfazer_acao():
    """POP: desfaz (remove) somente a última ação registrada."""
    if not pilha_acoes:
        print("  Nenhuma ação para desfazer.")
        return
    acao = pilha_acoes.pop()  # remove do topo: complexidade O(1)
    print(f"  Ação desfeita: {acao['descricao']} ({acao['id']})")


def menu_pilha():
    while True:
        print("\n--- CARRINHO: HISTÓRICO DE AÇÕES (Pilha - LIFO) ---")
        print("1 - Registrar ação (push)")
        print("2 - Listar pilha (do topo para a base)")
        print("3 - Ver topo")
        print("4 - Atualizar ação do topo")
        print("5 - Desfazer última ação (pop)")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            registrar_acao()
        elif opcao == "2":
            listar_pilha()
        elif opcao == "3":
            ver_topo()
        elif opcao == "4":
            atualizar_topo()
        elif opcao == "5":
            desfazer_acao()
        elif opcao == "0":
            return
        else:
            print("  Opção inválida.")


# ----------------------------------------------------------------------------
# ÁRVORE - DEPARTAMENTOS > CATEGORIAS > SUBCATEGORIAS
# O dicionário 'arvore' é a raiz implícita. Cada chave é um nó e o valor dela é
# o dicionário dos seus filhos. Folha = dicionário vazio {}.
# Exemplo: {"Informática": {"Periféricos": {"Teclados": {}, "Mouses": {}}}}
# Os caminhos são digitados assim: Informática > Periféricos > Teclados
# ----------------------------------------------------------------------------
def ler_caminho(mensagem):
    """Lê um caminho separado por '>' e devolve a lista de nomes. Vazio = raiz."""
    texto = input(mensagem)
    nomes = [parte.strip() for parte in texto.split(">")]
    return [nome for nome in nomes if nome != ""]


def buscar_no(caminho):
    """Desce na árvore seguindo o caminho. Devolve o dicionário do nó ou None."""
    no = arvore  # começa na raiz
    for nome in caminho:
        if nome not in no:
            return None
        no = no[nome]
    return no


def inserir_no():
    """CREATE: acrescenta um filho em um nó existente (ou um departamento na raiz)."""
    print("  Informe o PAI do novo nó. Deixe vazio para criar um Departamento.")
    caminho_pai = ler_caminho("  Caminho do pai (ex: Informática > Periféricos): ")
    if len(caminho_pai) >= MAX_NIVEIS:
        print(f"  A árvore tem no máximo {MAX_NIVEIS} níveis.")
        return
    pai = buscar_no(caminho_pai)
    if pai is None:
        print("  Caminho do pai não encontrado (use exatamente os mesmos nomes).")
        return
    nivel = NIVEIS[len(caminho_pai)]
    nome = ler_texto(f"  Nome ({nivel}): ", "|>")
    if nome in pai:
        print("  Já existe um nó com esse nome nesse local.")
        return
    pai[nome] = {}  # todo nó novo nasce como folha
    print(f"  {nivel} '{nome}' inserido(a).")


def exibir_arvore(no, nivel=0):
    """READ: imprime a hierarquia usando recursão (cada filho é uma subárvore)."""
    for nome, filhos in no.items():
        print("    " * nivel + f"[{NIVEIS[nivel]}] {nome}")
        exibir_arvore(filhos, nivel + 1)


def mostrar_hierarquia():
    if not arvore:
        print("  Árvore vazia.")
        return
    exibir_arvore(arvore)


def navegar_no():
    """READ: vai até um nó e lista os filhos diretos dele."""
    caminho = ler_caminho("  Caminho do nó (vazio = raiz): ")
    no = buscar_no(caminho)
    if no is None:
        print("  Nó não encontrado.")
        return
    titulo = " > ".join(caminho) if caminho else "Raiz"
    if not no:
        print(f"  '{titulo}' não tem filhos.")
        return
    print(f"  Filhos de '{titulo}':")
    for filho in no:
        print(f"   - {filho}")


def renomear_no():
    """UPDATE: troca o nome do nó e mantém toda a subárvore dele."""
    caminho = ler_caminho("  Caminho do nó a renomear: ")
    if not caminho:
        print("  Informe um nó (a raiz não tem nome).")
        return
    pai = buscar_no(caminho[:-1])  # o pai é o caminho sem o último nome
    antigo = caminho[-1]
    if pai is None or antigo not in pai:
        print("  Nó não encontrado.")
        return
    novo = ler_texto("  Novo nome: ", "|>")
    if novo in pai:
        print("  Já existe um nó com esse nome nesse local.")
        return
    pai[novo] = pai.pop(antigo)  # o valor (filhos) passa para a chave nova
    print("  Nó renomeado.")


def remover_no():
    """DELETE: remove o nó e, junto com ele, todos os seus descendentes."""
    caminho = ler_caminho("  Caminho do nó a remover: ")
    if not caminho:
        print("  Informe um nó (a raiz não pode ser removida).")
        return
    pai = buscar_no(caminho[:-1])
    nome = caminho[-1]
    if pai is None or nome not in pai:
        print("  Nó não encontrado.")
        return
    if pai[nome]:
        print("  Atenção: este nó tem filhos e todos eles serão removidos também.")
    if confirmar(f"  Remover '{nome}'?"):
        del pai[nome]
        print("  Nó removido.")


def menu_arvore():
    while True:
        print("\n--- DEPARTAMENTOS E CATEGORIAS (Árvore) ---")
        print("1 - Inserir nó")
        print("2 - Exibir hierarquia completa")
        print("3 - Navegar (ver filhos de um nó)")
        print("4 - Renomear nó")
        print("5 - Remover nó")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            inserir_no()
        elif opcao == "2":
            mostrar_hierarquia()
        elif opcao == "3":
            navegar_no()
        elif opcao == "4":
            renomear_no()
        elif opcao == "5":
            remover_no()
        elif opcao == "0":
            return
        else:
            print("  Opção inválida.")


# ----------------------------------------------------------------------------
# PERSISTÊNCIA EM TXT ÚNICO
# Formato, uma linha por registro:
#   LISTA|id|nome|preco|estoque
#   FILA|id|cliente|valor|status
#   PILHA|id|descricao
#   ARVORE|nó1|nó2|nó3   (caminho da raiz até uma folha)
# ----------------------------------------------------------------------------
def memoria_vazia():
    return not (produtos or fila_pagamentos or pilha_acoes or arvore)


def caminhos_das_folhas(no, caminho):
    """Percorre a árvore (recursão) e devolve o caminho completo de cada folha.
    Nós internos não precisam de linha própria: já aparecem dentro dos caminhos."""
    resultado = []
    for nome, filhos in no.items():
        novo_caminho = caminho + [nome]
        if filhos:                                   # tem filhos: continua descendo
            resultado.extend(caminhos_das_folhas(filhos, novo_caminho))
        else:                                        # dicionário vazio: é folha
            resultado.append(novo_caminho)
    return resultado


def montar_linhas():
    """Converte as quatro estruturas em linhas de texto."""
    linhas = []
    for p in produtos:
        linhas.append(f"LISTA|{p['id']}|{p['nome']}|{p['preco']:.2f}|{p['estoque']}")
    for pedido in fila_pagamentos:                   # do início ao fim da fila
        linhas.append(f"FILA|{pedido['id']}|{pedido['cliente']}|"
                      f"{pedido['valor']:.2f}|{pedido['status']}")
    for acao in pilha_acoes:                         # da base ao topo
        linhas.append(f"PILHA|{acao['id']}|{acao['descricao']}")
    for caminho in caminhos_das_folhas(arvore, []):
        linhas.append("ARVORE|" + "|".join(caminho))
    return linhas


def salvar_dados():
    """Exporta o estado atual da memória para o arquivo (sobrescreve o anterior)."""
    if memoria_vazia() and os.path.exists(ARQUIVO):
        if not confirmar("  A memória está vazia e já existe um arquivo salvo. Sobrescrever?"):
            print("  Salvamento cancelado.")
            return
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
            for linha in montar_linhas():
                arquivo.write(linha + "\n")
    except OSError:
        print("  Erro ao gravar o arquivo.")
        return
    print(f"  Dados salvos em {ARQUIVO}.")


def atualizar_contador(chave, id_texto):
    """Depois de carregar, o contador volta ao maior número usado (PED-03 -> 3).
    Assim os próximos IDs não repetem os que já estão em memória."""
    try:
        numero = int(id_texto.split("-")[1])
    except (IndexError, ValueError):
        return
    if numero > contadores[chave]:
        contadores[chave] = numero


def carregar_dados():
    """Reconstrói as estruturas em memória a partir do arquivo."""
    if not os.path.exists(ARQUIVO):
        print("  Arquivo não encontrado. Salve os dados primeiro.")
        return
    if not memoria_vazia() and not confirmar("  Os dados atuais da memória serão substituídos. Continuar?"):
        print("  Carregamento cancelado.")
        return
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except (OSError, UnicodeDecodeError):
        print("  Erro ao ler o arquivo.")
        return

    # Limpa tudo antes de preencher: assim carregar duas vezes não duplica dados.
    produtos.clear()
    fila_pagamentos.clear()
    pilha_acoes.clear()
    arvore.clear()
    contadores["pedido"] = 0
    contadores["acao"] = 0

    ignoradas = 0
    for linha in linhas:
        linha = linha.strip()
        if linha == "":
            continue
        campos = linha.split("|")
        tipo = campos[0]
        try:
            if tipo == "LISTA" and len(campos) == 5:
                produtos.append({"id": int(campos[1]), "nome": campos[2],
                                 "preco": float(campos[3]), "estoque": int(campos[4])})
            elif tipo == "FILA" and len(campos) == 5:
                fila_pagamentos.append({"id": campos[1], "cliente": campos[2],
                                        "valor": float(campos[3]), "status": campos[4]})
                atualizar_contador("pedido", campos[1])
            elif tipo == "PILHA" and len(campos) == 3:
                pilha_acoes.append({"id": campos[1], "descricao": campos[2]})
                atualizar_contador("acao", campos[1])
            elif tipo == "ARVORE" and 2 <= len(campos) <= MAX_NIVEIS + 1:
                no = arvore
                for nome in campos[1:]:
                    # setdefault reaproveita o nó se ele já existe (sem duplicar)
                    # e cria um dicionário vazio se for novo
                    no = no.setdefault(nome, {})
            else:
                ignoradas += 1
        except ValueError:                           # número inválido na linha
            ignoradas += 1

    print(f"  Dados carregados: {len(produtos)} produto(s), {len(fila_pagamentos)} pedido(s) "
          f"na fila, {len(pilha_acoes)} ação(ões) na pilha e a árvore de categorias.")
    if ignoradas > 0:
        print(f"  Atenção: {ignoradas} linha(s) inválida(s) foram ignoradas.")


# ----------------------------------------------------------------------------
# MENU PRINCIPAL
# ----------------------------------------------------------------------------
def main():
    print("PLATAFORMA DE COMÉRCIO ELETRÔNICO")
    print("O sistema começa vazio. Use 'Carregar dados' para recuperar um arquivo salvo.")
    try:
        while True:
            print("\n===== MENU PRINCIPAL =====")
            print("1 - Catálogo de produtos (Lista)")
            print("2 - Pagamentos (Fila)")
            print("3 - Histórico de ações do carrinho (Pilha)")
            print("4 - Departamentos e categorias (Árvore)")
            print("5 - Salvar dados")
            print("6 - Carregar dados")
            print("0 - Sair")
            opcao = input("Escolha: ").strip()
            if opcao == "1":
                menu_lista()
            elif opcao == "2":
                menu_fila()
            elif opcao == "3":
                menu_pilha()
            elif opcao == "4":
                menu_arvore()
            elif opcao == "5":
                salvar_dados()
            elif opcao == "6":
                carregar_dados()
            elif opcao == "0":
                if confirmar("Deseja salvar os dados antes de sair?"):
                    salvar_dados()
                print("Sistema encerrado.")
                break
            else:
                print("  Opção inválida.")
    except (KeyboardInterrupt, EOFError):
        print("\nSistema encerrado.")


if __name__ == "__main__":
    main()
