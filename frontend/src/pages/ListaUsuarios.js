// Página de usuários — exibe links de ação pois não há endpoint de listagem
function ListaUsuarios() {
  return (
    <div style={estilos.pagina}>
      <h1 style={estilos.titulo}>Usuários</h1>

      <div style={estilos.grade}>
        {/* Card: cadastrar novo vendedor */}
        <div style={estilos.card}>
          <h3 style={estilos.cardTitulo}>Cadastrar Vendedor</h3>
          <p style={estilos.cardDescricao}>
            Registre um novo vendedor no sistema. Após o cadastro, o vendedor
            receberá um código de ativação via WhatsApp.
          </p>
          <a href="/usuarios/novo" style={estilos.botao}>Novo Cadastro</a>
        </div>

        {/* Card: ativar conta */}
        <div style={estilos.card}>
          <h3 style={estilos.cardTitulo}>Ativar Conta</h3>
          <p style={estilos.cardDescricao}>
            Informe o celular e o código recebido via WhatsApp para ativar
            uma conta recém-cadastrada.
          </p>
          <a href="/usuarios/ativar" style={{ ...estilos.botao, backgroundColor: '#28a745' }}>Ativar Conta</a>
        </div>
      </div>
    </div>
  );
}

// Estilos inline da página de usuários
const estilos = {
  pagina:       { padding: '32px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f5f6fa', minHeight: 'calc(100vh - 56px)' },
  titulo:       { marginBottom: '24px', color: '#333' },
  grade:        { display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '24px', maxWidth: '680px' },
  card:         { backgroundColor: '#fff', padding: '28px', borderRadius: '8px', boxShadow: '0 1px 4px rgba(0,0,0,0.1)' },
  cardTitulo:   { margin: '0 0 12px', color: '#333' },
  cardDescricao:{ color: '#666', fontSize: '14px', marginBottom: '20px', lineHeight: '1.5' },
  botao:        { display: 'inline-block', backgroundColor: '#007bff', color: '#fff', padding: '10px 20px', borderRadius: '4px', textDecoration: 'none', fontSize: '14px' },
};

export default ListaUsuarios;
