function RunSentimentAnalysis() {
    const textToAnalyze = document.getElementById('textToAnalyze').value;
    const systemResponseDiv = document.getElementById('system_response');
    const loadingDiv = document.getElementById('loading');

    if (!textToAnalyze.trim()) {
        systemResponseDiv.innerHTML = '<div class="alert alert-warning">Please enter some text to analyze.</div>';
        return;
    }

    
    loadingDiv.style.display = 'block';
    systemResponseDiv.innerHTML = '';

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4) {
            loadingDiv.style.display = 'none';

            if (this.status === 200) {
                try {
                    const response = JSON.parse(this.responseText);
                    systemResponseDiv.innerHTML = `<div class="alert alert-success">${response.response}</div>`;
                } catch (e) {
                    systemResponseDiv.innerHTML = '<div class="alert alert-danger">Error parsing response.</div>';
                }
            } else {
                let errorMsg = 'Error: Unable to process request.';
                if (this.status >= 400) {
                    try {
                        const errorResponse = JSON.parse(this.responseText);
                        errorMsg = errorResponse.error || errorMsg;
                    } catch (e) {
                        errorMsg = `Error: ${this.statusText}`;
                    }
                }
                systemResponseDiv.innerHTML = `<div class="alert alert-danger">${errorMsg}</div>`;
            }
        }
    };

    xhttp.open('GET', `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`, true);
    xhttp.send();
}