// src/components/Dashboard.jsx

import React, { useState } from 'react';
import Sidebar from './sidebar';
import CandlestickChart from './grafico';

const Dashboard = () => {
    const [categoria, setCategoria] = useState('acoes');
    const [periodo, setPeriodo] = useState('6 meses');

    // Exemplo de dados de teste para o gráfico
    const data = [
        { date: new Date(2023, 0, 1), open: 200, high: 210, low: 198, close: 205 },
        { date: new Date(2023, 0, 2), open: 205, high: 215, low: 204, close: 210 },
        // Adicione mais dados conforme necessário
    ];

    return (
        <div className="dashboard">
            <Sidebar
                categoria={categoria}
                setCategoria={setCategoria}
                periodo={periodo}
                setPeriodo={setPeriodo}
            />
            <div className="charts-container">
                <CandlestickChart data={data} />
                {/* Adicione mais componentes de gráficos conforme necessário */}
            </div>
        </div>
    );
};

export default Dashboard;
