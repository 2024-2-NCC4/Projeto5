require('dotenv').config();

const express = require('express');
const mysql = require('mysql2');

const app = express();
const PORT = process.env.PORT || 3000;

// Configurar a conexão com o banco de dados
const db = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

console.log("Host: ", process.env.DB_HOST);
console.log("Usuario:", process.env.DB_USER);
console.log("Senha: ", process.env.DB_PASSWORD);

// Conectar ao banco de dados
db.connect((err) => {
  if (err) {
    console.error('Erro ao conectar ao MySQL:', err);
    return;
  }
  console.log('Conectado ao MySQL!');
});

// Seus endpoints continuam os mesmos
app.get('/', (req, res) => {
  res.send('Servidor online!');
});

app.get('/dev', (req, res) => {
  const firstTenQuery = 'SELECT * FROM tabela_projeto ORDER BY id ASC LIMIT 10';
  const lastTenQuery = 'SELECT * FROM tabela_projeto ORDER BY id DESC LIMIT 10';

  db.query(firstTenQuery, (err, firstTenResults) => {
    if (err) {
      console.error('Erro ao executar a consulta dos primeiros 10 itens:', err);
      res.status(500).send('Erro no servidor');
      return;
    }

    db.query(lastTenQuery, (err, lastTenResults) => {
      if (err) {
        console.error('Erro ao executar a consulta dos últimos 10 itens:', err);
        res.status(500).send('Erro no servidor');
        return;
      }

      // Reverter a ordem dos últimos 10 itens para manter a ordem crescente
      lastTenResults.reverse();

      res.json({
        primeiros10: firstTenResults,
        ultimos10: lastTenResults,
      });
    });
  });
});

app.get('/query', (req, res) => {
  const { ramo, simbolo, data_inicio, data_final } = req.query;

  if (!ramo || !simbolo || !data_inicio || !data_final) {
    return res.status(400).send('Todos os parâmetros são necessários: ramo, simbolo, data_inicio e data_final.');
  }

  // Montar a query
  const query = `
    SELECT Data, Fechamento_Padronizado 
    FROM tabela_projeto 
    WHERE Ramo = ? 
      AND Simbolo = ? 
      AND SUBSTRING(Data, 7, 4) = ? 
      AND SUBSTRING(Data, 4, 2) BETWEEN ? AND ? 
  `;

  // Extrair o ano e os meses das datas
  const ano = data_inicio.slice(-4); // Pega os últimos 4 caracteres
  const mes_inicio = data_inicio.slice(3, 5); // Pega os caracteres do mês
  const mes_final = data_final.slice(3, 5); // Pega os caracteres do mês

  // Executar a query
  db.query(query, [ramo, simbolo, ano, mes_inicio, mes_final], (err, results) => {
    if (err) {
      console.error('Erro ao executar a consulta:', err);
      return res.status(500).send('Erro no servidor ao executar a consulta.');
    }

    res.json(results);
  });
});


app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
