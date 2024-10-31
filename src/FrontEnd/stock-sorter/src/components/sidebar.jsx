// src/components/Sidebar.jsx

import React from 'react';

const Sidebar = ({ categoria, setCategoria, periodo, setPeriodo }) => {
    return (
        <div className="sidebar">
            <h3>Filtros</h3>
            <label>
                Categoria:
                <select value={categoria} onChange={(e) => setCategoria(e.target.value)}>
                    <option value="acoes">Ações</option>
                    <option value="ouro">Ouro</option>
                    <option value="petroleo">Petróleo</option>
                    <option value="indices">Índices</option>
                </select>
            </label>
            <label>
                Período:
                <select value={periodo} onChange={(e) => setPeriodo(e.target.value)}>
                    <option value="6 meses">Últimos 6 Meses</option>
                    <option value="1 ano">Último Ano</option>
                    <option value="5 anos">Últimos 5 Anos</option>
                </select>
            </label>
        </div>
    );
};

export default Sidebar;
