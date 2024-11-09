// src/components/FilterForm.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FilterForm = ({ onSubmit }) => {
    const [ramo, setRamo] = useState('');
    const [simbolo, setSimbolo] = useState('');
    const [dataInicio, setDataInicio] = useState('');
    const [dataFinal, setDataFinal] = useState('');
    const [ramos, setRamos] = useState([]);
    const [simbolos, setSimbolos] = useState([]);

    // Buscar ramos e símbolos ao montar o componente
    useEffect(() => {
        const fetchOptions = async () => {
            try {
                const ramoResponse = await axios.get('http://localhost:3000/ramos');
                setRamos(ramoResponse.data);

                const simboloResponse = await axios.get('http://localhost:3000/simbolos');
                setSimbolos(simboloResponse.data);
            } catch (error) {
                console.error("Erro ao buscar opções de ramo e símbolo:", error);
            }
        };

        fetchOptions();
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ ramo, simbolo, dataInicio, dataFinal });
    };

    return (
        <form onSubmit={handleSubmit} className="filter-form">
            <div>
                <label>Ramo:</label>
                <select value={ramo} onChange={(e) => setRamo(e.target.value)} required>
                    <option value="">Selecione um ramo</option>
                    {ramos.map((option) => (
                        <option key={option} value={option}>{option}</option>
                    ))}
                </select>
            </div>
            <div>
                <label>Símbolo:</label>
                <select value={simbolo} onChange={(e) => setSimbolo(e.target.value)} required>
                    <option value="">Selecione um símbolo</option>
                    {simbolos.map((option) => (
                        <option key={option} value={option}>{option}</option>
                    ))}
                </select>
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
