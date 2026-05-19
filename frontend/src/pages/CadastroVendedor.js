import FormVendedor from '../components/FormVendedor';

// Página de cadastro de novo vendedor — rota pública (/usuarios/novo)
function CadastroVendedor() {
  return (
    <div style={{ backgroundColor: '#f0f2f5', minHeight: '100vh', padding: '32px' }}>
      <FormVendedor />
    </div>
  );
}

export default CadastroVendedor;
