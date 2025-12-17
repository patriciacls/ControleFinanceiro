CREATE TABLE Lancamentos ( 
id INT IDENTITY PRIMARY KEY, 
tipo VARCHAR(10),-- Entrada ou Gasto 
categoria VARCHAR(50), 
descricao VARCHAR(255), 
valor DECIMAL(10,2), 
data_lancamento DATETIME DEFAULT GETDATE(), 
delet varchar(1) );
