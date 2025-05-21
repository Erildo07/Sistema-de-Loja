# Sistema-de-Loja


🏪 Sistema de Loja - Visão Geral
🔧 1. Funcionalidades principais
📦 Produtos de estoque / preço

    Cada produto tem:

        Nome

        Quantidade em estoque

        Preço

    Armazenado no banco de dados.

💰 Gerenciar ganhos financeiros

    Cada venda registra:

        Valor total

        Data/hora da venda

    Sistema calcula:

        Total do dia

        Total do mês

        Total do ano

📊 Total de vendas /dia, mês, ano

    Página ou dashboard com relatórios:

        Exibe vendas agrupadas por data

        Exibe lucro por período

🧾 2. Fluxo de venda
✅ Opção de registrar nova venda

    Vendedor seleciona produtos

    Sistema calcula valor final

    Após confirmação:

        Reduz quantidade do estoque

        Registra a venda

📲 Gerar QR Code da venda

    Ao finalizar:

        Gera um QR Code com:

            ID da venda

            Link para comprovante

            Dados do cliente (opcional)

✏️ Editar produtos

    Interface para:

        Adicionar novo produto

        Alterar nome, preço, quantidade

🛒 3. Página de compras para o usuário (cliente)

    Mostra os produtos disponíveis com:

        Nome

        Imagem

        Preço

        Botão "Adicionar ao carrinho"

    Carrinho mostra total

    Ao finalizar:

        Gera QR Code ou redireciona ao WhatsApp com resumo da compra

🤖 4. Bot do WhatsApp

    Usado para:

        Confirmar pedidos

        Enviar mensagem tipo:

            "Olá {{nome}}, sua compra foi registrada! Valor total: R$ XX,XX"

    Opções de resposta rápida:

        [1] Ver produtos

        [2] Finalizar pedido

        [3] Falar com atendente

🗃️ 5. Banco de dados - Estrutura
Tabelas principais (SQLite, PostgreSQL, etc.):

Produtos
- id
- nome
- preco
- quantidade

Vendas
- id
- data
- valor_total

ItensVenda
- id
- venda_id
- produto_id
- quantidade
- preco_unitario



## 👨‍💻 Desenvolvedores

- **Erildo Nunes** – responsável pelo sistema principal, banco de dados e frontend.
- **Rodrigo da Silva** – responsável pelas automações, bot do WhatsApp e sistema de vendas.

---
