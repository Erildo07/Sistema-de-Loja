import sqlite3
import qrcode
from datetime import datetime
from user import compras 

# === Conexão com banco ===
conn = sqlite3.connect('loja.db')
cursor = conn.cursor()

# === Tabelas ===
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    total REAL NOT NULL,
    descricao TEXT NOT NULL
)
''')
conn.commit()

# === Funções ===

def adicionar_produto():
    nome = input("Nome do produto: ")
    preco = float(input("Preço: "))
    quantidade = int(input("Quantidade: "))
    cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
    conn.commit()
    print("Produto adicionado!\n")

def listar_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    for p in produtos:
        print(f"{p[0]} - {p[1]} | R${p[2]:.2f} | Estoque: {p[3]}")
    print()

def editar_produto():
    listar_produtos()
    pid = int(input("ID do produto para editar: "))
    novo_preco = float(input("Novo preço: "))
    nova_qtd = int(input("Nova quantidade: "))
    cursor.execute("UPDATE produtos SET preco=?, quantidade=? WHERE id=?", (novo_preco, nova_qtd, pid))
    conn.commit()
    print("Produto atualizado!\n")

def registrar_venda():
    listar_produtos()
    ids = input("IDs dos produtos comprados (separados por vírgula): ").split(',')
    total = 0
    descricoes = []

    for pid in ids:
        pid = int(pid.strip())
        cursor.execute("SELECT nome, preco, quantidade FROM produtos WHERE id=?", (pid,))
        p = cursor.fetchone()
        if p and p[2] > 0:
            total += p[1]
            descricoes.append(p[0])
            cursor.execute("UPDATE produtos SET quantidade = quantidade - 1 WHERE id=?", (pid,))
        else:
            print(f"Produto {pid} não disponível ou sem estoque.")

    if total > 0:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        descricao = ', '.join(descricoes)
        cursor.execute("INSERT INTO vendas (data, total, descricao) VALUES (?, ?, ?)", (data, total, descricao))
        conn.commit()

        gerar_qr_code(f"Venda de R${total:.2f} em {data}")
        print("Venda registrada e QR Code gerado!\n")
        print(f"🟢 Simulação de mensagem WhatsApp: Obrigado pela compra de: {descricao} - Total: R${total:.2f}")
    else:
        print("Nenhum produto válido comprado.\n")

def gerar_qr_code(texto):
    img = qrcode.make(texto)
    img.save(f"qrcode_venda_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
    texto = "67996487977"

def total_vendas_por_data():
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()
    hoje = datetime.now().date()
    total_dia = total_mes = total_ano = 0

    for v in vendas:
        data_venda = datetime.strptime(v[1], "%Y-%m-%d %H:%M:%S")
        if data_venda.date() == hoje:
            total_dia += v[2]
        if data_venda.month == hoje.month and data_venda.year == hoje.year:
            total_mes += v[2]
        if data_venda.year == hoje.year:
            total_ano += v[2]

    print(f"🔹 Total HOJE: R${total_dia:.2f}")
    print(f"🔹 Total MÊS: R${total_mes:.2f}")
    print(f"🔹 Total ANO: R${total_ano:.2f}\n")

# === Menu ===

def menu():
    while True:
        print("""
--- SISTEMA DE LOJA ---
1. Adicionar produto
2. Listar produtos
3. Editar produto
4. Registrar venda
5. Relatório financeiro
0. Sair
""")
        op = input("Escolha: ")
        if op == '1':
            adicionar_produto()
        elif op == '2':
            listar_produtos()
        elif op == '3':
            editar_produto()
        elif op == '4':
            compras.comprar()
        elif op == '5':
            total_vendas_por_data()
        elif op == '0':
            break
        else:
            print("Opção inválida!\n")

menu()