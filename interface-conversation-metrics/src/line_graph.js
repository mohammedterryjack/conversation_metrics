function displayLineGraph(jsonResult){
    const lineGraphData = extractTurnBasedScores(jsonResult);    
    const divID = 'lineGraph';
    cleanCanvas(divID);
    am5.ready(function() {                
        const root = am5.Root.new(divID);
        root.setThemes([am5themes_Animated.new(root)]);

        const lineGraphSettings = {
            type:am5xy.XYChart.new(root, {
                panX: true,
                panY: true,
                wheelX: "panX",
                wheelY: "zoomX",
                maxTooltipDistance: 0
            }),
            xAxis:am5xy.ValueAxis.new(root, {
                renderer: am5xy.AxisRendererX.new(root, {}),
                tooltip: am5.Tooltip.new(root, {})
            }),
            yAxis:am5xy.ValueAxis.new(root,{
                renderer: am5xy.AxisRendererY.new(root, {})
            }),
            xLabel:'utterance',
            yLabel:'score',
            cursor: am5xy.XYCursor.new(root, {behavior: "none"}),
            scrollBarX: am5.Scrollbar.new(root, {orientation: "horizontal"}),
            scrollBarY: am5.Scrollbar.new(root, {orientation: "vertical"}),
            legend:am5.Legend.new(root, {
                width: 200,
                paddingLeft: 15,
                height: am5.percent(100)
            }),
            fadedLine:{
                strokeOpacity: 0.15,
                stroke: am5.color(0x000000)
            },
            highlightedLine:{
                strokeWidth: 3
            },
            xAxisLabel: am5.Label.new(root, {
                text: "Utterance",
                x: am5.p50,
                centerX: am5.p50
            })
        }

        const chart = root
            .container
            .children
            .push(lineGraphSettings.type);    

        const xAxis = chart
            .xAxes
            .push(lineGraphSettings.xAxis);
        xAxis
            .children
            .moveValue(lineGraphSettings.xAxisLabel, xAxis.children.length - 1);
            
        const yAxis = chart
            .yAxes
            .push(lineGraphSettings.yAxis);

        chart
            .set("cursor", lineGraphSettings.cursor)
            .lineY
            .set("visible", false);
        chart
            .set("scrollbarX", lineGraphSettings.scrollBarX);
        chart
            .set("scrollbarY", lineGraphSettings.scrollBarY);

        const legend = chart
            .rightAxesContainer
            .children
            .push(lineGraphSettings.legend);            
        legend
            .itemContainers
            .template
            .events
            .on("pointerover", function(event) {
                let line = event
                    .target
                    .dataItem
                    .dataContext;

                chart
                    .series
                    .each(function(chartLine) {
                        if (chartLine != line) {
                            chartLine.strokes.template.setAll(lineGraphSettings.fadedLine);
                        } else {
                            chartLine.strokes.template.setAll(lineGraphSettings.highlightedLine);
                        }
                    })
            })
        legend
            .itemContainers
            .template
            .events
            .on("pointerout", function() {            
                chart
                    .series
                    .each(function(chartLine) {
                        chartLine.strokes.template.setAll({
                            strokeOpacity: 1,
                            strokeWidth: 1,
                            stroke: chartLine.get("fill")
                        });
                    });
            })
        legend
            .itemContainers
            .template
            .set("width", am5.p100);
        legend
            .valueLabels
            .template
            .setAll({width: am5.p100,textAlign: "right"});

                
        function add_data_to_chart(chart, data) {
            return chart
                .series
                .push(
                    am5xy.LineSeries.new(root, {
                        name: data.label,
                        xAxis: xAxis,
                        yAxis: yAxis,
                        valueYField: lineGraphSettings.yLabel,
                        valueXField: lineGraphSettings.xLabel,
                        legendValueText: "{valueY}",
                        tooltip: am5
                            .Tooltip
                            .new(root,{
                                pointerOrientation: "horizontal",
                                labelText: "{valueY}"
                            })
                        })
                );
        }
        
        lineGraphData.forEach(data=>{
            let line = add_data_to_chart(chart, data)
            line.data.setAll(data.series);
            line.appear();
        });
                
        legend.data.setAll(chart.series.values);
        chart.appear(1000, 100);               

    }); 
};