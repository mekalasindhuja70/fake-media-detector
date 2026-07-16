// ================================
// Fake Media Detector JavaScript
// ================================

const fileInput = document.getElementById("file");
const uploadBox = document.querySelector(".upload-box");
const form = document.querySelector("form");
const button = document.querySelector(".analyze-btn");

// ----------------------------
// Drag & Drop Highlight
// ----------------------------

uploadBox.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = "#00ff99";
    uploadBox.style.background = "rgba(255,255,255,0.15)";
});

uploadBox.addEventListener("dragleave", () => {
    uploadBox.style.borderColor = "cyan";
    uploadBox.style.background = "transparent";
});

uploadBox.addEventListener("drop", (e) => {
    e.preventDefault();

    uploadBox.style.borderColor = "cyan";
    uploadBox.style.background = "transparent";

    fileInput.files = e.dataTransfer.files;

    updateFileName();
});

// ----------------------------
// Show Selected File Name
// ----------------------------

fileInput.addEventListener("change", updateFileName);

function updateFileName(){

    if(fileInput.files.length > 0){

        const fileName = fileInput.files[0].name;

        uploadBox.innerHTML = `
            <i class="fa-solid fa-image upload-icon"></i>
            <h2>${fileName}</h2>
            <p>Image Ready for Analysis</p>
        `;
    }
}

// ----------------------------
// Loading Animation
// ----------------------------

form.addEventListener("submit", function(){

    button.innerHTML = `
    <i class="fa-solid fa-spinner fa-spin"></i>
    Analyzing...
    `;

    button.disabled = true;

});