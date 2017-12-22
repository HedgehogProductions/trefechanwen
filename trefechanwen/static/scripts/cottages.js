// Get the modals
var cottageTermsModal = document.getElementById('cottageTermsModal');
var cottageAccessModal = document.getElementById('cottageAccessModal');

// Get the buttons that open a modal
var cottageTermsButton = document.getElementById("cottageTermsButton");
var cottageAccessButton = document.getElementById("cottageAccessButton");

// Get the modal close buttons
var cottageTermsClose = document.getElementById("cottageTermsClose");
var cottageAccessClose = document.getElementById("cottageAccessClose");

// When the user clicks on the button, open the cottageTermsModal
cottageTermsButton.onclick = function() {
    cottageTermsModal.style.display = "block";
};
cottageAccessButton.onclick = function() {
    cottageAccessModal.style.display = "block";
};

// When the user clicks on close, close the modal
cottageTermsClose.onclick = function() {
    cottageTermsModal.style.display = "none";
};
cottageAccessClose.onclick = function() {
    cottageAccessModal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == cottageTermsModal || event.target == cottageAccessModal) {
        cottageTermsModal.style.display = "none";
        cottageAccessModal.style.display = "none";
    }
};