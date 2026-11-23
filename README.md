# Plataforma de Comércio Eletrônico — Projeto Final de Teoria das Estruturas de Dados

**Autor:** Arthur Maximus Silva e Rocha
**Disciplina:** Teoria das Estruturas de Dados
**Tema sorteado:** Tema 2 — Plataforma de Comércio Eletrônico

Sistema de linha de comando (CLI) em Python que integra as quatro estruturas de dados estudadas na disciplina — **Lista, Fila, Pilha e Árvore** — e preserva os dados entre execuções em um único arquivo texto (`dados_sistema.txt`).

| Módulo da plataforma | Estrutura | Implementação em Python |
|---|---|---|
| Catálogo geral de produtos | **Lista** | `list` |
| Processamento e aprovação de pagamentos | **Fila** (FIFO) | `collections.deque` |
| Histórico de ações do carrinho (desfazer) | **Pilha** (LIFO) | `list` (topo = último elemento) |
| Departamentos > Categorias > Subcategorias | **Árvore** | dicionários aninhados (`dict`) |

---

## 1. Como executar

**Requisitos:** Python 3.8 ou superior. Usa somente a biblioteca padrão (`os`, `math` e `collections`), então não há nada para instalar.

1. Baixe ou clone este repositório e abra um terminal **dentro da pasta do projeto**.
2. Execute:

```bash
python main.py
```

(em alguns sistemas o comando é `python3 main.py`).

3. Navegue pelo menu digitando o número da opção e pressionando Enter.

**Observações importantes**

- O sistema **inicia totalmente vazio**: nenhum dado vem pré-carregado no código.
- Para guardar o trabalho, use **5 — Salvar dados**. Na próxima execução, use **6 — Carregar dados** para recuperar tudo.
- O arquivo `dados_sistema.txt` é criado na pasta em que o comando `python main.py` foi executado.
- Ao escolher **0 — Sair**, o sistema pergunta se deseja salvar antes de encerrar.

### Menu principal

```
1 - Catálogo de produtos (Lista)
2 - Pagamentos (Fila)
3 - Histórico de ações do carrinho (Pilha)
4 - Departamentos e categorias (Árvore)
5 - Salvar dados
6 - Carregar dados
0 - Sair
```

### Operações disponíveis (CRUD respeitando a regra de cada estrutura)

| Módulo | Criar | Ler | Atualizar | Remover |
|---|---|---|---|---|
| **Lista** | Cadastrar produto (no fim da lista) | Listar todos / consultar por ID | Alterar nome, preço e estoque por ID | Remover por ID |
| **Fila** | Enfileirar pedido (**só no fim**) | Listar fila / ver o próximo | Alterar o status de um pedido (a posição não muda) | Processar pagamento (**só o primeiro** sai) |
| **Pilha** | Registrar ação (**só no topo**) | Listar do topo à base / ver o topo | Alterar a ação do topo | Desfazer a última ação (**só o topo** sai) |
| **Árvore** | Inserir nó filho em um caminho existente | Exibir hierarquia / navegar pelos filhos de um nó | Renomear nó (mantém a subárvore) | Remover nó (leva os descendentes junto) |

### Como informar caminhos na árvore

Os nós são localizados por caminho, separando os níveis com `>`:

```
Informática > Periféricos > Teclados
```

Para criar um **departamento** (primeiro nível), deixe o caminho do pai em branco. Os nomes devem ser digitados exatamente como foram criados. A árvore aceita até 3 níveis: departamento, categoria e subcategoria.

---

## 2. Justificativa técnica das estruturas

### 2.1 Lista — catálogo de produtos (`list`)

O catálogo é uma coleção que cresce e diminui ao longo do tempo, na qual se consulta, altera e remove produtos em **qualquer posição**, e não apenas nas pontas. A lista é a estrutura sequencial indicada para isso: mantém a ordem de cadastro, permite acesso direto por índice e, no nosso caso, busca por chave (o ID do produto).

- **Inserção no fim** com `append`: O(1) amortizado.
- **Busca por ID:** percorre a lista, O(n). Para um catálogo de tamanho moderado é perfeitamente adequado, e ganha-se simplicidade.
- **Remoção por posição** com `pop(i)`: O(n), pois os elementos seguintes são deslocados.

Nem a fila nem a pilha serviriam aqui, porque elas restringem o acesso a uma das pontas, e o catálogo precisa de acesso a qualquer produto.

### 2.2 Fila — pagamentos (`collections.deque`)

Pagamentos devem ser tratados **na ordem em que chegaram**: quem pediu primeiro é processado primeiro. Isso é exatamente o princípio **FIFO** (*First-In, First-Out*). Qualquer outra ordem seria injusta com os clientes e quebraria a lógica do negócio.

- Pedido novo entra **no fim**: `append()`.
- O pagamento a processar é sempre **o do início**: `popleft()`.
- Nenhuma operação do sistema remove ou insere no meio da fila.

**Por que `deque` e não `list`?** Com uma lista, remover o primeiro elemento (`pop(0)`) obriga o Python a deslocar todos os demais, custando **O(n)**. No `deque`, tanto `append` quanto `popleft` custam **O(1)**. Em uma plataforma com muitos pedidos aguardando, essa diferença importa.

### 2.3 Pilha — histórico de ações do carrinho (`list`)

Desfazer modificações no carrinho segue a lógica do "Ctrl+Z": a **última** ação feita é a **primeira** a ser desfeita. É o princípio **LIFO** (*Last-In, First-Out*) da pilha.

- Registrar uma ação é `push`: `append()` no fim da lista.
- Desfazer é `pop`: `pop()` remove o último elemento.
- Consultar o topo é `pilha[-1]`.

O **topo da pilha é o último elemento da lista**, porque `append` e `pop()` operam no fim da lista em **O(1)**. Se o topo fosse o início, cada operação custaria O(n). Como na pilha só o topo é acessível, nenhum registro do meio pode ser alterado ou removido (por isso a opção "Atualizar" mexe apenas na ação do topo).

### 2.4 Árvore — departamentos, categorias e subcategorias (`dict` aninhado)

Os produtos de uma loja são organizados em uma **hierarquia**: um departamento contém categorias e cada categoria contém subcategorias. Isso é uma árvore, e não uma sequência: cada nó tem **um pai** (exceto a raiz) e **zero ou mais filhos**. Uma lista, uma fila ou uma pilha não conseguem representar essa relação de pertencimento.

Na terminologia da disciplina:

| Conceito | No sistema |
|---|---|
| **Raiz** | O dicionário `arvore` (raiz implícita, sem nome) |
| **Nós** | Departamentos, categorias e subcategorias (as chaves do dicionário) |
| **Filhos** | O dicionário que é o valor de cada chave |
| **Folha** | Nó cujo dicionário de filhos está vazio (`{}`) |
| **Subárvore** | Um nó junto com todos os seus descendentes |
| **Profundidade** | Departamento = 1, categoria = 2, subcategoria = 3 (raiz no nível 0) |

Exemplo na memória:

```python
{
    "Informática": {
        "Periféricos": {"Teclados": {}, "Mouses": {}},
        "Monitores": {}
    },
    "Moda": {"Feminina": {}}
}
```

É uma **árvore geral** (não binária): um nó pode ter qualquer quantidade de filhos. O dicionário foi escolhido porque busca o filho pelo nome em tempo médio O(1) por nível, e porque a estrutura aninhada espelha a **definição recursiva** de árvore (cada filho é, ele mesmo, uma árvore). Por isso a exibição da hierarquia (`exibir_arvore`) e a coleta de folhas para salvar (`caminhos_das_folhas`) são recursivas. Remover um nó (`del`) elimina automaticamente toda a sua subárvore.

---

## 3. Persistência em arquivo texto

Todo o estado é gravado em **um único arquivo**, `dados_sistema.txt`, em UTF-8. Cada linha começa com o identificador da estrutura, seguido dos campos separados por `|`. Não são usados JSON, CSV, `pickle` nem banco de dados.

```
LISTA|101|Teclado Mecanico|250.00|15
FILA|PED-01|Cliente Joao|250.00|Aguardando
PILHA|ACAO-01|Adicionou Teclado ao carrinho
ARVORE|Informatica|Perifericos|Teclados
```

| Identificador | Campos |
|---|---|
| `LISTA` | id, nome, preço, estoque |
| `FILA` | id do pedido, cliente, valor, status |
| `PILHA` | id da ação, descrição |
| `ARVORE` | caminho da raiz até uma folha (um nó por campo) |

**Ordem dos registros.** A fila é gravada do início para o fim, e a pilha da base para o topo. Como o carregamento relê as linhas na mesma ordem, a **ordem FIFO e a ordem LIFO são preservadas** após salvar e carregar.

**Como a árvore é reconstruída.** Cada linha `ARVORE` traz o caminho completo até uma folha. Ao carregar, o sistema desce pelos nomes usando `setdefault`: se o nó já existe, ele é reaproveitado; se não existe, é criado como dicionário vazio. Assim, linhas que compartilham o mesmo departamento ou categoria **não duplicam nós**, e os nós intermediários não precisam de linha própria.

**Carregar sem duplicar.** Antes de preencher as estruturas, o carregamento as **esvazia**. Carregar o arquivo várias vezes sempre resulta no mesmo estado.

---

## 4. Decisões de projeto e validações

- **Arquivo único** (`main.py`), dividido em blocos de funções: entrada de dados, uma seção para cada estrutura, persistência e menu principal.
- **Validação de entrada:** textos vazios são recusados; números inválidos ou negativos são repetidos até a digitação correta; preço aceita vírgula ou ponto.
- **Caractere `|` proibido nos textos**, pois é o delimitador do arquivo. Nos nomes da árvore, o `>` também é proibido, pois separa os níveis do caminho.
- **Operações em estruturas vazias** (processar pagamento, desfazer, ver o topo etc.) exibem uma mensagem, sem causar erro.
- **IDs automáticos** para pedidos (`PED-01`) e ações (`ACAO-01`). Ao carregar o arquivo, os contadores retomam a partir do maior número existente, evitando repetições.
- **Confirmações** antes de remover um produto ou um nó, antes de substituir dados da memória ao carregar e antes de sobrescrever um arquivo existente com a memória vazia.
- **Tratamento de erros de arquivo:** arquivo inexistente, ilegível ou linhas fora do formato (que são ignoradas e contadas no aviso).

## 5. Complexidade das operações

| Operação | Estrutura | Custo |
|---|---|---|
| Cadastrar produto | Lista (`append`) | O(1) amortizado |
| Consultar, atualizar ou remover produto por ID | Lista | O(n) |
| Enfileirar pedido | Fila (`append`) | O(1) |
| Processar pagamento | Fila (`popleft`) | O(1) |
| Registrar ou desfazer ação, ver o topo | Pilha | O(1) |
| Localizar nó por caminho | Árvore | O(h), com h ≤ 3 |
| Exibir a hierarquia | Árvore | O(n), n = número de nós |
| Salvar e carregar | Todas | O(n) no total de registros |

## 6. Limitações conhecidas

- Os contadores de ID não são gravados no arquivo (o formato só contém os registros). Se o arquivo for salvo com a fila vazia, os IDs `PED-xx` recomeçam do 01 na próxima carga. Como nenhum pedido antigo permanece no sistema, não há conflito.
- Valores monetários usam `float`, suficiente para este projeto acadêmico. Em um sistema real, o ideal seria `decimal.Decimal` ou valores inteiros em centavos.
- O pedido processado sai da fila e não é guardado em histórico, pois o escopo do tema define a fila apenas como ordem de processamento.

## 7. Estrutura do repositório

```
.
├── main.py       # todo o código-fonte
└── README.md     # esta documentação
```

O arquivo `dados_sistema.txt` é gerado em tempo de execução, quando se usa a opção **Salvar dados**.
