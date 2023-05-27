function displaySentimentFormality(jsonResult){
    const tripleGraphData = extractTripleData(jsonResult);
    const divID = "sentimentFormalityGraph";
    cleanCanvas(divID);
    am5.ready(function() {
        const root = am5
            .Root
            .new(divID);
        root.setThemes([am5themes_Animated.new(root)]);
        
        const tripleSettings = {
            type:am5xy.XYChart.new(root, {
                panX: true,
                panY: false,
                wheelX: "none",
                wheelY: "true",
                arrangeTooltips: false
            }),
            xRenderer:am5xy
                .AxisRendererX
                .new(root, { minGridDistance: 70 }),
            xRendererSettings:{
                multiLocation: 0.5,
                location: 0.5,
                centerY: am5.p50,
                centerX: am5.p50,
                paddingTop: 10
            },
            background:am5.Rectangle.new(root, {
                fillOpacity: 1,
                fill: root.interfaceColors.get("background")
            }),
        };

        const chart = root
            .container
            .children
            .push(tripleSettings.type);
        chart
            .leftAxesContainer
            .set("layout", root.verticalLayout);

        const xRenderer = tripleSettings.xRenderer;
        xRenderer
            .labels
            .template
            .setAll(tripleSettings.xRendererSettings);
        xRenderer
            .grid
            .template
            .set("location", 0.5);
        
        const xAxis = chart
            .xAxes
            .push(
                am5xy.CategoryAxis.new(root, {
                    maxDeviation:0.3,
                    categoryField: "turn",
                    tooltip: am5.Tooltip.new(root, {}),
                    renderer: xRenderer
                })
            );
        xAxis
            .data
            .setAll(tripleGraphData);
        
        const bulletTemplate = am5.Template.new(root, {});
        bulletTemplate
            .events
            .on("click", function(event) {
                scrollToUtterance(event.target._dataItem.dataContext.turn-1)
            });

        function createLineSeries(field, margin) {
            const yAxis = chart
                .yAxes
                .push(
                    am5xy.ValueAxis.new(root, {
                        renderer: am5xy.AxisRendererY.new(root, {}),
                        tooltip: am5.Tooltip.new(root, {animationDuration: 0}),
                    x: am5.p100,
                    centerX: am5.p100,
                    marginTop: margin
                    })
                );
            yAxis
                .axisHeader
                .set("background", tripleSettings.background);
            yAxis
                .children
                .moveValue(am5.Label.new(root, {
                    rotation: -90,
                    text: field,
                    y: am5.p50,
                    centerX: am5.p50
                }), 0);
            
            let series = chart.series.push(
                am5xy.LineSeries.new(root, {
                    xAxis: xAxis,
                    yAxis: yAxis,
                    valueYField: field,
                    categoryXField: "turn", 
                    legendValueText: "{valueY}",
                    sequencedInterpolation: true,
                    tooltip: am5.Tooltip.new(root, {
                        pointerOrientation: "vertical",
                        labelText: "{valueY}"
                    })
                })
            );
            series
                .bullets
                .push(function() {
                    return am5.Bullet.new(root, {
                        locationY: 1,
                        locationX: 0.5,
                        sprite: am5.Circle.new(root, {
                            radius: 4,
                            fill: series.get("fill")
                        },bulletTemplate)
                    });
                });
            series
                .data
                .setAll(tripleGraphData);
            series
                .appear();
        }
              

        function createColumnSeries(field, margin) {
            const yAxis = chart
                .yAxes
                .push(
                    am5xy.ValueAxis.new(root, {
                        renderer: am5xy.AxisRendererY.new(root, {}),
                        tooltip: am5.Tooltip.new(root, {animationDuration: 0}),
                    x: am5.p100,
                    centerX: am5.p100,
                    marginTop: margin
                    })
                );
            yAxis
                .axisHeader
                .set("background", tripleSettings.background);
            yAxis
                .children
                .moveValue(am5.Label.new(root, {
                    rotation: -90,
                    text: field,
                    y: am5.p50,
                    centerX: am5.p50
                }), 0);

            const series = chart.series.push(
                am5xy.ColumnSeries.new(root, {
                    xAxis: xAxis,
                    yAxis: yAxis,
                    valueYField: field,
                    openValueYField: field+"2",
                    categoryXField: "turn",
                    sequencedInterpolation: true,
                    tooltip: am5.Tooltip.new(root, {
                        pointerOrientation: "vertical",
                        labelText: "user: {valueY}\nsystem: {openValueY}"
                    })
                })
            );
            series
                .bullets
                .push(function() {
                    return am5.Bullet.new(root, {
                        locationY: 0,
                        sprite: am5.Circle.new(root, {
                            radius: 5,
                            fill: '#FFD280'
                        },bulletTemplate)
                    })
                })
              series
                .bullets
                .push(function() {
                    return am5.Bullet.new(root, {
                        locationY: 1,
                        sprite: am5.Circle.new(root, {
                            radius: 5,
                            fill: 'lightgrey'
                        },bulletTemplate)
                    })
                })                
            series
                .data
                .setAll(tripleGraphData);
            series
                .appear();
        }
        
        createLineSeries("quality", 0);
        createColumnSeries("sentiment", 40);
        createColumnSeries("formality", 40);
        
        const cursor = chart 
            .set("cursor", am5xy.XYCursor.new(root, {
                behavior: "none",
                xAxis: xAxis
            }));
        
        xAxis
            .set("layer", 50);

        cursor
            .events
            .on("cursormoved", function() {
                const position = cursor.getPrivate("positionY");
                const axisIndex = Math.floor(chart.yAxes.length * position)
                const axis = chart.yAxes.getIndex(axisIndex);
                const y = axis.y() + axis.height();
                const dy = Math.round(-(chart.plotContainer.height() - y));
                const tooltip = xAxis.get("tooltip");
        
                if(Math.round(xAxis.get("dy")) != dy){
                    xAxis.animate({ key: "dy", to: dy, duration: 600, easing: am5.ease.out(am5.ease.cubic) });
                    xAxis.set("y", 0);
                    if(tooltip){tooltip.hide(0)}
                } else { 
                    tooltip.show(300);
                }
            })
        
        chart
            .appear(1000, 100);
    });
}