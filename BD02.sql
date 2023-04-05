create database BD02
default character set utf8mb4
default collate utf8mb4_general_ci;

use bd02;

create table funcionarios_fabrica(
	ID int not null auto_increment,
	NOME varchar(50) not null,
    RG varchar(20),
    CPF varchar(15),
    Data_admissao date,
    Data_hora_alteracao_do_registro timestamp,
    CEP varchar(8),
    ENDERECO varchar(255),
    BAIRRO varchar(50),
    CIDADE varchar(50),
    primary key (ID)
) default charset=utf8mb4;

insert into funcionarios_fabrica
	(ID, NOME)
values
	(default, 'João Silva'),
	(default, 'Maria Santos'),
	(default, 'José Pereira'),
	(default, 'Ana Oliveira'),
	(default, 'Ricardo Alves'),
	(default, 'Carla Mendes'),
	(default, 'Márcio Rocha'),
	(default, 'Lívia Nogueira'),
	(default, 'Gabriel Fernandes'),
	(default, 'Juliana Costa');