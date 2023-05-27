function displayWordCloud(jsonResult){
    const entities = extractEntities(jsonResult);
    const divID = "wordCloud";
    cleanCanvas(divID);
    am5.ready(function() {
        const root = am5.Root.new(divID);
        root.setThemes([am5themes_Animated.new(root)]);

        const wordCloudSettings = {
            type:am5wc.WordCloud.new(root, {
                categoryField: "text",
                valueField: "value",
                maxFontSize: am5.percent(15)
            }),
            font:{fontFamily: "Courier New"},
            shuffleInterval:5000
        }

        const series = root
            .container
            .children
            .push(wordCloudSettings.type);
        series
            .labels
            .template
            .setAll(wordCloudSettings.font);
        series
            .data
            .setAll(entities);    


        function randomlyShuffleWord(dataItem) {
            let value = Math.random() * 65;
            value = value - Math.random() * value;
            dataItem.set("value", value);
            dataItem.set("valueWorking", value);
        }
            
        function shuffleWords() {  
            am5.array.each(series.dataItems, randomlyShuffleWord)
        };

        setInterval(shuffleWords, wordCloudSettings.shuffleInterval)    
    }); 
}