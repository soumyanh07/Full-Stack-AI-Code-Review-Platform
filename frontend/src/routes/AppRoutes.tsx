import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import RepositoryChatPage from "../pages/RepositoryChatPage";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route
          path="/repositories/:repositoryId/chat"
          element={<RepositoryChatPage />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;