import { useState, useEffect } from 'react';

// Componente de formulário para registrar uma nova venda
function FormVenda() {
  // Controle dos campos do formulário
  const [productId, setProductId] = useState('');
  const [quantity,  setQuantity]  = useState('');

  // Lista de produtos disponíveis para o select
  const [produtos, setProdutos] = useState([]);

  // Carrega a lista de produtos ativos ao montar o componente
  useEffect(() => {
    async function carregarProdutos() {
      const token = localStorage.getItem('token');
      const resposta = await fetch('http://localhost:5000/api/products', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      const dados = await resposta.json();
      if (resposta.ok) {
        // Exibe apenas produtos com status ACTIVE
        setProdutos(dados.filter((p) => p.status === 'ACTIVE'));
      }
    }
    carregarProdutos();
  }, []);

  // Valida e envia a venda para a API
  async function handleSubmit() {
    if (!productId || !quantity) {
      alert('Selecione o produto e informe a quantidade');
      return;
    }
    if (parseInt(quantity, 10) <= 0) {
      alert('A quantidade deve ser maior que zero');
      return;
    }

    const token = localStorage.getItem('token');
    const resposta = await fetch('http://localhost:5000/api/sales', {
      method: 'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        product_id: parseInt(productId, 10),
        quantity:   parseInt(quantity, 10),
      }),
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      alert('Venda registrada com sucesso!');
      window.location.href = '/vendas';
    } else {
      alert(dados.erro || 'Erro ao registrar venda');
    }
  }

  return (
    <div style={estilos.container}>
      <h2 style={estilos.titulo}>Nova Venda</h2>

      {/* Seleção do produto */}
      <label style={estilos.label}>Produto *</label>
      <select
        value={productId}
        onChange={(e) => setProductId(e.target.value)}
        style={estilos.input}
      >
        <option value="">-- Selecione um produto --</option>
        {produtos.map((p) => (
          <option key={p.id} value={p.id}>
            {p.name} — R$ {Number(p.price).toFixed(2)} (estoque: {p.quantity})
          </option>
        ))}
      </select>

      {/* Quantidade a ser vendida */}
      <label style={estilos.label}>Quantidade *</label>
      <input
        type="number"
        min="1"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        style={estilos.input}
        placeholder="1"
      />

      {/* Botões de ação */}
      <div style={estilos.rodape}>
        <button onClick={handleSubmit} style={estilos.botaoSalvar}>Registrar Venda</button>
        <button onClick={() => window.location.href = '/vendas'} style={estilos.botaoCancelar}>Cancelar</button>
      </div>
    </div>
  );
}

// Estilos inline do formulário de venda
const estilos = {
  container:     { backgroundColor: '#fff', padding: '32px', borderRadius: '8px', boxShadow: '0 1px 4px rgba(0,0,0,0.1)', maxWidth: '520px', margin: '32px auto' },
  titulo:        { marginBottom: '24px', color: '#333' },
  label:         { display: 'block', marginBottom: '4px', color: '#555', fontWeight: 'bold', fontSize: '14px' },
  input:         { width: '100%', padding: '10px', marginBottom: '16px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' },
  rodape:        { display: 'flex', gap: '12px', marginTop: '8px' },
  botaoSalvar:   { flex: 1, padding: '12px', backgroundColor: '#28a745', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '15px' },
  botaoCancelar: { flex: 1, padding: '12px', backgroundColor: '#6c757d', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '15px' },
};

export default FormVenda;
