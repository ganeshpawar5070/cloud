alert("script loaded");
const SERVER = "https://dropped-server-forge-extending.trycloudflare.com/";

function login() {
    alert("Login button clicked");

    const u = document.getElementById("username").value;
    const p = document.getElementById("password").value;

    if (u === "sumo" && p === "Sumo@123") {

        document.getElementById("loginBox").style.display = "none";
        document.getElementById("homeBox").style.display = "block";

    } else {

        document.getElementById("msg").innerText = "Wrong Username or Password";

    }

}

function openUpload() {
    window.open(SERVER + "/upload", "_blank");
}

function openDownload() {
    window.open(SERVER + "/download", "_blank");
}
