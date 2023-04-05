create database BD01
default character set utf8mb4
default collate utf8mb4_general_ci;

use bd01;

create table funcionarios (
	ID int not null auto_increment,
	Nome varchar(50) not null,
	RG varchar(20) not null,
	CPF varchar(15) not null,
	Data_admissao date not null,
	Data_hora_alteracao_do_registro timestamp not null,
	CEP varchar(8) not null,
	primary key (ID)
) default charset utf8mb4;

insert into funcionarios
	(ID, Nome, RG, CPF, Data_admissao, Data_hora_alteracao_do_registro, CEP)
values
	(default, 'João Silva', '123456789', '12345678900', '2022-01-01', '2022-01-01 12:34:56', '01310100'),
	(default, 'Maria Santos', '987654321', '98765432100', '2022-01-02', '2022-01-02 12:34:56', '04610080'),
	(default, 'José Pereira', '112233445', '11122233300', '2022-01-03', '2022-01-03 12:34:56', '06460050'),
	(default, 'Ana Oliveira', '445556667', '44455566600', '2022-01-04', '2022-01-04 12:34:56', '08215230'),
	(default, 'Ricardo Alves', '778889990', '77788899900', '2022-01-05', '2022-01-05 12:34:56', '11065500'),
	(default, 'Carla Mendes', '001112223', '00011122200', '2022-01-06', '2022-01-06 12:34:56', '88512292'),
	(default, 'Márcio Rocha', '334445556', '33344455500', '2022-01-07', '2022-01-07 12:34:56', '22221010'),
	(default, 'Lívia Nogueira', '667778881', '66677788800', '2022-01-08', '2022-01-08 12:34:56', '30180120'),
	(default, 'Gabriel Fernandes', '990001114', '99900011100', '2022-01-09', '2022-01-09 12:34:56', '40240230'),
	(default, 'Juliana Costa', '223334448', '22233344400', '2022-01-10', '2022-01-10 12:34:56', '57072500');
