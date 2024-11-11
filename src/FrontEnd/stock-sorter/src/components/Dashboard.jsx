// src/components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import DynamicChart from './DynamicChart';
import FilterForm from './FilterForm';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = ({ onLogout }) => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchData = async (filters) => {
        const params = {
            ramo: filters.ramo || 'Tecnologia',
            simbolo: filters.simbolo || 'Apple_Inc.',
            data_inicio: filters.dataInicio || '01-01-2015',
            data_final: filters.dataFinal || '31-12-2023'
        };

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

    useEffect(() => {
        fetchData({});
    }, []);

    const handleFilter = (filters) => {
        setLoading(true);
        fetchData(filters);
    };

    return (
        <div className="dashboard">
            <button onClick={onLogout} className="logout-button">Logout</button>
            <h2>Gráfico de Fechamento</h2>
            <FilterForm onFilter={handleFilter} />
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
