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

insert into BD02.funcionarios_fabrica
	(ID, NOME)
select ID, Nome from bd01.funcionarios;
	

    