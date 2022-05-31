DROP TABLE IF EXISTS cliente CASCADE;
DROP TABLE IF EXISTS endereco CASCADE;
DROP TABLE IF EXISTS tempo CASCADE;
DROP TABLE IF EXISTS produto CASCADE;
DROP TABLE IF EXISTS venda_fato CASCADE;

CREATE TABLE cliente (
    id_cliente_nk INTEGER NOT NULL,
    data_cadastro_cliente DATE NOT NULL,
    nome_cliente VARCHAR(255) NOT NULL,
    nome_fantasia_cliente VARCHAR(255) NOT NULL,
    tipo_pessoa_cliente CHAR(2) NOT NULL,
    origem_cliente VARCHAR(100) NOT NULL,
    data_nascimento_cliente DATE NOT NULL,
    codigo_cliente INTEGER NOT NULL,
    data_carga_cliente DATE NOT NULL,
    CONSTRAINT cliente_sk_pk PRIMARY KEY (id_cliente_nk)
);

CREATE TABLE endereco (
    id_endereco_nk INTEGER NOT NULL,
    cep INTEGER NOT NULL,
    sigla_uf CHAR(2) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    cidade VARCHAR(255) NOT NULL,
    bairro VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    complemento VARCHAR(255) NOT NULL,
    data_carga_endereco DATE NOT NULL,
    CONSTRAINT localidade_sk_pk PRIMARY KEY (id_endereco_nk)
);

CREATE TABLE tempo (
    id_tempo_sk DATE NOT NULL,
    dia INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    mes_nome VARCHAR(100) NOT NULL,
    ano INTEGER NOT NULL,
    dia_da_semana VARCHAR(100) NOT NULL,
    trimestre_do_ano INTEGER NOT NULL,
    semestre_do_ano INTEGER NOT NULL,
    CONSTRAINT tempo_sk_pk PRIMARY KEY (id_tempo_sk)
);

CREATE TABLE produto (
    id_produto_nk INTEGER NOT NULL,
    data_cadastro_produto DATE NOT NULL,
    nome_produto VARCHAR(255) NOT NULL,
    valor_produto DECIMAL NOT NULL,
    download_produto INTEGER NOT NULL,
    upload_produto INTEGER NOT NULL,
    tipo_produto VARCHAR(100) NOT NULL,
    data_carga_produto DATE NOT NULL,
    CONSTRAINT produto_sk_pk PRIMARY KEY (id_produto_nk)
);

CREATE TABLE venda_fato (
    id_cliente_nk INTEGER NOT NULL,
    id_endereco_nk INTEGER NOT NULL,
    id_produto_nk INTEGER NOT NULL,
    id_tempo_sk DATE NOT NULL,
    id_venda_sk INTEGER NOT NULL,
    id_transacao INTEGER NOT NULL,
    valor_venda DECIMAL NOT NULL,
    status VARCHAR(100) NOT NULL,
    data_venda DATE NOT NULL,
    data_habilitacao DATE NOT NULL, 
    descricao_tecnologia VARCHAR(100) NOT NULL,
    vendedor VARCHAR(100) NOT NULL,
    origem VARCHAR(100) NOT NULL,
    valor_instalacao DECIMAL NOT NULL,
    motivo_cancelamento VARCHAR(100) NOT NULL,
    data_cancelamento DATE NOT NULL,
    numero_servico_cliente INTEGER NOT NULL,
    tipo_transacao VARCHAR(100) NOT NULL,
    tipo_produto VARCHAR(100) NOT NULL,
    forma_cobranca VARCHAR(100) NOT NULL,
    empresa VARCHAR(255) NOT NULL,
    data_carga_venda DATE NOT NULL,
    CONSTRAINT venda_fato_pk PRIMARY KEY (id_cliente_nk, id_endereco_nk, id_produto_nk, id_tempo_sk, id_venda_sk)
);

ALTER TABLE venda_fato ADD FOREIGN KEY (id_cliente_nk) REFERENCES cliente (id_cliente_nk);
ALTER TABLE venda_fato ADD FOREIGN KEY (id_endereco_nk) REFERENCES endereco (id_endereco_nk);
ALTER TABLE venda_fato ADD FOREIGN KEY (id_produto_nk) REFERENCES produto (id_produto_nk);
ALTER TABLE venda_fato ADD FOREIGN KEY (id_tempo_sk) REFERENCES tempo (id_tempo_sk); 