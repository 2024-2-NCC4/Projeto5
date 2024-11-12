// src/components/DynamicChart.jsx
import React, { useEffect } from 'react';
import * as am5 from "@amcharts/amcharts5";
import * as am5xy from "@amcharts/amcharts5/xy";
import am5themes_Animated from "@amcharts/amcharts5/themes/Animated";

const DynamicChart = ({ data, simbolo }) => {
    useEffect(() => {
        if (data && data.length > 0) {
            am5.array.each(am5.registry.rootElements, function (root) {
                if (root.dom.id === "chartdiv") {
                    root.dispose();
                }
            });

            let root = am5.Root.new("chartdiv");
            root.setThemes([am5themes_Animated.new(root)]);

            let chart = root.container.children.push(
                am5xy.XYChart.new(root, {
                    panX: true,
                    panY: true,
                    wheelX: "zoomX", // Apenas o scroll fará o zoom
                    wheelY: "zoomX",
                    pinchZoomX: true,
                    layout: root.verticalLayout 
                })
            );

            let title = chart.children.unshift(
                am5.Label.new(root, {
                    text: `Preço de Fechamento Diário - ${simbolo || 'Indefinido'}`,
                    fontSize: 20,
                    fontWeight: "bold",
                    textAlign: "center",
                    x: am5.percent(50),
                    centerX: am5.percent(50),
                    paddingBottom: 10
                })
            );

            let xAxis = chart.xAxes.push(
                am5xy.DateAxis.new(root, {
                    baseInterval: { timeUnit: "day", count: 1 },
                    renderer: am5xy.AxisRendererX.new(root, {
                        minGridDistance: 50 
                    }),
                    tooltip: am5.Tooltip.new(root, {})
                })
            );

            let yAxis = chart.yAxes.push(
                am5xy.ValueAxis.new(root, {
                    renderer: am5xy.AxisRendererY.new(root, {
                        minGridDistance: 30 
                    })
                })
            );

            yAxis.children.unshift(
                am5.Label.new(root, {
                    rotation: -90,
                    text: "Preço de Fechamento (USD)",
                    y: am5.percent(50),
                    centerX: am5.percent(50),
                    fontSize: 15,
                    fontWeight: "500"
                })
            );

            let series = chart.series.push(
                am5xy.LineSeries.new(root, {
                    name: "Fechamento",
                    xAxis: xAxis,
                    yAxis: yAxis,
                    valueYField: "Fechamento",
                    valueXField: "Data",
                    tooltip: am5.Tooltip.new(root, {
                        labelText: "{valueY}",
                        dy: -5 
                    })
                })
            );

            const formattedData = data.map(item => ({
                Data: new Date(item.Data.split(".").reverse().join("-")).getTime(),
                Fechamento: parseFloat(item.Fechamento)
            }));
            series.data.setAll(formattedData);

            series.strokes.template.setAll({
                stroke: am5.color(0x007bff),
                strokeWidth: 2
            });

            series.bullets.push(() => {
                return am5.Bullet.new(root, {
                    sprite: am5.Circle.new(root, {
                        radius: 3,
                        fill: am5.color(0x007bff),
                        strokeWidth: 0
                    })
                });
            });

            // Configurar o cursor para pan com o clique do mouse e zoom com o scroll
            chart.set("cursor", am5xy.XYCursor.new(root, {
                behavior: "none", // Desativa o zoom no clique
                xAxis: xAxis
            }));

            series.fills.template.setAll({
                fillOpacity: 0.1,
                visible: true
            });

            series.appear(1000);
            chart.appear(1000, 100);

            return () => {
                root.dispose();
            };
        }
    }, [data, simbolo]);

    return <div id="chartdiv" style={{ width: "100%", height: "500px", minWidth: "600px" }}></div>;
};

export default DynamicChart;
