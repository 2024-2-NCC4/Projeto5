import React from 'react';
import './Login.css';

const Login = () => {
    return (
        <div className="login-container">
            <div className="login-box">
                <h2>Stock Sorter - Login</h2>
                <input type="email" placeholder="Email" />
                <input type="password" placeholder="Senha" />
                <button>Entrar</button>
                <p>Não tem uma conta? <a href="/register">Cadastre-se</a></p>
            </div>
        </div>
    );
};

export default Login;
