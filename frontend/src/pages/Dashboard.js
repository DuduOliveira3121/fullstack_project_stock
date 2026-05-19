import { useState, useEffect } from 'react';

function Dashboard() {
  // Estado para armazenar os dados do dashboard
  const [stats, setStats] = useState(null);
  const [erro, setErro]   = useState('');

  // Carrega os dados ao montar o componente
  useEffect(() => {
    async function carregarDashboard() {
      const token = localStorage.getItem('token');
      const resposta = await fetch('http://localhost:5000/api/dashboard', {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (resposta.status === 401) {
        window.location.href = '/login';
        return;
      }

      const dados = await resposta.json();

      if (resposta.ok) {
        setStats(dados);
      } else {
        setErro(dados.erro || 'Erro ao carregar dashboard');
      }
    }

    carregarDashboard();
  }, []);

  // Exibe mensagem enquanto os dados carregam
  if (!stats && !erro) {
    return <div style={estilos.pagina}><p>Carregando...</p></div>;
  }

  return (
    <div style={estilos.pagina}>
      <div style={estilos.cabecalho}>
        <h1 style={estilos.titulo}>Dashboard</h1>
        <div style={estilos.acoes}>
          <a href="/produtos/novo" style={estilos.botaoLink}>+ Novo Produto</a>
          <a href="/vendas/nova"   style={estilos.botaoLink}>+ Nova Venda</a>
        </div>
      </div>

      {erro && <p style={estilos.erro}>{erro}</p>}

      {/* Cards com os indicadores principais */}
      {stats && (
        <>
          <div style={estilos.grade}>
            <div style={estilos.card}>
              <p style={estilos.labelCard}>Produtos Ativos</p>
              <p style={estilos.valorCard}>{stats.total_produtos}</p>
            </div>
            <div style={estilos.card}>
              <p style={estilos.labelCard}>Total em Estoque</p>
              <p style={estilos.valorCard}>{stats.total_estoque} un.</p>
            </div>
            <div style={estilos.card}>
              <p style={estilos.labelCard}>Total Vendido (R$)</p>
              <p style={estilos.valorCard}>R$ {Number(stats.total_vendido).toFixed(2)}</p>
            </div>
            <div style={estilos.card}>
              <p style={estilos.labelCard}>Ticket Médio</p>
              <p style={estilos.valorCard}>R$ {Number(stats.ticket_medio).toFixed(2)}</p>
            </div>
          </div>

          {/* Tabela de produtos com baixo estoque */}
          {stats.produtos_baixo_estoque && stats.produtos_baixo_estoque.length > 0 && (
            <div style={{ marginTop: '32px' }}>
              <h2 style={{ color: '#cc0000', marginBottom: '12px' }}>⚠ Produtos com Baixo Estoque (menos de 10)</h2>
              <table style={estilos.tabela}>
                <thead>
                  <tr>
                    <th style={estilos.th}>ID</th>
                    <th style={estilos.th}>Nome</th>
                    <th style={estilos.th}>Qtd. em Estoque</th>
                    <th style={estilos.th}>Preço</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.produtos_baixo_estoque.map((p) => (
                    <tr key={p.id}>
                      <td style={estilos.td}>{p.id}</td>
                      <td style={estilos.td}>{p.name}</td>
                      <td style={{ ...estilos.td, color: '#cc0000', fontWeight: 'bold' }}>{p.quantity}</td>
                      <td style={estilos.td}>R$ {Number(p.price).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}

// Estilos inline do Dashboard
const estilos = {
  pagina:     { padding: '32px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f5f6fa', minHeight: 'calc(100vh - 56px)' },
  cabecalho:  { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' },
  titulo:     { margin: 0, color: '#333' },
  acoes:      { display: 'flex', gap: '12px' },
  botaoLink:  { backgroundColor: '#007bff', color: '#fff', padding: '8px 16px', borderRadius: '4px', textDecoration: 'none', fontSize: '14px' },
  erro:       { backgroundColor: '#ffeaea', color: '#cc0000', padding: '12px', borderRadius: '4px', marginBottom: '16px' },
  grade:      { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px' },
  card:       { backgroundColor: '#fff', padding: '24px', borderRadius: '8px', boxShadow: '0 1px 4px rgba(0,0,0,0.1)', textAlign: 'center' },
  labelCard:  { margin: '0 0 8px', color: '#888', fontSize: '13px', textTransform: 'uppercase' },
  valorCard:  { margin: 0, fontSize: '28px', fontWeight: 'bold', color: '#333' },
  tabela:     { width: '100%', borderCollapse: 'collapse', backgroundColor: '#fff', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 1px 4px rgba(0,0,0,0.1)' },
  th:         { backgroundColor: '#f0f0f0', padding: '12px', textAlign: 'left', fontSize: '13px', color: '#555' },
  td:         { padding: '12px', borderBottom: '1px solid #eee', fontSize: '14px' },
};

export default Dashboard;
