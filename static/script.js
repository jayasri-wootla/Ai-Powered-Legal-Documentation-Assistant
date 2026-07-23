function uploadFile() {
    let file = document.getElementById("fileInput").files[0];
    let formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("summary").innerText = data.summary;
        document.getElementById("clauses").innerText = JSON.stringify(data.clauses, null, 2);
        document.getElementById("risk").innerText = JSON.stringify(data.risk, null, 2);
    });
}

function askQuestion() {
    let question = document.getElementById("question").value;

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: question})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("answer").innerText = data.answer;
    });
}