import { useState, useEffect } from 'react';

// Componente reutilizável para criar ou editar um produto
// Props:
//   mode    — "create" para novo produto, "edit" para editar
//   produto — objeto com dados do produto (somente em mode="edit")
function FormProduto({ mode, produto }) {
  // Controle dos campos do formulário
  const [name,      setName]      = useState('');
  const [price,     setPrice]     = useState('');
  const [quantity,  setQuantity]  = useState('');
  const [imageUrl,  setImageUrl]  = useState('');

  // Preenche os campos quando estiver em modo de edição
  useEffect(() => {
    if (mode === 'edit' && produto) {
      setName(produto.name || '');
      setPrice(produto.price || '');
      setQuantity(produto.quantity || '');
      setImageUrl(produto.image_url || '');
    }
  }, [mode, produto]);

  // Valida e envia o formulário
  async function handleSubmit() {
    if (!name || !price || !quantity) {
      alert('Preencha os campos obrigatórios: nome, preço e quantidade');
      return;
    }

    const token = localStorage.getItem('token');
    const corpo = {
      name,
      price:    parseFloat(price),
      quantity: parseInt(quantity, 10),
      image_url: imageUrl,
    };

    // Define URL e método conforme o modo
    const url    = mode === 'edit'
      ? `http://localhost:5000/api/products/${produto.id}`
      : 'http://localhost:5000/api/products';
    const metodo = mode === 'edit' ? 'PUT' : 'POST';

    const resposta = await fetch(url, {
      method:  metodo,
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(corpo),
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      alert(mode === 'edit' ? 'Produto atualizado!' : 'Produto cadastrado!');
      window.location.href = '/produtos';
    } else {
      alert(dados.erro || 'Erro ao salvar produto');
    }
  }

  return (
    <div style={estilos.container}>
      <h2 style={estilos.titulo}>
        {mode === 'edit' ? 'Editar Produto' : 'Novo Produto'}
      </h2>

      {/* Campo: Nome */}
      <label style={estilos.label}>Nome *</label>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={estilos.input}
        placeholder="Ex: Camiseta Básica"
      />

      {/* Campo: Preço */}
      <label style={estilos.label}>Preço (R$) *</label>
      <input
        type="number"
        step="0.01"
        min="0"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        style={estilos.input}
        placeholder="0.00"
      />

      {/* Campo: Quantidade em estoque */}
      <label style={estilos.label}>Quantidade em Estoque *</label>
      <input
        type="number"
        min="0"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
        style={estilos.input}
        placeholder="0"
      />

      {/* Campo: URL da imagem (opcional) */}
      <label style={estilos.label}>URL da Imagem</label>
      <input
        type="text"
        value={imageUrl}
        onChange={(e) => setImageUrl(e.target.value)}
        style={estilos.input}
        placeholder="https://..."
      />

      {/* Botões de ação */}
      <div style={estilos.rodape}>
        <button onClick={handleSubmit} style={estilos.botaoSalvar}>
          {mode === 'edit' ? 'Salvar Alterações' : 'Cadastrar Produto'}
        </button>
        <button onClick={() => window.location.href = '/produtos'} style={estilos.botaoCancelar}>
          Cancelar
        </button>
      </div>
    </div>
  );
}

// Estilos inline do formulário de produto
const estilos = {
  container:     { backgroundColor: '#fff', padding: '32px', borderRadius: '8px', boxShadow: '0 1px 4px rgba(0,0,0,0.1)', maxWidth: '520px', margin: '32px auto' },
  titulo:        { marginBottom: '24px', color: '#333' },
  label:         { display: 'block', marginBottom: '4px', color: '#555', fontWeight: 'bold', fontSize: '14px' },
  input:         { width: '100%', padding: '10px', marginBottom: '16px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' },
  rodape:        { display: 'flex', gap: '12px', marginTop: '8px' },
  botaoSalvar:   { flex: 1, padding: '12px', backgroundColor: '#28a745', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '15px' },
  botaoCancelar: { flex: 1, padding: '12px', backgroundColor: '#6c757d', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '15px' },
};

export default FormProduto;
