import { useState } from "react";
import api from "../api/axios";
import { useAuthStore } from "../store/authStore";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
  const login = useAuthStore((state) => state.login);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      login(
        response.data.access_token,
        { id: 0, email }
      );

      navigate("/dashboard");

    } catch (error) {
      console.error(error);
      const message = error instanceof Error ? error.message : "Unknown error";
      alert(`Login failed: ${message}`);
    }
  };


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">

      <form
        onSubmit={handleLogin}
        className="bg-gray-800 p-8 rounded-xl w-96"
      >

        <h1 className="text-3xl text-white font-bold mb-6">
          Login
        </h1>

        <input
          className="w-full p-3 mb-4 rounded bg-gray-700 text-white"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
        />

        <input
          className="w-full p-3 mb-6 rounded bg-gray-700 text-white"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
        />


        <button
          className="w-full bg-green-600 text-white p-3 rounded"
        >
          Login
        </button>

      </form>

    </div>
  );
}

export default Login;