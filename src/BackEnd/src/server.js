require('dotenv').config();
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors'); // Importa o pacote de CORS
const bcrypt = require('bcrypt'); // para proteger as senhas
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors({
  origin: 'http://localhost:5173', // Substitua pela URL do seu frontend
  methods: ['GET', 'POST'], // Métodos permitidos
  allowedHeaders: ['Content-Type', 'Authorization'] // Cabeçalhos permitidos
}));

app.use(express.json());

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

/*
// Conectar ao banco de dados
db.connect((err) => {
  if (err) {
    console.error('Erro ao conectar ao MySQL:', err);
    return;
  }
  console.log('Conectado ao MySQL!');
});
*/

db.on('error', (err) => {
  console.error('Erro na conexão com o banco de dados:', err);
});


// Endpoint de teste
app.get('/', (req, res) => {
  res.send('Servidor online!');
});

//Endpoints de Login e Registro

// Endpoint de Registro
app.post('/register', async (req, res) => {
  const { name, email, password } = req.body;
  
  if (!name || !email || !password) {
    return res.status(400).json({ message: 'Nome, email e senha são necessários' });
  }

  // Criptografar a senha
  const hashedPassword = await bcrypt.hash(password, 10);

  const query = `INSERT INTO Usuarios (Nome, Email, Senha) VALUES (?, ?, ?)`;
  db.query(query, [name, email, hashedPassword], (err, result) => {
    if (err) {
      console.error('Erro ao registrar usuário:', err);
      return res.status(500).json({ message: 'Erro ao registrar o usuário' });
    }
    res.status(201).json({ message: 'Usuário registrado com sucesso' });
  });
});


// Endpoint de Login
app.post('/login', (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: 'Email e senha são necessários' });
  }

  const query = `SELECT * FROM Usuarios WHERE Email = ?`;
  db.query(query, [email], async (err, results) => {
    if (err) {
      console.error('Erro ao buscar usuário:', err);
      return res.status(500).json({ message: 'Erro no servidor' });
    }

    if (results.length === 0) {
      return res.status(401).json({ message: 'Credenciais inválidas' });
    }

    // Comparar a senha fornecida com a senha armazenada
    const isMatch = await bcrypt.compare(password, results[0].Senha);

    if (!isMatch) {
      return res.status(401).json({ message: 'Credenciais inválidas' });
    }

    res.json({ message: 'Login bem-sucedido', userId: results[0].Id });
  });
});

// Endpoint para obter os primeiros e últimos 10 registros
app.get('/dev', (req, res) => {
  const firstTenQuery = 'SELECT * FROM Dados ORDER BY id ASC LIMIT 10';
  const lastTenQuery = 'SELECT * FROM Dados ORDER BY id DESC LIMIT 10';

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

// Endpoint para obter a data mínima considerando o formato de texto dd.mm.yyyy
app.get('/min_date', (req, res) => {
  const query = `
    SELECT Data AS minDate 
    FROM Dados 
    ORDER BY STR_TO_DATE(Data, '%d.%m.%Y') ASC 
    LIMIT 1
  `; // Usamos STR_TO_DATE para converter a coluna de texto no formato correto


  db.query(query, (err, result) => {
    if (err) {
      console.error('Erro ao obter a data mínima:', err);
      res.status(500).send('Erro no servidor');
      return;
    }
    res.json(result[0].minDate);
  });
});


// Endpoint para obter a data máxima considerando o formato de texto dd.mm.yyyy
app.get('/max_date', (req, res) => {
  const query = `
    SELECT Data AS maxDate 
    FROM Dados 
    ORDER BY STR_TO_DATE(Data, '%d.%m.%Y') DESC 
    LIMIT 1
  `; // Usamos STR_TO_DATE para converter a coluna de texto no formato correto

  db.query(query, (err, result) => {
    if (err) {
      console.error('Erro ao obter a data máxima:', err);
      res.status(500).send('Erro no servidor');
      return;
    }
    res.json(result[0].maxDate);
  });
});



// Endpoint para obter os valores distintos de Ramo
app.get('/ramos', (req, res) => {
  const query = 'SELECT DISTINCT Ramo FROM Dados';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Erro ao buscar ramos:', err);
      return res.status(500).send('Erro ao buscar ramos');
    }
    const ramos = results.map(row => row.Ramo); // Extrai os valores de Ramo
    res.json(ramos);
  });
});

// Endpoint para obter os valores distintos de Simbolo
app.get('/simbolos', (req, res) => {
  const query = 'SELECT DISTINCT Simbolo FROM Dados';
  db.query(query, (err, results) => {
    if (err) {
      console.error('Erro ao buscar símbolos:', err);
      return res.status(500).send('Erro ao buscar símbolos');
    }
    const simbolos = results.map(row => row.Simbolo); // Extrai os valores de Simbolo
    res.json(simbolos);
  });
});


// Adicione este endpoint ao seu arquivo server.js
app.get('/simbolos/:ramo', (req, res) => {
  const { ramo } = req.params;

  const query = 'SELECT DISTINCT Simbolo FROM Dados WHERE Ramo = ?';
  db.query(query, [ramo], (err, results) => {
    if (err) {
      console.error('Erro ao buscar símbolos:', err);
      return res.status(500).json({ message: 'Erro ao buscar símbolos' });
    }

    const simbolos = results.map(row => row.Simbolo);
    res.json(simbolos);
  });
});


// Endpoint para consulta filtrada
app.get('/query', (req, res) => {
  const { ramo, simbolo, data_inicio, data_final } = req.query;

  if (!ramo || !simbolo || !data_inicio || !data_final) {
      return res.status(400).send('Todos os parâmetros são necessários: ramo, simbolo, data_inicio e data_final.');
  }

  // Montar a query usando STR_TO_DATE para comparar as datas corretamente
  const query = `
      SELECT Data, Fechamento, Simbolo, Ramo
      FROM Dados 
      WHERE Ramo = ? 
        AND Simbolo = ? 
        AND STR_TO_DATE(Data, '%d.%m.%Y') BETWEEN STR_TO_DATE(?, '%d.%m.%Y') AND STR_TO_DATE(?, '%d.%m.%Y')
  `;

  // Executar a query
  db.query(query, [ramo, simbolo, data_inicio, data_final], (err, results) => {
      if (err) {
          console.error('Erro ao executar a consulta:', err);
          return res.status(500).send('Erro no servidor ao executar a consulta.');
      }

      return res.json(results);
  });
});


app.get('/query2', (req, res) => {
  const { ramo, simbolos, data_inicio, data_final } = req.query;

  if (!ramo || !simbolos || !data_inicio || !data_final) {
      return res.status(400).send('Todos os parâmetros são necessários: ramo, simbolos, data_inicio e data_final.');
  }

  // Converter 'simbolos' em um array se for uma string
  let listaSimbolos = [];
  if (typeof simbolos === 'string') {
      listaSimbolos = simbolos.split(',');
  } else if (Array.isArray(simbolos)) {
      listaSimbolos = simbolos;
  } else {
      return res.status(400).send('O parâmetro simbolos deve ser uma string ou um array.');
  }

  // Criar placeholders para os símbolos
  const placeholders = listaSimbolos.map(() => '?').join(', ');

  const query = `
      SELECT Data, Fechamento_Padronizado, Simbolo, Ramo
      FROM Dados 
      WHERE Ramo = ? 
        AND Simbolo IN (${placeholders})
        AND STR_TO_DATE(Data, '%d.%m.%Y') BETWEEN STR_TO_DATE(?, '%d.%m.%Y') AND STR_TO_DATE(?, '%d.%m.%Y')
  `;

  const params = [ramo, ...listaSimbolos, data_inicio, data_final];

  db.query(query, params, (err, results) => {
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
