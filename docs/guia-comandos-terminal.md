# 🧭 Guia Completo: Comandos de Terminal Essenciais para Usar com Git

Mesmo usando Git diariamente, você depende do terminal para navegar, criar, mover e inspecionar arquivos.  
Este guia reúne **todos os comandos não‑git** que você realmente usa no fluxo de trabalho.

---

## 📂 1. Navegação entre pastas

- **[cd](ca://s?q=Explique_o_comando_cd)** — entra em uma pasta.  
- **[cd ..](ca://s?q=O_que_faz_cd_2_pontos)** — volta um nível.  
- **[pwd](ca://s?q=Para_que_serve_pwd)** — mostra o caminho completo da pasta atual.  
- **[ls](ca://s?q=Como_usar_ls)** — lista arquivos e pastas.  
- **[ls -la](ca://s?q=ls_-la_explicacao)** — lista tudo, incluindo arquivos ocultos (como `.git`).

---

## 🛠️ 2. Manipulação de arquivos e diretórios

- **[mkdir](ca://s?q=Como_usar_mkdir)** — cria uma nova pasta.  
- **[touch](ca://s?q=Para_que_serve_touch)** — cria arquivos vazios (muito usado antes de `git add`).  
- **[rm](ca://s?q=Como_funciona_rm)** — remove arquivos.  
- **[rm -r](ca://s?q=rm_-r_explicacao)** — remove pastas recursivamente.  
- **[mv](ca://s?q=Como_usar_mv)** — move ou renomeia arquivos.  
- **[cp](ca://s?q=Como_usar_cp)** — copia arquivos.

---

## 🔍 3. Inspeção de conteúdo

- **[cat](ca://s?q=O_que_faz_cat)** — exibe o conteúdo de um arquivo.  
- **[less](ca://s?q=Como_usar_less)** — abre arquivos longos para leitura paginada.  
- **[head](ca://s?q=Comando_head_explicacao)** — mostra o início de um arquivo.  
- **[tail](ca://s?q=Comando_tail_explicacao)** — mostra o final (ótimo para logs).  
- **[grep](ca://s?q=Como_usar_grep)** — busca texto dentro de arquivos.

---

## ⚙️ 4. Utilidades gerais

- **[clear](ca://s?q=Comando_clear_terminal)** — limpa o terminal.  
- **[echo](ca://s?q=Para_que_serve_echo)** — imprime texto (útil em scripts).  
- **[history](ca://s?q=Comando_history)** — mostra comandos usados recentemente.  
- **[which](ca://s?q=Comando_which_explicacao)** — mostra onde um programa está instalado.  
- **[code .](ca://s?q=Abrir_VSCode_pelo_terminal)** — abre o VS Code na pasta atual (se instalado).  
- **[chmod](ca://s?q=Como_usar_chmod)** — altera permissões de arquivos.

---

## 🔗 5. Como esses comandos se conectam ao Git

Git depende do estado do sistema de arquivos.  
Esses comandos permitem:

- Criar arquivos antes de versionar (`touch`, `mkdir`).  
- Navegar até o repositório (`cd`).  
- Ver o que existe na pasta (`ls`).  
- Remover ou mover arquivos antes de commitar (`rm`, `mv`).  
- Inspecionar conteúdo antes de um commit (`cat`, `less`).  

Sem eles, você até usa Git, mas fica “cego” dentro do repositório.

---

## 🚀 6. Mini‑workflow Git + Terminal

```bash
mkdir meu-projeto
cd meu-projeto
git init
touch index.html
ls -la
git add index.html
git commit -m "Inicializa projeto"
code .
```
