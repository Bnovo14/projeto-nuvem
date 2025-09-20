// script.js

async function buscarDados() {
    const elementoMensagem = document.getElementById('mensagem-backend');
    elementoMensagem.textContent = 'Buscando dados...';

    // Este é o endereço do back-end que você acabou de criar!
    const backend_url = '/api/dados';

    try {
        // Tenta fazer a "chamada" para o back-end
        const response = await fetch(backend_url);
        const dados = await response.json();
        
        // Se der certo, exibe a mensagem recebida do back-end na tela
        elementoMensagem.textContent = dados.message;

    } catch (error) {
        // Se der errado, avisa no console e na tela
        console.error('Falha ao buscar dados do back-end:', error);
        elementoMensagem.textContent = 'Erro ao conectar com o back-end.';
    }
}
