import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:3000/login', { email, password });
            navigate('/home'); // Redireciona para a tela inicial após o login
        } catch (error) {
            console.error('Erro ao fazer login:', error);
            alert("Email ou senha incorretos");
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2>Stock Sorter - Login</h2>
                <input 
                    type="email" 
                    placeholder="Email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input 
                    type="password" 
                    placeholder="Senha" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button onClick={handleLogin}>Entrar</button>
                <p>Não tem uma conta? <a href="/register">Cadastre-se</a></p>
            </div>
        </div>
    );
};

export default Login;
