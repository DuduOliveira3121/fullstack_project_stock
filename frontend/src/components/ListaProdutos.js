import { useState } from 'react';

// Componente que exibe a tabela de produtos e ações de editar/desativar
// Props:
//   produtos    — array de produtos vindo da API
//   onDesativar — callback chamado após desativar um produto
function ListaProdutos({ produtos, onDesativar }) {

  // Controla qual imagem está aberta no modal (null = fechado)
  const [imagemModal, setImagemModal] = useState(null);

  // Desativa o produto chamando PATCH /api/products/:id/inactivate
  async function handleDesativar(id) {
    if (!window.confirm('Deseja desativar este produto?')) return;

    const token = localStorage.getItem('token');
    const resposta = await fetch(`http://localhost:5000/api/products/${id}/inactivate`, {
      method:  'PATCH',
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (resposta.ok) {
      alert('Produto desativado!');
      // Notifica a página pai para recarregar a lista
      if (onDesativar) onDesativar();
    } else {
      const dados = await resposta.json();
      alert(dados.erro || 'Erro ao desativar produto');
    }
  }

  // Exibe mensagem quando não há produtos cadastrados
  if (!produtos || produtos.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>
        Nenhum produto cadastrado.
        <br />
        <a href="/produtos/novo" style={{ color: '#007bff' }}>Cadastrar primeiro produto</a>
      </div>
    );
  }

  return (
    <>
      {/* Modal de imagem ampliada — aparece ao clicar na miniatura */}
      {imagemModal && (
        <div style={estilos.overlay} onClick={() => setImagemModal(null)}>
          <div style={estilos.modalCaixa} onClick={(e) => e.stopPropagation()}>
            <button style={estilos.fechar} onClick={() => setImagemModal(null)}>✕</button>
            <img src={imagemModal.url} alt={imagemModal.nome} style={estilos.imagemGrande} />
            <p style={estilos.modalNome}>{imagemModal.nome}</p>
          </div>
        </div>
      )}

      <table style={estilos.tabela}>
      <thead>
        <tr>
          <th style={estilos.th}>Imagem</th>
          <th style={estilos.th}>ID</th>
          <th style={estilos.th}>Nome</th>
          <th style={estilos.th}>Preço</th>
          <th style={estilos.th}>Estoque</th>
          <th style={estilos.th}>Status</th>
          <th style={estilos.th}>Ações</th>
        </tr>
      </thead>
      <tbody>
        {/* Renderiza uma linha por produto */}
        {produtos.map((produto) => (
          <tr key={produto.id}>
            <td style={estilos.td}>
              {produto.image_url
                ? <img
                    src={produto.image_url}
                    alt={produto.name}
                    style={{ ...estilos.imagem, cursor: 'zoom-in' }}
                    onClick={() => setImagemModal({ url: produto.image_url, nome: produto.name })}
                    title="Clique para ampliar"
                  />
                : <div style={estilos.semImagem}>sem<br/>foto</div>
              }
            </td>
            <td style={estilos.td}>{produto.id}</td>
            <td style={estilos.td}>{produto.name}</td>
            <td style={estilos.td}>R$ {Number(produto.price).toFixed(2)}</td>
            <td style={estilos.td}>{produto.quantity}</td>
            <td style={estilos.td}>
              <span style={produto.status === 'ACTIVE' ? estilos.badgeAtivo : estilos.badgeInativo}>
                {produto.status === 'ACTIVE' ? 'Ativo' : 'Inativo'}
              </span>
            </td>
            <td style={estilos.td}>
              {/* Botão Editar navega para a página de edição */}
              <button
                onClick={() => { window.location.href = '/produtos/editar/' + produto.id; }}
                style={estilos.botaoEditar}
              >
                Editar
              </button>
              {/* Botão Desativar apenas aparece para produtos ativos */}
              {produto.status === 'ACTIVE' && (
                <button
                  onClick={() => handleDesativar(produto.id)}
                  style={estilos.botaoDesativar}
                >
                  Desativar
                </button>
              )}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    </>
  );
}

// Estilos inline da tabela de produtos
const estilos = {
  tabela:        { width: '100%', borderCollapse: 'collapse', backgroundColor: '#fff', borderRadius: '8px', overflow: 'hidden', boxShadow: '0 1px 4px rgba(0,0,0,0.1)' },
  imagem:        { width: '48px', height: '48px', objectFit: 'cover', borderRadius: '4px', display: 'block' },
  semImagem:     { width: '48px', height: '48px', backgroundColor: '#eee', borderRadius: '4px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '10px', color: '#aaa', textAlign: 'center' },
  th:            { backgroundColor: '#f0f0f0', padding: '12px', textAlign: 'left', fontSize: '13px', color: '#555' },
  td:            { padding: '12px', borderBottom: '1px solid #eee', fontSize: '14px' },
  badgeAtivo:    { backgroundColor: '#d4edda', color: '#155724', padding: '2px 8px', borderRadius: '12px', fontSize: '12px' },
  badgeInativo:  { backgroundColor: '#f8d7da', color: '#721c24', padding: '2px 8px', borderRadius: '12px', fontSize: '12px' },
  botaoEditar:   { marginRight: '8px', padding: '5px 12px', backgroundColor: '#ffc107', color: '#333', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' },
  botaoDesativar:{ padding: '5px 12px', backgroundColor: '#dc3545', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' },

  // Estilos do modal de imagem ampliada
  overlay:       { position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 },
  modalCaixa:    { backgroundColor: '#fff', borderRadius: '12px', padding: '24px', maxWidth: '90vw', maxHeight: '90vh', textAlign: 'center', position: 'relative' },
  imagemGrande:  { maxWidth: '70vw', maxHeight: '70vh', objectFit: 'contain', borderRadius: '8px', display: 'block', margin: '0 auto' },
  modalNome:     { marginTop: '12px', fontWeight: 'bold', fontSize: '16px', color: '#333' },
  fechar:        { position: 'absolute', top: '10px', right: '14px', background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer', color: '#888' },
};

export default ListaProdutos;
