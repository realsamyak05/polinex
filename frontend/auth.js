function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Please fill all fields");
        return;
    }

    console.log("Login working");

    localStorage.setItem("user", email);

    console.log("Stored user:", localStorage.getItem("user"));

    // 🔥 FIXED REDIRECT
    setTimeout(() => {
        window.location.href = "index.html";
    }, 100);
}

function signup() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!name || !email || !password) {
        alert("Please fill all fields");
        return;
    }

    alert("Account created!");
    window.location.href = "login.html";
}