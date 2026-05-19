import { useState } from 'react';

// Componente de formulário para cadastro de novo vendedor
// Campos mapeados com os nomes que o backend espera: nome, cnpj, email, celular, senha
function FormVendedor() {
  // Controle dos campos do formulário
  const [nome,     setNome]     = useState('');
  const [cnpj,     setCnpj]     = useState('');
  const [email,    setEmail]    = useState('');
  const [celular,  setCelular]  = useState('');
  const [senha,    setSenha]    = useState('');

  // Valida e envia o cadastro para a API
  async function handleSubmit() {
    if (!nome || !cnpj || !email || !celular || !senha) {
      alert('Preencha todos os campos obrigatórios');
      return;
    }

    const resposta = await fetch('http://localhost:5000/api/sellers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, cnpj, email, celular, senha }),
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      alert('Cadastro realizado! Verifique seu WhatsApp para ativar a conta.');
      window.location.href = '/usuarios/ativar';
    } else {
      alert(dados.erro || 'Erro ao cadastrar');
    }
  }

  return (
    <div style={estilos.container}>
      <h2 style={estilos.titulo}>Cadastro de Vendedor</h2>

      {/* Campo: Nome */}
      <label style={estilos.label}>Nome *</label>
      <input
        type="text"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        style={estilos.input}
        placeholder="Nome completo"
      />

      {/* Campo: CNPJ */}
      <label style={estilos.label}>CNPJ *</label>
      <input
        type="text"
        value={cnpj}
        onChange={(e) => setCnpj(e.target.value)}
        style={estilos.input}
        placeholder="00.000.000/0000-00"
      />

      {/* Campo: Email */}
      <label style={estilos.label}>Email *</label>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={estilos.input}
        placeholder="seu@email.com"
      />

      {/* Campo: Celular (usado para ativação via WhatsApp) */}
      <label style={estilos.label}>Celular (com DDD) *</label>
      <input
        type="text"
        value={celular}
        onChange={(e) => setCelular(e.target.value)}
        style={estilos.input}
        placeholder="11999999999"
      />

      {/* Campo: Senha */}
      <label style={estilos.label}>Senha *</label>
      <input
        type="password"
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
        style={estilos.input}
        placeholder="Mínimo 6 caracteres"
      />

      {/* Botão de envio */}
      <button onClick={handleSubmit} style={estilos.botao}>Cadastrar</button>

      <p style={{ textAlign: 'center', marginTop: '16px' }}>
        Já tem conta?{' '}
        <a href="/login" style={{ color: '#007bff' }}>Entrar</a>
      </p>
    </div>
  );
}

// Estilos inline do formulário de vendedor
const estilos = {
  container: { backgroundColor: '#fff', padding: '32px', borderRadius: '8px', boxShadow: '0 1px 4px rgba(0,0,0,0.1)', maxWidth: '480px', margin: '40px auto' },
  titulo:    { marginBottom: '24px', color: '#333', textAlign: 'center' },
  label:     { display: 'block', marginBottom: '4px', color: '#555', fontWeight: 'bold', fontSize: '14px' },
  input:     { width: '100%', padding: '10px', marginBottom: '16px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' },
  botao:     { width: '100%', padding: '12px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '15px' },
};

export default FormVendedor;
