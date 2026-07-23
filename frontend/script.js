// ===============================
// AI Content Generation Tool
// script.js
// ===============================

// Generate Content
async function generateContent() {

    const task = document.getElementById("task").value;
    const inputText = document.getElementById("inputText").value.trim();
    const result = document.getElementById("result");

    if (inputText === "") {
        alert("Please enter some text.");
        return;
    }

    result.innerHTML = "<p class='loading'>⏳ Generating content...</p>";

    try {

        const response = await fetch("http://127.0.0.1:8000/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                task: task,
                text: inputText
            })

        });

        if (!response.ok) {
            throw new Error("Server Error");
        }

        const data = await response.json();

        result.innerHTML = `
            <h3>Generated Output</h3>
            <p>${data.output.replace(/\n/g, "<br>")}</p>
        `;

    }

    catch (error) {

        console.error(error);

        result.innerHTML = `
            <p style="color:red;">
                ❌ Unable to connect to the backend.
            </p>
        `;
    }
}

// ===============================
// Clear Input & Output
// ===============================
function clearText() {

    document.getElementById("inputText").value = "";

    document.getElementById("result").innerHTML =
        "Your generated content will appear here...";

}

// ===============================
// Copy Output
// ===============================
function copyOutput() {

    const result = document.getElementById("result").innerText;

    if (
        result === "" ||
        result === "Your generated content will appear here..."
    ) {
        alert("Nothing to copy.");
        return;
    }

    navigator.clipboard.writeText(result);

    alert("✅ Output copied to clipboard!");

}

// ===============================
// Download Output
// ===============================
function downloadOutput() {

    const text = document.getElementById("result").innerText;

    if (
        text === "" ||
        text === "Your generated content will appear here..."
    ) {
        alert("Nothing to download.");
        return;
    }

    const blob = new Blob([text], { type: "text/plain" });

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "Generated_Output.txt";

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);

    window.URL.revokeObjectURL(url);

}