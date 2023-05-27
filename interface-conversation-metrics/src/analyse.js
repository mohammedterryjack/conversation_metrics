const url = "https://server2.oxolo.com:8080/api/main/run";
const token = "Pv5fZ44pHFK7mg2pkVEJFrMXWEMDf429";

function analyseConversation(conversation) {   
    document
        .getElementById("api-button")
        .className = 'conversation-submit clicked';
    const post = new XMLHttpRequest();
    post.open("POST", url);
    post.setRequestHeader("Access-Control-Allow-Origin","*");
    post.setRequestHeader("Accept", "application/json");
    post.setRequestHeader("token", token);
    post.setRequestHeader("Content-Type", "application/json");
    post.onreadystatechange = function() {
        if (post.readyState === 4) {
            console.log(post.status);
            jsonResult = JSON.parse(post.response);
            cache[conversation] = jsonResult;
            console.log(jsonResult)
            document.dispatchEvent(new Event('ApiReady'));
        }
    };
    post.send(JSON.stringify({
        string:conversation
    }));
};
