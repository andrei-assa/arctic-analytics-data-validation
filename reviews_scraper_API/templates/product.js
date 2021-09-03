// JavaScript code
function search_product() {

    var button = document.getElementById("btnSearch");

    button.onclick = function () {
        var text = document.getElementById("searchbar").value;
        window.open(text);
    }
}