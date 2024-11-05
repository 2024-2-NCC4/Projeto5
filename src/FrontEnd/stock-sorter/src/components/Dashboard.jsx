// src/components/Dashboard.jsx
import React, { useState } from 'react';
import FilterForm from './FilterForm';
import DynamicChart from './DynamicChart';
import axios from 'axios';

const Dashboard = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleFilterSubmit = async (filters) => {
        setLoading(true);
        try {
            const response = await axios.get('http://localhost:3000/query', {
                params: {
                    ramo: filters.ramo,
                    simbolo: filters.simbolo,
                    data_inicio: filters.dataInicio,
                    data_final: filters.dataFinal,
                },
            });
            setData(response.data);
        } catch (error) {
            console.error("Erro ao buscar dados:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard">
            <h2>Dashboard de Análise</h2>
            <FilterForm onSubmit={handleFilterSubmit} />
            {loading ? (
                <p>Carregando dados...</p>
            ) : data.length > 0 ? (
                <DynamicChart data={data} />
            ) : (
                <p>Selecione os filtros e clique em "Gerar Gráfico" para ver os dados.</p>
            )}
        </div>
    );
};

export default Dashboard;
