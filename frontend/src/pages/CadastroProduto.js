import FormProduto from '../components/FormProduto';

// Página de cadastro de novo produto
// Renderiza apenas o formulário em modo "create"
function CadastroProduto() {
  return (
    <div style={{ backgroundColor: '#f5f6fa', minHeight: 'calc(100vh - 56px)', padding: '32px' }}>
      <FormProduto mode="create" />
    </div>
  );
}

export default CadastroProduto;
