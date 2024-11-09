// src/components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import DynamicChart from './DynamicChart';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = ({ onLogout }) => { // Recebe a função de logout como prop
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const params = {
            ramo: 'Tecnologia',
            simbolo: 'Apple_Inc.',
            data_inicio: '01-01-2015',
            data_final: '31-12-2023'
        };

        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:3000/query', { params });
                console.log("Dados recebidos do backend:", response.data);
                setData(response.data);
            } catch (error) {
                console.error("Erro ao buscar dados do gráfico:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return (
        <div className="dashboard">
            <h2>Gráfico de Fechamento - Tecnologia</h2>
            <button onClick={onLogout} className="logout-button">Logout</button> {/* Botão de logout */}
            {loading ? (
                <p>Carregando dados...</p>
            ) : data.length > 0 ? (
                <div className="chart-container">
                    <DynamicChart data={data} />
                </div>
            ) : (
                <p>Nenhum dado encontrado.</p>
            )}
        </div>
    );
};

export default Dashboard;
