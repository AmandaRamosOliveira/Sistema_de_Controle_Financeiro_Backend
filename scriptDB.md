create database SistemaDeControleFinanceiro;
use SistemaDeControleFinanceiro;

create table Usuario(
    id_usuario int primary key auto_increment,
    nome varchar(80) not null,
    email varchar(45) not null,
    telefone varchar(16) not null,
    senha varchar(100) not null,
    salario double not null
);
alter table usuario modify column salario decimal(10,2) not null;

CREATE TABLE conta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    categoria VARCHAR(255) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    tipo ENUM('fixa', 'variavel') NOT NULL,
    mes INT NOT NULL,       -- 1 a 12
    ano INT NOT NULL,       -- ex: 2025
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

create table Meta(
    id_meta int primary key auto_increment,
    descricaoMeta varchar(100) not null,
    valor double not null,
    valor_final double not null,
    periodo_meses int not null,
    id_usuario int not null,
    foreign key(id_usuario) references Usuario(id_usuario)
);
ALTER TABLE meta
ADD COLUMN mes_conclusao int not null;
ALTER TABLE meta
ADD COLUMN ano_conclusao int not null;
ALTER TABLE meta 
MODIFY mes_conclusao INT NULL,
MODIFY ano_conclusao INT NULL;

ADD COLUMN status ENUM('pendente', 'concluida') DEFAULT 'pendente';
CREATE TABLE verificacoes_email (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    codigo VARCHAR(10) NOT NULL,
    expiracao DATETIME NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

use SistemaDeControleFinanceiro;
select * from Usuario;
truncate table Usuario;

INSERT INTO conta (id_usuario, categoria, valor, tipo, mes, ano) VALUES
-- Janeiro (1)
(2, 'Telefone/Internet', 120.00, 'fixa', 1, 2025),
(2, 'Conta de Água', 80.00, 'fixa', 1, 2025),
(2, 'Luz', 150.00, 'fixa', 1, 2025),
(2, 'Cartão', 300.00, 'variavel', 1, 2025),
(2, 'Comida iFood', 90.00, 'variavel', 1, 2025),

-- Fevereiro (2)
(2, 'Telefone/Internet', 120.00, 'fixa', 2, 2025),
(2, 'Conta de Água', 85.00, 'fixa', 2, 2025),
(2, 'Luz', 140.00, 'fixa', 2, 2025),
(2, 'Cartão', 250.00, 'variavel', 2, 2025),
(2, 'Comida iFood', 100.00, 'variavel', 2, 2025),

-- Março (3)
(2, 'Telefone/Internet', 120.00, 'fixa', 3, 2025),
(2, 'Conta de Água', 90.00, 'fixa', 3, 2025),
(2, 'Luz', 160.00, 'fixa', 3, 2025),
(2, 'Cartão', 280.00, 'variavel', 3, 2025),
(2, 'Comida iFood', 120.00, 'variavel', 3, 2025),

-- Abril (4)
(2, 'Telefone/Internet', 120.00, 'fixa', 4, 2025),
(2, 'Conta de Água', 80.00, 'fixa', 4, 2025),
(2, 'Luz', 130.00, 'fixa', 4, 2025),
(2, 'Cartão', 200.00, 'variavel', 4, 2025),
(2, 'Comida iFood', 90.00, 'variavel', 4, 2025),

-- Maio (5)
(2, 'Telefone/Internet', 120.00, 'fixa', 5, 2025),
(2, 'Conta de Água', 85.00, 'fixa', 5, 2025),
(2, 'Luz', 145.00, 'fixa', 5, 2025),
(2, 'Cartão', 320.00, 'variavel', 5, 2025),
(2, 'Comida iFood', 110.00, 'variavel', 5, 2025),

-- Junho (6)
(2, 'Telefone/Internet', 120.00, 'fixa', 6, 2025),
(2, 'Conta de Água', 95.00, 'fixa', 6, 2025),
(2, 'Luz', 150.00, 'fixa', 6, 2025),
(2, 'Cartão', 270.00, 'variavel', 6, 2025),
(2, 'Comida iFood', 95.00, 'variavel', 6, 2025),

-- Julho (7)
(2, 'Telefone/Internet', 120.00, 'fixa', 7, 2025),
(2, 'Conta de Água', 90.00, 'fixa', 7, 2025),
(2, 'Luz', 160.00, 'fixa', 7, 2025),
(2, 'Cartão', 400.00, 'variavel', 7, 2025),
(2, 'Comida iFood', 100.00, 'variavel', 7, 2025),

-- Agosto (8) (⚠️ Já tem conta de luz — não inserir duplicada)
(2, 'Telefone/Internet', 120.00, 'fixa', 8, 2025),
(2, 'Conta de Água', 85.00, 'fixa', 8, 2025),
(2, 'Cartão', 350.00, 'variavel', 8, 2025),
(2, 'Comida iFood', 110.00, 'variavel', 8, 2025),

-- Setembro (9) (⚠️ Já tem conta de água e luz)
(2, 'Telefone/Internet', 120.00, 'fixa', 9, 2025),
(2, 'Cartão', 300.00, 'variavel', 9, 2025),
(2, 'Comida iFood', 100.00, 'variavel', 9, 2025),

-- Outubro (10) (⚠️ Já tem conta de água, telefone e material de construção)
(2, 'Luz', 150.00, 'fixa', 10, 2025),
(2, 'Cartão', 320.00, 'variavel', 10, 2025),
(2, 'Comida iFood', 95.00, 'variavel', 10, 2025),

-- Novembro (11)
(2, 'Telefone/Internet', 120.00, 'fixa', 11, 2025),
(2, 'Conta de Água', 85.00, 'fixa', 11, 2025),
(2, 'Luz', 155.00, 'fixa', 11, 2025),
(2, 'Cartão', 280.00, 'variavel', 11, 2025),
(2, 'Comida iFood', 120.00, 'variavel', 11, 2025),

-- Dezembro (12)
(2, 'Telefone/Internet', 120.00, 'fixa', 12, 2025),
(2, 'Conta de Água', 90.00, 'fixa', 12, 2025),
(2, 'Luz', 160.00, 'fixa', 12, 2025),
(2, 'Cartão', 500.00, 'variavel', 12, 2025),
(2, 'Comida iFood', 150.00, 'variavel', 12, 2025);
