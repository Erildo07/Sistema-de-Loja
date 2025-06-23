# user/compras.py

import sqlite3
from datetime import datetime
import qrcode
import os

# Conecta ao mesmo banco
conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', 'loja.db'))
cursor = conn.cursor()

def listar_produtos():
    print("\n--- Produtos Disponíveis ---")
    cursor.execute("SELECT * FROM produtos WHERE quantidade > 0")
    produtos = cursor.fetchall()
    for p in produtos:
        print(f"{p[0]} - {p[1]} | R${p[2]:.2f} | Estoque: {p[3]}")
    print()

def gerar_qr_code(texto):
    nome_arquivo = f"qrcode_user_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    caminho = os.path.join(os.path.dirname(__file__), nome_arquivo)
    img = qrcode.make(texto)
    img.save(caminho)
    print(f"🧾 QR Code salvo em: {caminho}")

def comprar():
    carrinho = []
    total = 0

    while True:
        listar_produtos()
        pid = input("ID do produto (ou 'fim' para finalizar): ")
        if pid.lower() == 'fim':
            break
        try:
            pid = int(pid)
            cursor.execute("SELECT nome, preco, quantidade FROM produtos WHERE id=?", (pid,))
            produto = cursor.fetchone()
            if produto:
                nome, preco, estoque = produto
                if estoque == 0:
                    print("❌ Sem estoque.")
                    continue
                qtd = int(input(f"Quantidade de {nome} (disponível: {estoque}): "))
                if qtd <= 0 or qtd > estoque:
                    print("❌ Quantidade inválida.")
                    continue
                total += preco * qtd
                carrinho.append((nome, preco, qtd))
                cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id=?", (qtd, pid))
                conn.commit()
            else:
                print("Produto não encontrado.")
        except ValueError:
            print("Entrada inválida.")

    if carrinho:
        descricao = ', '.join([f"{q}x {n}" for n, _, q in carrinho])
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO vendas (data, total, descricao) VALUES (?, ?, ?)", (data, total, descricao))
        conn.commit()
        gerar_qr_code(f"Compra: {descricao}\nTotal: R${total:.2f}\nData: {data}")
        print(f"\n✅ Compra finalizada!\n💬 WhatsApp: Você comprou {descricao} por R${total:.2f}\n")
    else:
        print("Nenhum item comprado.\n")

if __name__ == '__main__':
    comprar()
