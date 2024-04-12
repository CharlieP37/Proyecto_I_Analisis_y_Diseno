import { BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import './App.css';
import { Layout } from './Pages/Layout';
import { MateriaPrimaEx } from './Pages/MateriaPrimaEx';
import { MateriaPrimaImp } from './Pages/MateriaPrimaImp';
import { ClientesImp } from './Pages/ClientesImp';
import { ClientesEx } from './Pages/ClientesEx';
import { CompaniaImp } from './Pages/CompaniaImp';
import { CompaniaEx } from './Pages/CompaniaEx';
import { DestinatarioImp } from './Pages/DestinatarioImp';
import { DestinatarioEx } from './Pages/DestinatarioEx';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' Component={Layout}/>
        <Route path='/materia-prima/exportar' element={<MateriaPrimaEx/>} />
        <Route path='/materia-prima/importar' element={<MateriaPrimaImp/>} />
        <Route path='/clientes/importar' element={<ClientesImp/>} />
        <Route path='/clientes/exportar' element={<ClientesEx/>} />
        <Route path='/compania/importar' element={<CompaniaImp/>} />
        <Route path='/compania/exportar' element={<CompaniaEx/>} />
        <Route path='/destinatario/importar' element={<DestinatarioImp/>} />
        <Route path='/destinatario/exportar' element={<DestinatarioEx/>} />
      </Routes>
    </Router>
  );
}

export default App;
