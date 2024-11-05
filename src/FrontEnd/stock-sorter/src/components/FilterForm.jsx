// src/components/FilterForm.jsx
import React, { useState } from 'react';

const FilterForm = ({ onSubmit }) => {
    const [ramo, setRamo] = useState('');
    const [simbolo, setSimbolo] = useState('');
    const [dataInicio, setDataInicio] = useState('');
    const [dataFinal, setDataFinal] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ ramo, simbolo, dataInicio, dataFinal });
    };

    return (
        <form onSubmit={handleSubmit} className="filter-form">
            <div>
                <label>Ramo:</label>
                <input type="text" value={ramo} onChange={(e) => setRamo(e.target.value)} required />
            </div>
            <div>
                <label>Símbolo:</label>
                <input type="text" value={simbolo} onChange={(e) => setSimbolo(e.target.value)} required />
            </div>
            <div>
                <label>Data Início:</label>
                <input type="date" value={dataInicio} onChange={(e) => setDataInicio(e.target.value)} required />
            </div>
            <div>
                <label>Data Final:</label>
                <input type="date" value={dataFinal} onChange={(e) => setDataFinal(e.target.value)} required />
            </div>
            <button type="submit">Gerar Gráfico</button>
        </form>
    );
};

export default FilterForm;
