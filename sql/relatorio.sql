SELECT 
	Pro.Produto_id,
	Pro.Nome_produto,
	Pro.Categoria,
	Pro.Preco_unitario,
	Ven.Quantidade,
	Pro.Preco_unitario * Ven.Quantidade AS Valor_total,
	Ven.Tipo_venda,
	CASE
		WHEN Pro.Preco_unitario <= 0 THEN 'Venda invalida'
		WHEN Ven.Validacao_venda = 'Venda invalida' THEN 'Venda invalida'
		ELSE 'Venda valida'
		END AS Status,
	Ven.Data_venda
FROM dbo.Vendas AS Ven
LEFT JOIN dbo.Produtos AS Pro
	ON Pro.Produto_id = Ven.Produto_id 
