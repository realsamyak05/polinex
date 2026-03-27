console.log("JS LOADED");

const translations = {
  en: {
    sentiments: "Sentiments",
    positive: "Positive",
    negative: "Negative",
    neutral: "Neutral",
    topTopics: "Top Topics",
    avgScore: "Average Score",
    summary: "Summary",
    noIssues: "No major issues reported"
  },
  hi: {
    sentiments: "भावनाएँ",
    positive: "सकारात्मक",
    negative: "नकारात्मक",
    neutral: "तटस्थ",
    topTopics: "मुख्य मुद्दे",
    avgScore: "औसत स्कोर",
    summary: "सारांश",
    noIssues: "कोई प्रमुख समस्या नहीं मिली"
  }
};

function updateLanguage(lang) {
  const t = translations[lang];

  document.getElementById("sentimentsTitle").textContent = t.sentiments;
  document.getElementById("topTopicsTitle").textContent = t.topTopics;
  document.getElementById("scoreTitle").textContent = t.avgScore;
  document.getElementById("summaryTitle").textContent = t.summary;

  document.getElementById("posLabel").textContent = t.positive + ":";
  document.getElementById("negLabel").textContent = t.negative + ":";
  document.getElementById("neuLabel").textContent = t.neutral + ":";

  localStorage.setItem("lang", lang);
}

document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("languageSelect").addEventListener("change", function () {
  updateLanguage(this.value);
});

const savedLang = localStorage.getItem("lang") || "en";
document.getElementById("languageSelect").value = savedLang;
updateLanguage(savedLang);

    const dropdown = document.getElementById("wardSelect"); // must match HTML id

    dropdown.addEventListener("change", async function () {
        const ward = this.value;
        if (!ward) return;

        const analysisData = await getAnalysis(ward);
        const summaryData = await getSummary(ward);

        localStorage.setItem("selectedWard", ward);
        localStorage.setItem("topTopics", JSON.stringify(analysisData.top_topics));
        localStorage.setItem("summary", summaryData.summary);

const posEl = document.getElementById("pos");
const negEl = document.getElementById("neg");
const neuEl = document.getElementById("neu");

posEl.textContent = analysisData.positive;
negEl.textContent = analysisData.negative;
neuEl.textContent = analysisData.neutral;

posEl.style.color = "#4CAF50";  // green
negEl.style.color = "#f44336";  // red
neuEl.style.color = "#FFC107";  // yellow

        const topicsEl = document.getElementById("topics");

if (!analysisData.top_topics || analysisData.top_topics.length === 0) {
    const lang = localStorage.getItem("lang") || "en";
    topicsEl.innerHTML = `<span class="chip">${translations[lang].noIssues}</span>`;
} else {
    topicsEl.innerHTML = analysisData.top_topics
        .map(t => `<span class="chip">${t}</span>`)
        .join("");
}

        document.getElementById("score").textContent = analysisData.avg_score;
        document.getElementById("summary").textContent = summaryData.summary;

        const heatmapData = await getHeatmap();

        const heatmapArray = Object.entries(heatmapData).map(([w, info]) => {
            const coords = getCoordinates(w);
            if (coords) return [coords.lat, coords.lng, info.count];
        }).filter(Boolean);

        console.log("HEATMAP ARRAY:", heatmapArray);

        renderHeatmap(heatmapArray);
        // 🔥 Highlight selected ward
const selectedCoords = getCoordinates(ward);

if (selectedCoords) {

    map.setView([selectedCoords.lat, selectedCoords.lng], 13);

    if (window.selectedMarker) {
        map.removeLayer(window.selectedMarker);
    }

    window.selectedMarker = L.marker([selectedCoords.lat, selectedCoords.lng])
        .addTo(map)
        .bindPopup(ward)
        .openPopup();
}
    });

    loadWards(); // 🔴 VERY IMPORTANT — this fills the dropdown

});



async function loadWards() {
    console.log("loadWards CALLED");  // 👈 add this

    const heatmapData = await getHeatmap();
    console.log("DATA:", heatmapData); // 👈 add this

    const wardSelect = document.getElementById("wardSelect");
    wardSelect.innerHTML = `<option value="">Select Ward</option>`;

    Object.keys(heatmapData).forEach(ward => {
        const option = document.createElement("option");
        option.value = ward;
        option.textContent = ward;
        wardSelect.appendChild(option);
    });
}


function logout() {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}