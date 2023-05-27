const userImg = "img/userAvatar.jpeg";
const systemImg = "img/systemAvatar.gif";
const roundingFactor = 10;

function displayChat(jsonResult){
    const divID = 'chatLog';
    console.log(`updating ${divID}`);
    let parentDiv = document.getElementById(divID);
    resetDiv(parentDiv);

    for (let index=0;index < jsonResult.utterances.length; index++){
        let utterance = jsonResult.utterances[index];
        let utteranceHTML = `<p>${utterance}</p>`
        let utteranceNo = jsonResult.utterance_based_scores.turn_number[index];
        let className, imageHTML, side, id;
        if (index%2==0){
            className="chat"
            imageHTML=`<img src=${userImg} alt="Avatar"></img>`
            side = 'right'
        } else {
            className="chat system"
            imageHTML=`<img src=${systemImg} alt="Avatar" class="right"></img>`
            side = 'left'
        }
        let sentiment = Math.round(roundingFactor*jsonResult.utterance_based_scores.sentiment[index])/roundingFactor;
        let formality = Math.round(roundingFactor*jsonResult.utterance_based_scores.formality[index])/roundingFactor;
        let indexHTML = `<span class="chat-id-${side}">Utterance: ${utteranceNo}&emsp;Sentiment: ${sentiment}&emsp;Formality: ${formality}</span>`
        let chatDiv = document.createElement('div');
        chatDiv.id = `utterance_${utteranceNo}`;
        chatDiv.className = className;
        chatDiv.innerHTML = `${imageHTML}\n${utteranceHTML}\n${indexHTML}`;
        parentDiv.appendChild(chatDiv);
    }
}; 

function scrollToUtterance(utteranceNo) {
    document
        .getElementById(`utterance_${utteranceNo}`)
        .scrollIntoView({behavior: 'smooth'});
}