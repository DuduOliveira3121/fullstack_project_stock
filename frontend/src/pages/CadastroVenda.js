import FormVenda from '../components/FormVenda';

// Página de registro de nova venda
function CadastroVenda() {
  return (
    <div style={{ backgroundColor: '#f5f6fa', minHeight: 'calc(100vh - 56px)', padding: '32px' }}>
      <FormVenda />
    </div>
  );
}

export default CadastroVenda;
