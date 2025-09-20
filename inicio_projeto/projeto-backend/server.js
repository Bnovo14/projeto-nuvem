// server.js

const express = require('express');
const cors = require('cors');
const app = express();

// A porta que o projeto exige para o back-end
const PORTA = 25000;

app.use(cors());

// Esta é a nossa "única rota" que o projeto exige
// Ela vai fornecer os dados para a página Web
app.get('/dados', (req, res) => {
  
  // Apenas devolve um objeto JSON com uma mensagem
  res.json({ 
    message: "Dados enviados pelo back-end com sucesso!"
  });
});

// Manda o servidor "escutar" por requisições na porta definida
app.listen(PORTA, () => {
  console.log(`Back-end está rodando na porta ${PORTA}`);
});