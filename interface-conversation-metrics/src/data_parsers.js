function resetDiv(div){
    while (div.firstChild){
        div.removeChild(div.lastChild);
    };
};

function cleanCanvas(graphDivId){
    let parentDiv = document.getElementById(graphDivId+"Container");
    resetDiv(parentDiv);
    let childDiv = document.createElement('div');
    childDiv.id = graphDivId;
    parentDiv.appendChild(childDiv);
    console.log(`updating ${graphDivId}`);
}

function extractTurnBasedScores(response){
    const quality = response.turn_based_scores.quality;
    const tft = response.turn_based_scores.tit_for_tat;
    const reaction = response.turn_based_scores.inferred_reaction;
    const scores = [quality,tft,reaction];
    const labels = ["Quality 🎯","Tit for Tat 🤝", "Reaction 🤨"];
    const turns = response.turn_based_scores.turn_number;

    const datas = [];
    for(index=0;index<labels.length;index++){
        let score = scores[index];
        const data = {
            label:labels[index],
            series:[]
        }
        for(jndex=0;jndex<score.length;jndex++){            
            data.series.push({
                utterance:turns[jndex],
                score:score[jndex]
            })
        }
        datas.push(data)
    }
    return datas
}

function extractTripleData(response){
    const data = [];
    const sentiments = response.utterance_based_scores.sentiment;
    const formality = response.utterance_based_scores.formality;
    const qualities = response.turn_based_scores.quality;
    const turns = response.turn_based_scores.turn_number;
    for (let index = 0; index < qualities.length; index++) { 
        let jndex = 2*index;
        data.push({
            turn: turns[index],
            quality: qualities[index],
            sentiment: sentiments[jndex],
            formality: formality[jndex],
            sentiment2: sentiments[jndex+1],
            formality2: formality[jndex+1],
        });
    }   
    return data; 
}

function extractEntityTreeRoot(response){
    const nodes = {}
    const userEntityNames = response.user_entities.text
    const userEntityCoordinates = response.user_entities.coordinates
    for (let index=0;index<userEntityNames.length; index++){
        let [xUser,yUser] = userEntityCoordinates[index];
        nodes[`${xUser}-${yUser}`] = {
            name:userEntityNames[index],
            speaker:'user',
            depth:Math.abs(yUser),
            children:[],
            weight:-1
        }
    }
    const systemEntityNames = response.system_entities.text
    const systemEntityCoordinates = response.system_entities.coordinates
    for (let index=0;index<systemEntityNames.length; index++){
        let [xSystem,ySystem] = systemEntityCoordinates[index];
        nodes[`${xSystem}-${ySystem}`] = {
            name:systemEntityNames[index],
            speaker:'system',
            depth:Math.abs(ySystem),
            children:[],
            weight:-1
        }        
    }
    const entity_links = response.relations.coordinates
    const link_weights = response.relations.weights
    for (let index=0;index<entity_links.length; index++){
        let [startCoordinate,endCoordinate] = entity_links[index]
        let [xStart,yStart] = startCoordinate
        let [xEnd,yEnd] = endCoordinate
        endNode = nodes[`${xEnd}-${yEnd}`]
        startNode = nodes[`${xStart}-${yStart}`]
        startNode.children.push(endNode)
        endNode.weight = link_weights[index]
    }
    const threadHeads = []
    for (let entityId in nodes ){
        entity = nodes[entityId]
        if (entity.weight < 0){
            threadHeads.push(entity)
        }
    }
    const systemRootThreadHead = {
        name:"System Initiated",
        speaker:"system",
        coordinate:null,
        children:[],
        weight:null
    }
    const userRootThreadHead = {
        name:"User Initiated",
        speaker:"user",
        coordinate:null,
        children:[systemRootThreadHead],
        weight:null
    }
    threadHeads.forEach(threadHead=>{
        if (threadHead.speaker == "user"){
            userRootThreadHead.children.push(threadHead);
        } else {
            systemRootThreadHead.children.push(threadHead);
        }
    })
    return userRootThreadHead
}

function extractEntities(response){
    const entityLookup = {}
    const userEntityNames = response.user_entities.text;
    const userEntityCoordinates = response.user_entities.coordinates;
    for (let index=0;index<userEntityNames.length; index++){
        let [x,y] = userEntityCoordinates[index];
        entityLookup[`${x}-${y}`] = {
            text:userEntityNames[index],
            color: "#C0D5EF",
            speaker: "user",
            x: x,
            y: y,
            parent: null,
            value: 0
        };
    };
    const systemEntityNames = response.system_entities.text;
    const systemEntityCoordinates = response.system_entities.coordinates;
    for (let index=0;index<systemEntityNames.length; index++){
        let [x,y] = systemEntityCoordinates[index];
        entityLookup[`${x}-${y}`] =  {
            text:systemEntityNames[index],
            color: "#EFC0D5",
            speaker: "system",
            x: x,
            y: y,
            parent: null,
            value: 0
        };
    };
    const data = []
    const linkWeights = response.relations.weights;
    const linkCoordinates = response.relations.coordinates;
    for (let index=0; index<linkCoordinates.length; index++){
        let [startCoordinate,endCoordinate] = linkCoordinates[index]
        let [xParent,yParent] = startCoordinate
        let [xChild,yChild] = endCoordinate
        let parent = entityLookup[`${xParent}-${yParent}`];
        let child = entityLookup[`${xChild}-${yChild}`];
        child.parent = parent.text;
        child.value = 100*(linkWeights[index])/2;
        data.push(child);
    };
    return data
}