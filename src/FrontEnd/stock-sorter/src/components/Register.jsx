// src/components/Register.jsx
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Register.css';
import axios from 'axios';

function Register() {
    const [name, setName] = useState(''); // Estado para o nome
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState(''); // Estado para confirmar senha
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();

        // Verificação se as senhas coincidem
        if (password !== confirmPassword) {
            alert("As senhas não coincidem. Tente novamente.");
            return;
        }

        try {
            // Envia a solicitação de registro para o servidor
            await axios.post('http://localhost:3000/register', { name, email, password });
            alert("Cadastro bem-sucedido!");
            navigate('/');
        } catch (error) {
            console.error('Erro ao registrar:', error);
            alert("Erro ao cadastrar o usuário");
        }
    };

    return (
        <div className="register-container">
            <h2>Stock Sorter - Cadastro</h2>
            <form onSubmit={handleRegister}>
                <input 
                    type="text" 
                    placeholder="Nome" 
                    value={name} 
                    onChange={(e) => setName(e.target.value)} 
                    required 
                />
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
                <input 
                    type="password" 
                    placeholder="Repita a senha" 
                    value={confirmPassword} 
                    onChange={(e) => setConfirmPassword(e.target.value)} 
                    required 
                />
                <button type="submit">Cadastrar</button>
            </form>
            <p>Já tem uma conta? <Link to="/">Faça login</Link></p>
        </div>
    );
}

export default Register;
