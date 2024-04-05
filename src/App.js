import { BrowserRouter as Router, Routes, Route} from 'react-router-dom'
import logo from './logo.svg';
import './App.css';
import { Layout } from './Pages/Layout';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' Component={Layout}/>
      </Routes>
    </Router>
  );
}

export default App;
