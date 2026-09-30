-- Cria as duas tabelas do projeto: raw_vendas (bruta) e vendas_tratadas (tratada)
-- Este script deve ser executado DENTRO do banco vendas_supermercado

-- ============================================================
-- TABELA 1: raw_vendas (camada Raw)
-- Cópia fiel do CSV. Todas as colunas são TEXT para nada se
-- perder na importação. Sem restrições de propósito: a limpeza
-- e a tipagem acontecem depois, no Python.
-- A ordem das colunas é a mesma do CSV (17 colunas).
-- ============================================================
CREATE TABLE IF NOT EXISTS raw_vendas (
    invoice_id              TEXT,  -- Invoice ID
    branch                  TEXT,  -- Branch
    city                    TEXT,  -- City
    customer_type           TEXT,  -- Customer type
    gender                  TEXT,  -- Gender
    product_line            TEXT,  -- Product line
    unit_price              TEXT,  -- Unit price
    quantity                TEXT,  -- Quantity
    tax_5pct                TEXT,  -- Tax 5%
    sales                   TEXT,  -- Sales
    sale_date               TEXT,  -- Date (evito o nome "date", que é palavra de tipo do SQL)
    sale_time               TEXT,  -- Time (evito o nome "time" pelo mesmo motivo)
    payment                 TEXT,  -- Payment
    cogs                    TEXT,  -- cogs
    gross_margin_percentage TEXT,  -- gross margin percentage
    gross_income            TEXT,  -- gross income
    rating                  TEXT   -- Rating
);

-- ============================================================
-- TABELA 2: vendas_tratadas (camada Tratada)
-- Segue o dicionário de dados do enunciado (seção 6).
-- Nomes com maiúscula ou acento precisam de aspas duplas,
-- por exemplo "Filial" e "Avaliação".
-- ============================================================
CREATE TABLE IF NOT EXISTS vendas_tratadas (
    -- Chave primária: identifica cada venda de forma única
    id_venda          VARCHAR(50)    PRIMARY KEY,

    -- Campos obrigatórios (NOT NULL)
    "Filial"          VARCHAR(10)    NOT NULL,
    "Cidade"          VARCHAR(100)   NOT NULL,
    tipo_cliente      VARCHAR(50),
    "Gênero"          VARCHAR(20),
    linha_produto     VARCHAR(150)   NOT NULL,

    -- Valores numéricos: NOT NULL nos campos críticos + CHECK de regra de negócio
    preco_unitario    NUMERIC(10,2)  NOT NULL CHECK (preco_unitario >= 0),
    "Quantidade"      INTEGER        NOT NULL CHECK ("Quantidade" > 0),
    "Imposto"         NUMERIC(10,2)  CHECK ("Imposto" >= 0),
    valor_total       NUMERIC(12,2)  NOT NULL CHECK (valor_total >= 0),

    -- Data e hora já convertidas para os tipos certos
    data_venda        DATE           NOT NULL,
    hora_venda        TIME,

    forma_pagamento   VARCHAR(50)    NOT NULL,
    custo_mercadoria  NUMERIC(12,2)  CHECK (custo_mercadoria >= 0),
    margem_percentual NUMERIC(10,2),
    receita_bruta     NUMERIC(12,2)  CHECK (receita_bruta >= 0),

    -- Avaliação do cliente: só aceita notas de 0 a 10
    "Avaliação"       NUMERIC(4,2)   CHECK ("Avaliação" BETWEEN 0 AND 10)
);