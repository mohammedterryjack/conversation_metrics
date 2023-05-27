updateCache();
updateVisualisations();

document
    .querySelector('button')
    .addEventListener('click',updateCache);

document
    .addEventListener('ApiReady', function (event) {
        console.log(event.type);
        document
            .getElementById("api-button")
            .className = 'conversation-submit';
        console.log(jsonResult);
        updateVisualisations();
    }, false);