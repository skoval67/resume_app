import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Login from "./pages/Login";
import Resumes from "./pages/Resumes";
import ResumeDetail from "./pages/ResumeDetail";

// функция для получения токена из cookie
function getTokenFromCookie() {
  const match = document.cookie.match(new RegExp('(^| )access_token=([^;]+)'));
  return match ? match[2] : null;
}

export default function App() {
  const [token, setToken] = useState(getTokenFromCookie()); // читаем токен из куки

  const handleLogin = () => {
    setToken(getTokenFromCookie());
  };

  // Следим за изменением куки каждые 500 мс
  useEffect(() => {
    const interval = setInterval(() => {
      const newToken = getTokenFromCookie();
      if (newToken !== token) {
        setToken(newToken);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [token]);
  
return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        {token ? (
          <>
            <Route path="/resumes" element={<Resumes />} />
            <Route path="/resumes/:id" element={<ResumeDetail />} />
            <Route path="*" element={<Navigate to="/resumes" />} />
          </>
        ) : (
          <Route path="*" element={<Navigate to="/login" />} />
        )}
      </Routes>
    </BrowserRouter>
  );
}
