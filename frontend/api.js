if (!localStorage.getItem("token")) {
    window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", () => {

    initMap();

    document.getElementById("loadBtn").addEventListener("click", async () => {

        const data = await getAnalysis();

        document.getElementById("pos").textContent = data.positive;
        document.getElementById("neg").textContent = data.negative;
        document.getElementById("neu").textContent = data.neutral;

        const topics = document.getElementById("topics");
        topics.innerHTML = "";

        data.top_topics.slice(0, 3).forEach(t => {
            const li = document.createElement("li");
            li.textContent = t;
            topics.appendChild(li);
        });

        document.getElementById("score").textContent = data.average_score;
        document.getElementById("summary").textContent = data.summary;

        const heatmap = await getHeatmap();
        renderHeatmap(heatmap);
    });

});

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}