import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api";

export default function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await login(email, password);
      onLogin(); // обновляем state в App.jsx
      navigate("/resumes");
    } catch (err) {
      alert("Ошибка: " + err.message);
    }
  };

  return (
    <div className="p-6 max-w-sm mx-auto">
      <h1 className="text-2xl mb-4">Вход</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          className="border p-2 rounded"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="border p-2 rounded"
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="bg-blue-600 text-white p-2 rounded">Войти</button>
      </form>
    </div>
  );
}
