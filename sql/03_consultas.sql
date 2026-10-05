-- Consultas SQL fundamentais sobre a camada Raw (raw_vendas)
-- Executar no banco vendas_supermercado, UMA consulta por vez
-- As colunas da Raw são TEXT, então foi utilizado CAST para fazer contas

-- 1. Faturamento por filial (maior primeiro)
SELECT branch AS filial,
       city AS cidade,
       ROUND(SUM(CAST(sales AS NUMERIC)), 2) AS faturamento
FROM raw_vendas
GROUP BY branch, city
ORDER BY faturamento DESC;

-- 2. Quantidade de vendas por filial
SELECT branch AS filial,
       COUNT(*) AS qtd_vendas
FROM raw_vendas
GROUP BY branch
ORDER BY qtd_vendas DESC;

-- 3. Faturamento por linha de produto
SELECT product_line AS linha_produto,
       ROUND(SUM(CAST(sales AS NUMERIC)), 2) AS faturamento
FROM raw_vendas
GROUP BY product_line
ORDER BY faturamento DESC;

-- 4. Avaliação média por linha de produto
SELECT product_line AS linha_produto,
       ROUND(AVG(CAST(rating AS NUMERIC)), 2) AS avaliacao_media
FROM raw_vendas
GROUP BY product_line
ORDER BY avaliacao_media DESC;

-- 5. Quantidade de vendas por forma de pagamento
SELECT payment AS forma_pagamento,
       COUNT(*) AS qtd_vendas
FROM raw_vendas
GROUP BY payment
ORDER BY qtd_vendas DESC;

-- 6. Valor médio das vendas
SELECT ROUND(AVG(CAST(sales AS NUMERIC)), 2) AS valor_medio
FROM raw_vendas;

-- 7. Maior venda registrada
SELECT invoice_id, branch, product_line, sales
FROM raw_vendas
ORDER BY CAST(sales AS NUMERIC) DESC
LIMIT 1;

-- 8. Quantidade de vendas por dia da semana
SELECT TO_CHAR(TO_DATE(sale_date, 'MM/DD/YYYY'), 'FMDay') AS dia_semana,
       COUNT(*) AS qtd_vendas
FROM raw_vendas
GROUP BY dia_semana
ORDER BY qtd_vendas DESC;

-- 9. Exemplo com WHERE: vendas acima de 500
SELECT invoice_id, branch, sales
FROM raw_vendas
WHERE CAST(sales AS NUMERIC) > 500
ORDER BY CAST(sales AS NUMERIC) DESC;


