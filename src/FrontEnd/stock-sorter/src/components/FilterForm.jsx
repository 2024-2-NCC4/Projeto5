// src/components/FilterForm.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './FilterForm.css';

const FilterForm = ({ onSubmit }) => {
    const [ramo, setRamo] = useState('');
    const [simbolo, setSimbolo] = useState('');
    const [dataInicioMes, setDataInicioMes] = useState('');
    const [dataInicioAno, setDataInicioAno] = useState('');
    const [dataFinalMes, setDataFinalMes] = useState('');
    const [dataFinalAno, setDataFinalAno] = useState('');
    const [ramos, setRamos] = useState([]);
    const [simbolos, setSimbolos] = useState([]);
    const [minYear, setMinYear] = useState(null);
    const [maxYear, setMaxYear] = useState(null);

    const months = [
        { value: '01', label: 'Jan' }, { value: '02', label: 'Fev' },
        { value: '03', label: 'Mar' }, { value: '04', label: 'Abr' },
        { value: '05', label: 'Mai' }, { value: '06', label: 'Jun' },
        { value: '07', label: 'Jul' }, { value: '08', label: 'Ago' },
        { value: '09', label: 'Set' }, { value: '10', label: 'Out' },
        { value: '11', label: 'Nov' }, { value: '12', label: 'Dez' },
    ];

    useEffect(() => {
        const fetchOptionsAndDates = async () => {
            try {
                const ramoResponse = await axios.get('http://localhost:3000/ramos');
                setRamos(ramoResponse.data);

                const minDateResponse = await axios.get('http://localhost:3000/min_date');
                const maxDateResponse = await axios.get('http://localhost:3000/max_date');

                // Extrair o ano das respostas de data
                setMinYear(parseInt(minDateResponse.data.slice(-4), 10));
                setMaxYear(parseInt(maxDateResponse.data.slice(-4), 10));
            } catch (error) {
                console.error("Erro ao buscar dados de filtros e datas:", error);
            }
        };

        fetchOptionsAndDates();
    }, []);

    // Função para buscar símbolos com base no ramo selecionado
    const fetchSimbolos = async (ramoSelecionado) => {
        try {
            const simboloResponse = await axios.get(`http://localhost:3000/simbolos/${ramoSelecionado}`);
            setSimbolos(simboloResponse.data);
        } catch (error) {
            console.error("Erro ao buscar símbolos:", error);
        }
    };

    // Quando o ramo é alterado, busca os símbolos associados a ele
    const handleRamoChange = (e) => {
        const selectedRamo = e.target.value;
        setRamo(selectedRamo);
        setSimbolo(''); // Reseta o símbolo selecionado quando o ramo muda
        if (selectedRamo) {
            fetchSimbolos(selectedRamo);
        } else {
            setSimbolos([]); // Limpa os símbolos se nenhum ramo estiver selecionado
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const dataInicio = `01.${dataInicioMes}.${dataInicioAno}`;
        const dataFinal = `01.${dataFinalMes}.${dataFinalAno}`;
        console.log("Filtros aplicados:", { ramo, simbolo, dataInicio, dataFinal });
        onSubmit({ ramo, simbolo, dataInicio, dataFinal });
    };
    

    return (
        <form onSubmit={handleSubmit} className="filter-form">
            <div>
                <label>Ramo:</label>
                <select value={ramo} onChange={handleRamoChange} required>
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
                <div style={{ display: 'flex', gap: '5px' }}>
                    <select value={dataInicioMes} onChange={(e) => setDataInicioMes(e.target.value)} required>
                        <option value="">Mês</option>
                        {months.map((month) => (
                            <option key={month.value} value={month.value}>{month.label}</option>
                        ))}
                    </select>
                    <select value={dataInicioAno} onChange={(e) => setDataInicioAno(e.target.value)} required>
                        <option value="">Ano</option>
                        {minYear && maxYear ? (
                            Array.from({ length: maxYear - minYear + 1 }, (_, i) => (
                                <option key={i} value={minYear + i}>{minYear + i}</option>
                            ))
                        ) : (
                            <option>Carregando...</option>
                        )}
                    </select>
                </div>
            </div>
            <div>
                <label>Data Final:</label>
                <div style={{ display: 'flex', gap: '5px' }}>
                    <select value={dataFinalMes} onChange={(e) => setDataFinalMes(e.target.value)} required>
                        <option value="">Mês</option>
                        {months.map((month) => (
                            <option key={month.value} value={month.value}>{month.label}</option>
                        ))}
                    </select>
                    <select value={dataFinalAno} onChange={(e) => setDataFinalAno(e.target.value)} required>
                        <option value="">Ano</option>
                        {minYear && maxYear ? (
                            Array.from({ length: maxYear - minYear + 1 }, (_, i) => (
                                <option key={i} value={minYear + i}>{minYear + i}</option>
                            ))
                        ) : (
                            <option>Carregando...</option>
                        )}
                    </select>
                </div>
            </div>
            <button type="submit">Aplicar Filtros</button>
        </form>
    );
};

export default FilterForm;
