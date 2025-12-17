import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import sqlalchemy as sa

# =========================
# CONEXÃO COM SQL SERVER
# =========================
engine = sa.create_engine(
    "mssql+pyodbc://@PX-NTB_85MLD53/ControleFinanceiro"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

# =========================
# CATEGORIAS
# =========================
categorias = [
    "Assinaturas",
    "Contas da Casa",
    "Financiamento do Carro",
    "Parcelamento de Compras",
    "Seguros",
    "Compras em Geral",
    "Gastos Fixos",
    "Entrada"
]

# =========================
# FUNÇÕES
# =========================
def salvar_lancamento():
    tipo = tipo_var.get()
    categoria = categoria_var.get()
    descricao = descricao_entry.get()
    valor = valor_entry.get()

    if not valor:
        messagebox.showwarning("Atenção", "Informe o valor")
        return

    try:
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido")
        return

    with engine.begin() as conn:
        conn.execute(
            sa.text("""
                INSERT INTO Lancamentos (tipo, categoria, descricao, valor)
                VALUES (:tipo, :categoria, :descricao, :valor)
            """),
            {
                "tipo": tipo,
                "categoria": categoria,
                "descricao": descricao,
                "valor": valor
            }
        )

    valor_entry.delete(0, tk.END)
    descricao_entry.delete(0, tk.END)
    messagebox.showinfo("Sucesso", "Lançamento salvo 💾")


def gerar_grafico():
    query = """
        SELECT categoria, SUM(valor) total
        FROM Lancamentos
        WHERE tipo = 'Gasto'
          AND (delet IS NULL OR delet <> '*')
        GROUP BY categoria
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        messagebox.showwarning("Aviso", "Nenhum dado encontrado")
        return

    df.plot(kind="bar", x="categoria", y="total", legend=False)
    plt.title("Gastos por Categoria")
    plt.ylabel("Valor (R$)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def exportar_excel():
    df = pd.read_sql(
        "SELECT * FROM Lancamentos WHERE delet IS NULL OR delet <> '*'",
        engine
    )

    if df.empty:
        messagebox.showwarning("Aviso", "Nada para exportar")
        return

    df.to_excel("controle_financeiro.xlsx", index=False)
    messagebox.showinfo("Exportado", "Arquivo criado 📊")


# =========================
# TELA DE CONSULTA
# =========================
def abrir_consulta():
    janela_c = tk.Toplevel(janela)
    janela_c.title("Consulta por Data")
    janela_c.geometry("800x400")

    tk.Label(janela_c, text="Data Início (dd/mm/aaaa)").pack()
    data_ini_entry = tk.Entry(janela_c)
    data_ini_entry.pack()

    tk.Label(janela_c, text="Data Fim (dd/mm/aaaa)").pack()
    data_fim_entry = tk.Entry(janela_c)
    data_fim_entry.pack()

    cols = ("ID", "Tipo", "Categoria", "Descrição", "Valor", "Data")
    tabela = ttk.Treeview(janela_c, columns=cols, show="headings")

    for col in cols:
        tabela.heading(col, text=col)
        tabela.column(col, width=120)

    tabela.pack(expand=True, fill="both")

    def buscar():
        try:
            data_ini = datetime.strptime(
                data_ini_entry.get(), "%d/%m/%Y"
            ).date()
            data_fim = datetime.strptime(
                data_fim_entry.get(), "%d/%m/%Y"
            ).date()
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido")
            return

        query = """
            SELECT id, tipo, categoria, descricao, valor, data_lancamento
            FROM Lancamentos
            WHERE (delet IS NULL OR delet <> '*')
              AND CAST(data_lancamento AS DATE)
                  BETWEEN :ini AND :fim
            ORDER BY data_lancamento
        """

        df = pd.read_sql(
            sa.text(query),
            engine,
            params={"ini": data_ini, "fim": data_fim}
        )

        tabela.delete(*tabela.get_children())

        for _, row in df.iterrows():
            tabela.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["tipo"],
                    row["categoria"],
                    row["descricao"],
                    row["valor"],
                    row["data_lancamento"].strftime("%d/%m/%Y")
                )
            )

    def excluir():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um registro")
            return

        id_sel = tabela.item(item)["values"][0]

        with engine.begin() as conn:
            conn.execute(
                sa.text(
                    "UPDATE Lancamentos SET delet='*' WHERE id=:id"
                ),
                {"id": id_sel}
            )

        tabela.delete(item)
        messagebox.showinfo("Excluído", "Registro removido logicamente")

    tk.Button(janela_c, text="Buscar", command=buscar).pack(pady=5)
    tk.Button(janela_c, text="Excluir", command=excluir).pack(pady=5)


# =========================
# INTERFACE PRINCIPAL
# =========================
janela = tk.Tk()
janela.title("Controle Financeiro 💰")
janela.geometry("360x450")
janela.resizable(False, False)

tk.Label(janela, text="Tipo").pack()
tipo_var = tk.StringVar(value="Gasto")
tk.OptionMenu(janela, tipo_var, "Entrada", "Gasto").pack()

tk.Label(janela, text="Categoria").pack()
categoria_var = tk.StringVar(value=categorias[0])
tk.OptionMenu(janela, categoria_var, *categorias).pack()

tk.Label(janela, text="Descrição").pack()
descricao_entry = tk.Entry(janela, width=40)
descricao_entry.pack()

tk.Label(janela, text="Valor").pack()
valor_entry = tk.Entry(janela)
valor_entry.pack()

tk.Button(janela, text="Salvar", command=salvar_lancamento, width=25).pack(pady=5)
tk.Button(janela, text="Consultar / Excluir", command=abrir_consulta, width=25).pack(pady=5)
tk.Button(janela, text="Gráfico por Categoria", command=gerar_grafico, width=25).pack(pady=5)
tk.Button(janela, text="Exportar Excel", command=exportar_excel, width=25).pack(pady=5)

tk.Label(janela, text="SQL Server Local", fg="gray").pack(pady=10)
tk.Label(janela, text="Feito com carinho por Patricia Santos", fg="gray").pack(pady=2)


janela.mainloop()
