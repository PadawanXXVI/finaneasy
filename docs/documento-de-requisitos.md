# 📄 Levantamento de Requisitos — FinanEasy

## 🧭 1. Visão Geral do Sistema
O **FinanEasy** é um sistema de controle financeiro desenvolvido em Python para o Hackathon Python do SENAI/DF.  
Seu objetivo é permitir que o usuário registre receitas e despesas, calcule o saldo total e visualize um resumo financeiro simples e claro.

---

## 🧱 2. Requisitos Funcionais (RF)

### **RF01 — Registrar receita**
O sistema deve permitir registrar uma receita com descrição, valor e data (opcional).

### **RF02 — Registrar despesa**
O sistema deve permitir registrar uma despesa com descrição, valor e data (opcional).

### **RF03 — Listar transações**
O sistema deve exibir todas as receitas e despesas registradas.

### **RF04 — Calcular saldo total**
O sistema deve calcular automaticamente:
**saldo = total de receitas – total de despesas**

### **RF05 — Exibir resumo financeiro**
O sistema deve apresentar:
- total de receitas  
- total de despesas  
- saldo final  

### **RF06 — Menu interativo**
O sistema deve exibir um menu com opções claras para o usuário navegar.

### **RF07 — Validar entradas**
O sistema deve impedir valores inválidos (ex.: letras no campo de valor).

### **RF08 — Encerrar o programa**
O sistema deve permitir sair de forma segura.

---

## 🧩 3. Requisitos Não Funcionais (RNF)

### **RNF01 — Usabilidade**
O sistema deve ser simples, intuitivo e fácil de usar via terminal.

### **RNF02 — Organização do código**
O código deve seguir boas práticas:
- PEP8  
- POO  
- Funções bem definidas  
- Comentários quando necessário  

### **RNF03 — Performance**
As operações devem ser executadas instantaneamente.

### **RNF04 — Portabilidade**
O sistema deve rodar em qualquer ambiente com Python 3.

### **RNF05 — Manutenibilidade**
O código deve ser modular, permitindo evolução futura.

---

## ⚖️ 4. Regras de Negócio (RN)

### **RN01 — Valores devem ser positivos**
Receitas e despesas devem aceitar apenas valores maiores que zero.

### **RN02 — Saldo não pode ser alterado manualmente**
O saldo é sempre calculado automaticamente.

### **RN03 — Transações devem ter tipo definido**
Cada transação deve ser classificada como receita ou despesa.

### **RN04 — Datas são opcionais**
Se o usuário não informar data, o sistema pode usar a data atual ou deixar em branco.

---

## 👤 5. Atores do Sistema
- **Usuário final**  
- **Equipe de desenvolvimento**: Anderson, Paulo e Raquel

---

## 📘 6. Casos de Uso

### **UC01 — Registrar Receita**
Usuário informa dados → sistema valida → salva → confirma.

### **UC02 — Registrar Despesa**
Mesmo fluxo do UC01.

### **UC03 — Consultar Resumo Financeiro**
Sistema calcula e exibe totais e saldo.

### **UC04 — Listar Transações**
Sistema exibe todas as transações registradas.

### **UC05 — Encerrar Sistema**
Usuário escolhe sair → sistema encerra.

---

## ✔️ 7. Critérios de Aceitação

- O sistema registra receitas e despesas corretamente.  
- O saldo é calculado sem erros.  
- O menu é claro e funcional.  
- Entradas inválidas não quebram o sistema.  
- O resumo financeiro é exibido de forma organizada.  
- O código é legível e modular.  
- O programa roda em qualquer computador com Python 3.

---

## 🧪 8. Restrições

- Desenvolvido apenas com Python puro.  
- Deve rodar em terminal.  
- Deve usar estruturas básicas de Python.  
- Deve ser entregue até a data definida pelo professor.

---

## 🚀 9. Possíveis Extensões Futuras

- Persistência em arquivo (JSON ou CSV)  
- Interface gráfica (Tkinter)  
- API (FastAPI)  
- Dashboard financeiro  
- Exportação de relatórios  

---
