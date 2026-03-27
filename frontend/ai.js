document.addEventListener("DOMContentLoaded", () => {

    const user = localStorage.getItem("user");
    if (!user) {
        window.location.href = "login.html";
        return;
    }

    const ward = localStorage.getItem("selectedWard");
    const topics = JSON.parse(localStorage.getItem("topTopics") || "[]");

    // Show ward name
    document.getElementById("ai-ward").innerText = `Ward: ${ward}`;

    // Show topics
    document.getElementById("ai-topics").innerHTML = topics
        .map(t => `<li>${t}</li>`)
        .join("");
});

async function generateSolutions() {
    const output = document.getElementById("ai-output");

    output.innerText = "🤖 Generating solutions...";

    const ward = localStorage.getItem("selectedWard");

    const topics = Array.from(document.querySelectorAll("#ai-topics li"))
        .map(li => li.innerText);

    try {
        const res = await fetch("http://127.0.0.1:5000/solutions", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                ward: ward,
                top_topics: topics
            })
        });

        const data = await res.json();

        output.innerHTML = formatSolutions(data.solutions);

    } catch (err) {
        output.innerText = "Error generating solutions.";
        console.error(err);
    }
}

function formatSolutions(text) {
    return text
        .split("\n")
        .map(line => {
            if (/^\*\*(.*?)\*\*/.test(line)) {
                // **Section Title** → <h3>
                return line.replace(/\*\*(.*?)\*\*/, "<h3>$1</h3>");
            } else if (/^\*\s/.test(line)) {
                // * bullet point → <li>
                return `<li>${line.replace(/^\*\s/, "")}</li>`;
            } else if (line.trim() === "") {
                return "<br>";
            } else {
                return `<p>${line}</p>`;
            }
        })
        .join("")
        // Wrap consecutive <li> items in <ul>
        .replace(/(<li>.*?<\/li>)+/gs, "<ul>$&</ul>");
}

function logout() {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}