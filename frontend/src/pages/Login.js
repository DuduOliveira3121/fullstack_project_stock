import { useState } from 'react';

function Login() {
  // Controle dos campos do formulário
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro]   = useState('');

  // Função chamada ao clicar em Entrar
  async function handleLogin() {
    if (!email || !senha) {
      alert('Preencha email e senha');
      return;
    }

    const resposta = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, senha }),
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      // Armazena o token JWT no localStorage para uso nas chamadas protegidas
      localStorage.setItem('token', dados.token);
      window.location.href = '/';
    } else {
      setErro(dados.erro || 'Erro ao fazer login');
    }
  }

  return (
    <div style={estilos.pagina}>
      <div style={estilos.card}>
        <h2 style={estilos.titulo}>Sistema de Estoque</h2>
        <h3 style={estilos.subtitulo}>Entrar</h3>

        {/* Exibe mensagem de erro quando houver */}
        {erro && <p style={estilos.erro}>{erro}</p>}

        <label style={estilos.label}>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={estilos.input}
          placeholder="seu@email.com"
        />

        <label style={estilos.label}>Senha</label>
        <input
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          style={estilos.input}
          placeholder="••••••••"
        />

        <button onClick={handleLogin} style={estilos.botao}>Entrar</button>

        <p style={{ textAlign: 'center', marginTop: '16px' }}>
          Não tem conta?{' '}
          <a href="/usuarios/novo" style={{ color: '#007bff' }}>Cadastre-se</a>
        </p>
      </div>
    </div>
  );
}

// Estilos inline do componente Login
const estilos = {
  pagina:    { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f0f2f5' },
  card:      { backgroundColor: '#fff', padding: '40px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.15)', width: '100%', maxWidth: '400px' },
  titulo:    { textAlign: 'center', color: '#333', marginBottom: '4px' },
  subtitulo: { textAlign: 'center', color: '#555', marginBottom: '24px', fontWeight: 'normal' },
  label:     { display: 'block', marginBottom: '4px', color: '#555', fontWeight: 'bold' },
  input:     { width: '100%', padding: '10px', marginBottom: '16px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' },
  botao:     { width: '100%', padding: '12px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '16px' },
  erro:      { backgroundColor: '#ffeaea', color: '#cc0000', padding: '10px', borderRadius: '4px', marginBottom: '16px', textAlign: 'center' },
};

export default Login;
