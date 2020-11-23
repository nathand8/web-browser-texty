var button = document.querySelectorAll("#button")[0]
var test = document.querySelectorAll("#test")[0]
var text = ""
button.addEventListener("click", function() {
    text += "This is a lot of text that is going" +
        " to break over multiple lines, causing this test" +
        " paragraph to change height, which should be a" +
        " problem for our reflow algorithm."
    test.innerHTML = text
})