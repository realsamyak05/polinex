let map;

function initMap() {
    if (map) return; // 🔥 prevent re-initialization

    map = L.map("map").setView([28.6, 77.2], 10);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
        .addTo(map);
}

let circleLayers = [];

function renderHeatmap(heatmapArray) {

    if (!map) {
        console.error("Map not initialized");
        return;
    }

    // Remove old circles
    circleLayers.forEach(layer => map.removeLayer(layer));
    circleLayers = [];

    // Add new circles
    heatmapArray.forEach(([lat, lng, count]) => {
        const circle = L.circle([lat, lng], {
            radius: 400,
            color: count > 1 ? "red" : "orange",
            fillOpacity: 0.5
        }).addTo(map);

        circleLayers.push(circle);
    });
}

function getCoordinates(ward) {
    const wardCoords = {
        "Rohini": { lat: 28.7041, lng: 77.1025 },
        "Dwarka": { lat: 28.5921, lng: 77.0460 },
        "Janakpuri": { lat: 28.6210, lng: 77.0910 },
        "Saket": { lat: 28.5245, lng: 77.2066 },
        "Pitampura": { lat: 28.6957, lng: 77.1310 },
        "Lajpat Nagar": { lat: 28.5677, lng: 77.2433 },
        "Karol Bagh": { lat: 28.6519, lng: 77.1909 },
        "Vasant Kunj": { lat: 28.5244, lng: 77.1507 },
        "Shahdara": { lat: 28.6680, lng: 77.2900 },
        "Mayur Vihar": { lat: 28.6096, lng: 77.2950 }
        // you can add more later
    };

    return wardCoords[ward];
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();
});
