const cache = {};

function updateCache(){
    const conversation = document
        .getElementById("user-input")
        .value;
    console.log(conversation);

    if (conversation.length == 0) {
        console.log('no input given');
    } else if (conversation in cache){
        jsonResult = cache[conversation];
        console.log('in cache');
    } else {
        analyseConversation(conversation);
    }
};

function updateVisualisations(){
    displayChat(jsonResult);   
    displayEntityTree(jsonResult);
    displayLineGraph(jsonResult);
    displaySentimentFormality(jsonResult);
    displayWordCloud(jsonResult);    
};