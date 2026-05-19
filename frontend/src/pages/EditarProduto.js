import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import FormProduto from '../components/FormProduto';

// Página de edição de produto
// Carrega os dados do produto pelo ID da URL e passa para o FormProduto
function EditarProduto() {
  const { id }            = useParams();
  const [produto, setProduto] = useState(null);
  const [erro, setErro]       = useState('');

  // Busca o produto pelo ID ao montar a página
  useEffect(() => {
    async function carregarProduto() {
      const token = localStorage.getItem('token');
      const resposta = await fetch(`http://localhost:5000/api/products/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (resposta.status === 401) {
        window.location.href = '/login';
        return;
      }

      const dados = await resposta.json();
      if (resposta.ok) {
        setProduto(dados);
      } else {
        setErro(dados.erro || 'Produto não encontrado');
      }
    }

    carregarProduto();
  }, [id]);

  return (
    <div style={{ backgroundColor: '#f5f6fa', minHeight: 'calc(100vh - 56px)', padding: '32px' }}>
      {erro && <p style={{ color: '#cc0000', textAlign: 'center' }}>{erro}</p>}

      {/* Exibe o formulário somente quando o produto já foi carregado */}
      {produto
        ? <FormProduto mode="edit" produto={produto} />
        : !erro && <p style={{ textAlign: 'center' }}>Carregando produto...</p>
      }
    </div>
  );
}

export default EditarProduto;
