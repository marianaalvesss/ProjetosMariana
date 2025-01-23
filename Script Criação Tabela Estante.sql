CREATE TABLE dbo.estante (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome_livro VARCHAR(255) NULL,
    autor VARCHAR(255) NULL,
    genero VARCHAR(255) NULL,
    numero_paginas NUMERIC(10,0) NULL,
    editora VARCHAR(255) NULL,
    data_compra DATE NULL,
    valor_compra DECIMAL(10,2) NULL,
    valor_atual DECIMAL(10,2) NULL,
    status VARCHAR(255) NULL,
    data_concluido DATE NULL,
    formato VARCHAR(255) NULL,
    nota DECIMAL(10,2) NULL
);
