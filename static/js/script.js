// ================================
// Fake Media Detector JavaScript
// ================================

const fileInput = document.getElementById("file");
const uploadBox = document.querySelector(".upload-box");
const button = document.querySelector(".analyze-btn");
const form = document.querySelector("form");

// Create filename text
const fileNameText = document.createElement("p");
fileNameText.style.marginTop = "15px";
fileNameText.style.fontWeight = "bold";
fileNameText.style.color = "#00ffff";

uploadBox.appendChild(fileNameText);

// ----------------------------
// Drag & Drop
// ----------------------------

uploadBox.addEventListener("dragover", function(e){
    e.preventDefault();
    uploadBox.style.borderColor = "#00ff99";
});

uploadBox.addEventListener("dragleave", function(){
    uploadBox.style.borderColor = "cyan";
});

uploadBox.addEventListener("drop", function(e){

    e.preventDefault();

    uploadBox.style.borderColor = "cyan";

    fileInput.files = e.dataTransfer.files;

    updateFileName();

});

// ----------------------------
// File Selection
// ----------------------------

fileInput.addEventListener("change", updateFileName);

function updateFileName(){

    if(fileInput.files.length > 0){

        fileNameText.innerHTML =
            "Selected : " + fileInput.files[0].name;

    }

}

// ----------------------------
// Loading
// ----------------------------

form.addEventListener("submit", function(){

    button.innerHTML =
        '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';

    button.disabled = true;

});