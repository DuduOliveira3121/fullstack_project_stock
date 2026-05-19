import { useState } from 'react';

// Página de ativação de conta via código enviado por WhatsApp — rota pública
function AtivacaoVendedor() {
  // Controle dos campos de ativação
  const [celular, setCelular] = useState('');
  const [codigo,  setCodigo]  = useState('');

  // Envia o código de ativação para a API
  async function handleAtivar() {
    if (!celular || !codigo) {
      alert('Informe o celular e o código de ativação');
      return;
    }

    const resposta = await fetch('http://localhost:5000/api/sellers/activate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ celular, codigo }),
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      alert('Conta ativada com sucesso! Faça login para continuar.');
      window.location.href = '/login';
    } else {
      alert(dados.erro || 'Código inválido ou expirado');
    }
  }

  return (
    <div style={estilos.pagina}>
      <div style={estilos.card}>
        <h2 style={estilos.titulo}>Ativar Conta</h2>
        <p style={estilos.descricao}>
          Digite o código enviado via WhatsApp para o número cadastrado.
        </p>

        {/* Campo: Celular */}
        <label style={estilos.label}>Celular (com DDD) *</label>
        <input
          type="text"
          value={celular}
          onChange={(e) => setCelular(e.target.value)}
          style={estilos.input}
          placeholder="11999999999"
        />

        {/* Campo: Código de ativação */}
        <label style={estilos.label}>Código de Ativação *</label>
        <input
          type="text"
          value={codigo}
          onChange={(e) => setCodigo(e.target.value)}
          style={estilos.input}
          placeholder="Ex: 123456"
        />

        <button onClick={handleAtivar} style={estilos.botao}>Ativar Conta</button>

        <p style={{ textAlign: 'center', marginTop: '16px' }}>
          <a href="/login" style={{ color: '#007bff' }}>Voltar ao Login</a>
        </p>
      </div>
    </div>
  );
}

// Estilos inline da página de ativação
const estilos = {
  pagina:    { display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', backgroundColor: '#f0f2f5' },
  card:      { backgroundColor: '#fff', padding: '40px', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.15)', width: '100%', maxWidth: '420px' },
  titulo:    { textAlign: 'center', color: '#333', marginBottom: '8px' },
  descricao: { textAlign: 'center', color: '#777', marginBottom: '24px', fontSize: '14px' },
  label:     { display: 'block', marginBottom: '4px', color: '#555', fontWeight: 'bold', fontSize: '14px' },
  input:     { width: '100%', padding: '10px', marginBottom: '16px', borderRadius: '4px', border: '1px solid #ccc', boxSizing: 'border-box', fontSize: '14px' },
  botao:     { width: '100%', padding: '12px', backgroundColor: '#28a745', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '15px' },
};

export default AtivacaoVendedor;
