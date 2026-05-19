import { useState, useEffect } from 'react';
import ListaVendas from '../components/ListaVendas';

// Página que exibe o histórico de vendas do vendedor
function PageListaVendas() {
  // Estado para armazenar as vendas carregadas da API
  const [vendas, setVendas] = useState([]);
  const [erro, setErro]     = useState('');

  // Carrega as vendas ao montar a página
  useEffect(() => {
    async function carregarVendas() {
      const token = localStorage.getItem('token');
      const resposta = await fetch('http://localhost:5000/api/sales', {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (resposta.status === 401) {
        window.location.href = '/login';
        return;
      }

      const dados = await resposta.json();
      if (resposta.ok) {
        setVendas(dados);
      } else {
        setErro(dados.erro || 'Erro ao carregar vendas');
      }
    }

    carregarVendas();
  }, []);

  return (
    <div style={estilos.pagina}>
      {/* Cabeçalho com título e botão de nova venda */}
      <div style={estilos.cabecalho}>
        <h1 style={estilos.titulo}>Vendas</h1>
        <a href="/vendas/nova" style={estilos.botaoNovo}>+ Nova Venda</a>
      </div>

      {erro && <p style={estilos.erro}>{erro}</p>}

      {/* Componente de tabela de vendas */}
      <ListaVendas vendas={vendas} />
    </div>
  );
}

// Estilos inline da página de lista de vendas
const estilos = {
  pagina:    { padding: '32px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f5f6fa', minHeight: 'calc(100vh - 56px)' },
  cabecalho: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' },
  titulo:    { margin: 0, color: '#333' },
  botaoNovo: { backgroundColor: '#28a745', color: '#fff', padding: '8px 16px', borderRadius: '4px', textDecoration: 'none', fontSize: '14px' },
  erro:      { backgroundColor: '#ffeaea', color: '#cc0000', padding: '12px', borderRadius: '4px', marginBottom: '16px' },
};

export default PageListaVendas;
