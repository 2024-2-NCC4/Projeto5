const express = require('express');

const app = express();
const PORT = 3000;

app.get("/", (req, res) => {
    console.log("Endpoint de teste funcionando!")
    res.send("Servidor online!")
})

app.listen(PORT, () => {   
    console.log(`Servidor rodando na porta ${PORT}`)
})