# Controle Financeiro
Uma aplicação Desktop desenvolvida em Python para gerenciamento de finanças pessoais. O sistema permite registrar entradas e saídas, visualizar gastos por categoria em gráficos e exportar relatórios para Excel, utilizando um banco de dados SQL Server local.
## Funcionalidade
* **Registro de Lançamentos:** Adicione receitas e despesas com descrição e categoria.
* **Categorização:** Categorias pré-definidas (Assinaturas, Contas da Casa, Financiamento, etc.).
* **Consulta Avançada:** Busque lançamentos por período de datas.
* **Exclusão Lógica:** O sistema marca o registro como excluído (`delet='*'`) sem apagá-lo fisicamente do banco.
* **Visualização Gráfica:** Gráfico de barras exibindo gastos por categoria (Matplotlib).
* **Exportação:** Gere um arquivo `.xlsx` com todos os lançamentos ativos.

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface Gráfica:** Tkinter
* **Banco de Dados:** SQL Server
* **Bibliotecas Principais:**
    * `pandas` (Manipulação de dados e Excel)
    * `matplotlib` (Gráficos)
    * `sqlalchemy` & `pyodbc` (Conexão com Banco de Dados)

## Pré-requisitos e Configuração

### 1. Banco de Dados
Certifique-se de ter o **SQL Server** instalado e o **ODBC Driver 17 for SQL Server**.

1.  Crie um banco de dados chamado `ControleFinanceiro`.
2.  Execute o script abaixo para criar a tabela necessária:

```sql
CREATE TABLE Lancamentos ( 
    id INT IDENTITY PRIMARY KEY, 
    tipo VARCHAR(10), -- Entrada ou Gasto 
    categoria VARCHAR(50), 
    descricao VARCHAR(255), 
    valor DECIMAL(10,2), 
    data_lancamento DATETIME DEFAULT GETDATE(), 
    delet varchar(1) 
);
