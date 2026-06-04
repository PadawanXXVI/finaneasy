# 🌿 Guia de Branches — Padrão Oficial do Projeto FinanEasy

Este guia define como criar, nomear, usar e encerrar branches no projeto FinanEasy, garantindo organização, rastreabilidade e colaboração eficiente entre os membros da equipe.

---

## 🎯 Objetivo do Guia

- Padronizar nomes de branches  
- Evitar conflitos e bagunça no histórico  
- Facilitar revisões e pull requests  
- Garantir que cada membro trabalhe de forma isolada e organizada  

---

## 🧩 Estrutura de Nomes de Branches

Cada branch deve seguir o padrão:

```
tipo/nome-descritivo
```

Ou, no caso das branches pessoais do time:

```
nome-dev
```

### Branches pessoais oficiais:

- `anderson-ds`  
- `paulo-dev`  
- `raquel-da`  

Essas branches são **fixas** e usadas para desenvolvimento contínuo de cada membro.

---

## 🏷 Tipos de Branches

### 1) Branches de funcionalidade (feature)

```
feat/nome-da-feature
```

Exemplos:

- `feat/menu-inicial`
- `feat/calculo-saldo`
- `feat/resumo-financeiro`

---

### 2) Branches de correção (fix)

```
fix/descricao-do-bug
```

Exemplos:

- `fix/erro-calculo-despesas`
- `fix/menu-opcao-invalida`

---

### 3) Branches de documentação (docs)

```
docs/nome-do-documento
```

Exemplos:

- `docs/guia-de-commits`
- `docs/arquitetura-inicial`

---

### 4) Branches de refatoração (refactor)

```
refactor/area-afetada
```

Exemplos:

- `refactor/models`
- `refactor/organizar-services`

---

### 5) Branches de tarefas internas (chore)

```
chore/tarefa
```

Exemplos:

- `chore/configurar-ambiente`
- `chore/atualizar-gitignore`

---

## 🔀 Fluxo de Trabalho com Branches

### 1) Criar branch a partir da `main`

Sempre atualize a main antes:

```
git checkout main
git pull
git checkout -b feat/nova-feature
```

---

### 2) Fazer commits seguindo o Guia de Commits

Exemplo:

```
feat(models): criar classe Transaction
```

---

### 3) Abrir Pull Request

- PR sempre **da sua branch → main**  
- Nunca faça commit direto na main  
- Descreva claramente o que foi feito  
- Marque quem deve revisar (normalmente Anderson)

---

### 4) Revisão e Merge

- O PR só é mergeado após revisão  
- Após o merge, a branch pode ser deletada (exceto branches pessoais)

---

## 🧹 Branches que nunca devem ser deletadas

- `main`  
- `anderson-ds`  
- `paulo-dev`  
- `raquel-da`  

---

## 🧭 Boas Práticas

- Uma branch = uma tarefa  
- Nunca misture funcionalidades diferentes na mesma branch  
- Mantenha nomes curtos e claros  
- Atualize sua branch com a main antes de abrir PR  
- Evite branches gigantes (faça PRs menores e frequentes)

---

## 🏁 Exemplo de Fluxo Completo

1. Criar branch:  
   `feat/calculo-saldo`

2. Desenvolver e commitar:  
   `feat(services): implementar cálculo de saldo`

3. Abrir PR para `main`

4. Revisar e aprovar

5. Fazer merge

6. Deletar branch (se não for branch pessoal)

---

## 📌 Relação com Milestones e Versionamento

- Cada milestone pode ter várias branches  
- Quando a milestone fecha → criamos uma tag (ex.: `v0.1.0`)  
- Branches ajudam a manter o histórico limpo para releases

---
