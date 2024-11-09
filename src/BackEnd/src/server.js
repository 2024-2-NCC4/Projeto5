require('dotenv').config();
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors'); // Importa o pacote de CORS

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors({
  origin: 'http://localhost:5173', // Substitua pela URL do seu frontend
  methods: ['GET', 'POST'], // Métodos permitidos
  allowedHeaders: ['Content-Type', 'Authorization'] // Cabeçalhos permitidos
}));


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

// Endpoint de teste
app.get('/', (req, res) => {
  res.send('Servidor online!');
});

// Endpoint para obter os primeiros e últimos 10 registros
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

// Endpoint para consulta filtrada
app.get('/query', (req, res) => {
  const { ramo, simbolo, data_inicio, data_final } = req.query;

  if (!ramo || !simbolo || !data_inicio || !data_final) {
    return res.status(400).send('Todos os parâmetros são necessários: ramo, simbolo, data_inicio e data_final.');
  }

  // Montar a query
  const query = `
    SELECT Data, Fechamento
    FROM tabela_projeto 
    WHERE Ramo = ? 
      AND Simbolo = ? 
      AND SUBSTRING(Data, 7, 4) = ?       -- Extrair o ano (posição 7 a 10)
      AND SUBSTRING(Data, 4, 2) BETWEEN ? AND ? -- Extrair o mês (posição 4 a 5)
  `;

  // Extrair o ano e os meses das datas com o novo formato dd-mm-yyyy
  const ano = data_inicio.slice(-4); // Últimos 4 caracteres para o ano
  const mes_inicio = data_inicio.slice(3, 5); // Caracteres do mês no formato dd-mm-yyyy
  const mes_final = data_final.slice(3, 5); // Caracteres do mês no formato dd-mm-yyyy

  // Executar a query
  db.query(query, [ramo, simbolo, ano, mes_inicio, mes_final], (err, results) => {
    if (err) {
      console.error('Erro ao executar a consulta:', err);
      return res.status(500).send('Erro no servidor ao executar a consulta.');
    }

    res.json(results);
  });
});

// Iniciar o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
