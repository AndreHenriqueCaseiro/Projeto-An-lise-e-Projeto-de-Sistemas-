CREATE TABLE Movimentacoes (
    id SERIAL PRIMARY KEY,
    item_id INTEGER NOT NULL,
    local_origem_id INTEGER NOT NULL,
    local_destino_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    data_movimentacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    CONSTRAINT fk_item FOREIGN KEY(item_id) REFERENCES Itens(id),
    CONSTRAINT fk_local_origem FOREIGN KEY(local_origem_id) REFERENCES Locais(id),
    CONSTRAINT fk_local_destino FOREIGN KEY(local_destino_id) REFERENCES Locais(id),
    CONSTRAINT fk_usuario FOREIGN KEY(usuario_id) REFERENCES Usuarios(id)
);