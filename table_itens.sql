CREATE TABLE Itens (
    id SERIAL PRIMARY KEY,
    produto_id INTEGER NOT NULL,
    local_id INTEGER NOT NULL,
    serial_number VARCHAR(100) UNIQUE,
    status VARCHAR(50) DEFAULT 'disponivel',
    data_aquisicao DATE,
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_produto FOREIGN KEY(produto_id) REFERENCES Produtos(id),
    CONSTRAINT fk_local FOREIGN KEY(local_id) REFERENCES Locais(id)
);