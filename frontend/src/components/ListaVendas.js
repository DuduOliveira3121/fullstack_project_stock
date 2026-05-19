// Componente que exibe a tabela de vendas realizadas
// Props:
//   vendas — array de vendas vindo da API
function ListaVendas({ vendas }) {

  // Formata a data ISO para exibição legível
  function formatarData(isoString) {
    if (!isoString) return '—';
    const d = new Date(isoString);
    return d.toLocaleString('pt-BR');
  }

  // Exibe mensagem quando não há vendas registradas
  if (!vendas || vendas.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>
        Nenhuma venda registrada.
        <br />
        <a href="/vendas/nova" style={{ color: '#007bff' }}>Registrar primeira venda</a>
      </div>
    );
  }

  return (
    <table style={estilos.tabela}>
      <thead>
        <tr>
          <th style={estilos.th}>ID</th>
          <th style={estilos.th}>Produto (ID)</th>
          <th style={estilos.th}>Quantidade</th>
          <th style={estilos.th}>Preço Unit.</th>
          <th style={estilos.th}>Total</th>
          <th style={estilos.th}>Data</th>
        </tr>
      </thead>
      <tbody>
        {/* Renderiza uma linha por venda */}
        {vendas.map((venda) => (
          <tr key={venda.id}>
            <td style={estilos.td}>{venda.id}</td>
            <td style={estilos.td}>{venda.product_id}</td>
            <td style={estilos.td}>{venda.quantity}</td>
            <td style={estilos.td}>R$ {Number(venda.unit_price).toFixed(2)}</td>
            <td style={estilos.td}>R$ {Number(venda.total_price).toFixed(2)}</td>
            <td style={estilos.td}>{formatarData(venda.sale_date)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Estilos inline da tabela de vendas
const estilos = {
  tabela: { width: '100%', borderCollapse: 'collapse', backgroundColor: '#fff', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 1px 4px rgba(0,0,0,0.1)' },
  th:     { backgroundColor: '#f0f0f0', padding: '12px', textAlign: 'left', fontSize: '13px', color: '#555' },
  td:     { padding: '12px', borderBottom: '1px solid #eee', fontSize: '14px' },
};

export default ListaVendas;
