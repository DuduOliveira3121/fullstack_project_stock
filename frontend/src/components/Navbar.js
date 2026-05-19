function Navbar() {
  // Função de logout: remove o token e redireciona para a tela de login
  function handleLogout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
  }

  return (
    <nav style={estilos.nav}>
      <span style={estilos.marca}>📦 Estoque</span>

      {/* Links de navegação principal */}
      <div style={estilos.links}>
        <a href="/"             style={estilos.link}>Dashboard</a>
        <a href="/produtos"     style={estilos.link}>Produtos</a>
        <a href="/vendas"       style={estilos.link}>Vendas</a>
        <a href="/usuarios"     style={estilos.link}>Usuários</a>
      </div>

      <button onClick={handleLogout} style={estilos.botaoSair}>Sair</button>
    </nav>
  );
}

// Estilos inline da barra de navegação
const estilos = {
  nav:      { display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#1a1a2e', padding: '0 24px', height: '56px' },
  marca:    { color: '#fff', fontWeight: 'bold', fontSize: '18px' },
  links:    { display: 'flex', gap: '24px' },
  link:     { color: '#ccc', textDecoration: 'none', fontSize: '14px' },
  botaoSair:{ backgroundColor: 'transparent', border: '1px solid #ccc', color: '#ccc', padding: '6px 14px', borderRadius: '4px', cursor: 'pointer', fontSize: '13px' },
};

export default Navbar;
