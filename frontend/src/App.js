import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Page1 from './Page1';
import Page2 from './Page2';
import Page3 from './Page3';

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <Routes>
        <Route path="/" element={<Page1 />} />
        <Route path="/submit" element={<Page2 />} />
        <Route path="/history" element={<Page3 />} />
      </Routes>
    </Router>
  );
}

export default App;