import { useState, useEffect } from 'react';
import ListaProdutos from '../components/ListaProdutos';

// Página que exibe a lista completa de produtos do vendedor
function PageListaProdutos() {
  // Estado para armazenar os produtos carregados da API
  const [produtos, setProdutos] = useState([]);
  const [erro, setErro]         = useState('');

  // Carrega os produtos ao montar a página (e quando onDesativar for chamado)
  useEffect(() => {
    carregarProdutos();
  }, []);

  async function carregarProdutos() {
    const token = localStorage.getItem('token');
    const resposta = await fetch('http://localhost:5000/api/products', {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (resposta.status === 401) {
      window.location.href = '/login';
      return;
    }

    const dados = await resposta.json();
    if (resposta.ok) {
      setProdutos(dados);
    } else {
      setErro(dados.erro || 'Erro ao carregar produtos');
    }
  }

  return (
    <div style={estilos.pagina}>
      {/* Cabeçalho com título e botão de novo produto */}
      <div style={estilos.cabecalho}>
        <h1 style={estilos.titulo}>Produtos</h1>
        <a href="/produtos/novo" style={estilos.botaoNovo}>+ Novo Produto</a>
      </div>

      {erro && <p style={estilos.erro}>{erro}</p>}

      {/* Componente de tabela; passa callback para recarregar após desativar */}
      <ListaProdutos produtos={produtos} onDesativar={carregarProdutos} />
    </div>
  );
}

// Estilos inline da página de lista de produtos
const estilos = {
  pagina:    { padding: '32px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f5f6fa', minHeight: 'calc(100vh - 56px)' },
  cabecalho: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' },
  titulo:    { margin: 0, color: '#333' },
  botaoNovo: { backgroundColor: '#007bff', color: '#fff', padding: '8px 16px', borderRadius: '4px', textDecoration: 'none', fontSize: '14px' },
  erro:      { backgroundColor: '#ffeaea', color: '#cc0000', padding: '12px', borderRadius: '4px', marginBottom: '16px' },
};

export default PageListaProdutos;
