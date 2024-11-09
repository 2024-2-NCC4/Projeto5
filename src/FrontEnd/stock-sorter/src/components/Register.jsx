// src/components/Register.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Register.css';

function Register() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleRegister = (e) => {
        e.preventDefault();
        // Simulação de cadastro
        alert("Cadastro bem-sucedido!");
        navigate('/');
    };

    return (
        <div className="register-container">
            <h2>Stock Sorter - Cadastro</h2>
            <form onSubmit={handleRegister}>
                <input 
                    type="email" 
                    placeholder="Email" 
                    value={email} 
                    onChange={(e) => setEmail(e.target.value)} 
                    required 
                />
                <input 
                    type="password" 
                    placeholder="Senha" 
                    value={password} 
                    onChange={(e) => setPassword(e.target.value)} 
                    required 
                />
                <button type="submit">Cadastrar</button>
            </form>
            <p>Já tem uma conta? <Link to="/">Faça login</Link></p>
        </div>
    );
}

export default Register;
