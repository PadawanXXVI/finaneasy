# 📘 Guia de Commits — Padrão Oficial do Projeto FinanEasy

Este guia define como escrever mensagens de commit de forma padronizada, clara e rastreável, utilizando o padrão **Conventional Commits**.

---

## 🎯 Objetivo do Guia

- Manter o histórico limpo e organizado  
- Facilitar revisões e pull requests  
- Ajudar no versionamento semântico (tags v0.1.0, v1.0.0 etc.)  
- Garantir consistência entre todos os membros da equipe  

---

## 🧩 Estrutura de um Commit

Formato padrão:

```bash
tipo(escopo): descrição breve e objetiva
```

Exemplos:

```bash
feat(models): adicionar classe Transaction
fix(services): corrigir cálculo de saldo
docs(readme): atualizar seção de equipe
refactor(ui): reorganizar funções do menu
```

---

## 🏷 Tipos de Commit Permitidos

### feat

Nova funcionalidade adicionada ao projeto.  
Ex.: `feat: criar módulo de transações`

### fix

Correção de bug.  
Ex.: `fix: corrigir erro no cálculo de despesas`

### docs

Alterações na documentação (README, ABOUT, guias etc.).  
Ex.: `docs(readme): adicionar versão inicial`

### refactor

Refatoração de código sem alterar comportamento.  
Ex.: `refactor: melhorar organização das classes`

### style

Mudanças que não afetam lógica (espaços, formatação, nomes).  
Ex.: `style: ajustar indentação`

### test

Adição ou ajuste de testes.  
Ex.: `test: adicionar testes para FinanceManager`

### chore

Tarefas internas que não afetam o código de produção.  
Ex.: `chore: atualizar .gitignore`

---

## 🧭 Escopos Recomendados

Use escopos para indicar a área afetada:

- readme  
- about  
- models  
- services  
- ui  
- data  
- core  
- docs  
- tests  

Exemplo:

```bash
feat(models): criar classe Expense
```

---

## ✍️ Como escrever a descrição

A descrição deve ser:

- curta  
- clara  
- no imperativo  
- sem ponto final  

✔ Correto:  
`feat: adicionar cálculo de saldo`

✘ Errado:  
`feat: adicionando cálculo de saldo.`  
`feat: adicionei cálculo de saldo`  

---

## 🧪 Exemplos Reais para o FinanEasy

- `feat(models): criar classe Transaction`  
- `feat(services): implementar cálculo de saldo`  
- `fix(ui): corrigir opção inválida no menu`  
- `docs(readme): adicionar seção de tecnologias`  
- `refactor(models): renomear atributos para consistência`  
- `chore: configurar ambiente inicial`  

---

## 🏁 Commits que iniciam milestones

Quando fechar uma milestone importante, use commits como:

```bash
chore(release): preparar versão v0.1.0
docs: atualizar README para entrega do hackathon
```

---

## 🔖 Relação com Versionamento (Tags)

Este guia funciona junto com o versionamento semântico:

- **v0.1.0** → entrega do Hackathon  
- **v1.0.0** → versão final  
- **v1.1.0** → início da versão web  

---
