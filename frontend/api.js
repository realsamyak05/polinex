const BASE_URL = "http://127.0.0.1:5000";

// ✅ Pass ward
async function getAnalysis(ward) {
    const res = await fetch(`${BASE_URL}/analyze?ward=${ward}`);
    return await res.json();
}

// ✅ Pass ward
async function getSummary(ward) {
    const res = await fetch(`${BASE_URL}/summary?ward=${ward}`);
    return await res.json();
}

// ✅ Heatmap stays global
async function getHeatmap() {
    const res = await fetch(`${BASE_URL}/heatmap`);
    return await res.json();
}

// ✅ Solutions (no change needed except cleaner format)
async function getSolutions(topics, ward) {
    try {
        const response = await fetch(`${BASE_URL}/solutions`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ward: ward,
                top_topics: topics
            })
        });

        return await response.json();

    } catch (error) {
        console.error("Error:", error);
    }
}