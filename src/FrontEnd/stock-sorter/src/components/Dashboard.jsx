// src/components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import DynamicChart from './DynamicChart';
import FilterForm from './FilterForm';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

const Dashboard = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filterMessage, setFilterMessage] = useState('');
    const [simboloSelecionado, setSimboloSelecionado] = useState('Apple Inc.');
    const navigate = useNavigate();

    // Função para aplicar os filtros
    const fetchFilteredData = async ({ ramo, simbolo, dataInicio, dataFinal }) => {
        setLoading(true);
        setFilterMessage('');
        setSimboloSelecionado(simbolo);
        try {
            const params = {
                ramo,
                simbolo,
                data_inicio: dataInicio,
                data_final: dataFinal,
            };
            const response = await axios.get('http://localhost:3000/query', { params });
            console.log("Dados filtrados recebidos do backend:", response.data);

            if (response.data.length === 0) {
                setFilterMessage(`Nenhum dado encontrado para ${simbolo} no período selecionado.`);
            }
            setData(response.data);
        } catch (error) {
            console.error("Erro ao buscar dados filtrados do gráfico:", error);
            setFilterMessage("Erro ao buscar dados. Por favor, tente novamente.");
        } finally {
            setLoading(false);
        }
    };

    // Função para buscar os dados iniciais da Apple
    useEffect(() => {
        const fetchDefaultData = async () => {
            setLoading(true);
            try {
                const defaultParams = {
                    ramo: 'Tecnologia', // Ramo da Apple
                    simbolo: 'Apple_Inc.',
                    data_inicio: '01.01.2022', // Altere conforme necessário
                    data_final: '31.12.2022', // Altere conforme necessário
                };
                console.log("Parâmetros padrão:", defaultParams); // Verifica os parâmetros no console
                const response = await axios.get('http://localhost:3000/query', { params: defaultParams });
                if (response.data.length === 0) {
                    setFilterMessage(`Nenhum dado encontrado para Apple Inc. no período padrão.`);
                }
                setData(response.data);
            } catch (error) {
                console.error("Erro ao buscar dados padrão do gráfico:", error);
                setFilterMessage("Erro ao carregar dados padrão.");
            } finally {
                setLoading(false);
            }
        };

        fetchDefaultData();
    }, []);

    // Função de logout
    const handleLogout = () => {
        navigate("/");
    };

    return (
        <div className="dashboard">
            <h2>Gráfico de Fechamento</h2>
            <button onClick={handleLogout} className="logout-button">Logout</button>
            <FilterForm onSubmit={fetchFilteredData} />
            {loading ? (
                <p>Carregando dados...</p>
            ) : data.length > 0 ? (
                <div className="chart-container">
                    <DynamicChart data={data} simbolo={simboloSelecionado} />
                </div>
            ) : (
                <p>{filterMessage || "Nenhum dado encontrado."}</p>
            )}
        </div>
    );
};

export default Dashboard;
