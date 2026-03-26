let map;

function initMap() {
    map = L.map("map").setView([28.6, 77.2], 10);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png")
        .addTo(map);
}

function renderHeatmap(data) {
    data.forEach(w => {
        L.circle([w.lat, w.lng], {
            radius: 400,
            color: w.count > 50 ? "red" : "orange"
        }).addTo(map)
        .bindTooltip(`${w.name}<br>${w.top_issue}<br>${w.count}`);
    });
}