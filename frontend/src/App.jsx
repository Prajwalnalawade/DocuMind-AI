import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import UploadDocument from "./pages/UploadDocument";
import DocumentDetails from "./pages/DocumentDetails";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar">
        <div className="nav-brand">
          <Link to="/">DocuMind AI</Link>
        </div>

        <div className="nav-links">
          <Link to="/">Dashboard</Link>
          <Link to="/upload">Upload Document</Link>
        </div>
      </nav>

      <main className="app-container">
        <Routes>
          <Route path="/" element={<Dashboard />} />

          <Route
            path="/upload"
            element={<UploadDocument />}
          />

          <Route
            path="/documents/:id"
            element={<DocumentDetails />}
          />

          <Route
            path="*"
            element={<NotFound />}
          />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;