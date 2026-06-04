# 🔀 Guia de Pull Requests — Padrão Oficial do Projeto FinanEasy

Este guia define como criar, revisar e aprovar Pull Requests (PRs) no projeto FinanEasy, garantindo organização, clareza e colaboração eficiente entre os membros da equipe.

---

## 🎯 Objetivo do Guia

- Padronizar a criação de PRs  
- Facilitar revisões e evitar conflitos  
- Garantir que cada mudança seja analisada antes de entrar na `main`  
- Manter o histórico limpo e rastreável  

---

## 🧩 Quando abrir um Pull Request

Abra um PR sempre que:

- Finalizar uma tarefa em sua branch  
- Implementar uma nova funcionalidade  
- Corrigir um bug  
- Atualizar documentação importante  
- Realizar refatorações significativas  

Nunca faça commits diretamente na `main`.

---

## 🏷 Nome do Pull Request

O título deve seguir o padrão:

```
tipo(escopo): descrição breve da mudança
```

Exemplos:

- `feat(models): adicionar classe Transaction`
- `fix(ui): corrigir erro na opção do menu`
- `docs(branches): criar guia de branches`

---

## 📝 Descrição do Pull Request

A descrição deve conter:

### ✔ 1. O que foi feito  
Explique de forma clara e objetiva.

### ✔ 2. Por que foi feito  
Contextualize a necessidade da mudança.

### ✔ 3. Como testar  
Passos simples para validar o funcionamento.

### ✔ 4. Checklist  
Inclua:

- Código testado  
- Sem erros de lint  
- Sem arquivos desnecessários  
- Commit seguindo o padrão  
- Branch atualizada com a `main`  

Exemplo de checklist:

```
- [x] Código testado
- [x] Commits seguindo Conventional Commits
- [x] Branch atualizada com main
- [x] Documentação atualizada (se necessário)
```

---

## 🔄 Atualizando sua branch antes do PR

Sempre atualize sua branch com a `main`:

```
git checkout main
git pull
git checkout sua-branch
git merge main
```

Ou, se preferir rebase:

```
git pull --rebase origin main
```

---

## 👀 Processo de Revisão

### ✔ Quem revisa?
Normalmente **Anderson**, mas qualquer membro pode revisar.

### ✔ O que verificar na revisão?

- Código limpo e organizado  
- Nome de variáveis e funções coerentes  
- Commits seguindo o padrão  
- Escopo do PR bem definido  
- Nada fora do propósito da tarefa  
- Documentação atualizada, se necessário  

### ✔ Como aprovar
Comente “Aprovado” ou use o botão **Approve** no GitHub.

---

## 🧹 Após o Merge

- A branch pode ser deletada (exceto branches pessoais)  
- A milestone pode ser atualizada  
- Se for uma entrega importante, criar tag (ex.: `v0.1.0`)  

---

## 🚫 O que evitar em um Pull Request

- PRs gigantes com muitas mudanças  
- Misturar funcionalidades diferentes  
- Commits fora do padrão  
- Código sem teste ou sem revisão  
- PR sem descrição  

---

## 🏁 Fluxo Completo de um PR

1. Criar branch  
2. Desenvolver a tarefa  
3. Fazer commits seguindo o padrão  
4. Atualizar branch com a `main`  
5. Abrir PR com título e descrição corretos  
6. Solicitar revisão  
7. Ajustar se necessário  
8. Receber aprovação  
9. Fazer merge  
10. Deletar branch (se aplicável)

---
