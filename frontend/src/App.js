import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Importação de todas as páginas
import Login              from './pages/Login';
import Dashboard          from './pages/Dashboard';
import ListaProdutos      from './pages/ListaProdutos';
import CadastroProduto    from './pages/CadastroProduto';
import EditarProduto      from './pages/EditarProduto';
import ListaVendas        from './pages/ListaVendas';
import CadastroVenda      from './pages/CadastroVenda';
import ListaUsuarios      from './pages/ListaUsuarios';
import CadastroVendedor   from './pages/CadastroVendedor';
import AtivacaoVendedor   from './pages/AtivacaoVendedor';
import Navbar             from './components/Navbar';

// Componente que protege rotas que exigem autenticação
function RotaProtegida({ children }) {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" />;
  }
  // Renderiza a Navbar + o conteúdo da página protegida
  return (
    <>
      <Navbar />
      {children}
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rotas públicas — acessíveis sem login */}
        <Route path="/login"           element={<Login />} />
        <Route path="/usuarios/novo"   element={<CadastroVendedor />} />
        <Route path="/usuarios/ativar" element={<AtivacaoVendedor />} />

        {/* Rotas protegidas — redirecionam para /login se não autenticado */}
        <Route path="/"                element={<RotaProtegida><Dashboard /></RotaProtegida>} />
        <Route path="/produtos"        element={<RotaProtegida><ListaProdutos /></RotaProtegida>} />
        <Route path="/produtos/novo"   element={<RotaProtegida><CadastroProduto /></RotaProtegida>} />
        <Route path="/produtos/editar/:id" element={<RotaProtegida><EditarProduto /></RotaProtegida>} />
        <Route path="/vendas"          element={<RotaProtegida><ListaVendas /></RotaProtegida>} />
        <Route path="/vendas/nova"     element={<RotaProtegida><CadastroVenda /></RotaProtegida>} />
        <Route path="/usuarios"        element={<RotaProtegida><ListaUsuarios /></RotaProtegida>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
