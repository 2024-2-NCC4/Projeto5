// src/components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import DynamicChart from './DynamicChart';
import FilterForm from './FilterForm'; // Importar o FilterForm
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    // Função para aplicar os filtros
    const handleFilterSubmit = async ({ ramo, simbolo, dataInicio, dataFinal }) => {
        setLoading(true); // Mostra o carregamento enquanto busca os dados
        try {
            const params = {
                ramo,
                simbolo,
                data_inicio: dataInicio,
                data_final: dataFinal,
            };
            const response = await axios.get('http://localhost:3000/query', { params });
            console.log("Dados filtrados recebidos do backend:", response.data);
            setData(response.data);
        } catch (error) {
            console.error("Erro ao buscar dados filtrados do gráfico:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard">
            <h2>Gráfico de Fechamento</h2>
            {/* Renderizar o FilterForm e passar a função de filtro como prop */}
            <FilterForm onSubmit={handleFilterSubmit} />
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
