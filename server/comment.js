p_error = document.querySelectorAll("#errors")[0];
input = document.querySelectorAll("input")[0];
input.addEventListener("change", lengthCheck);
allow_submit = true;

function lengthCheck() {
    allow_submit = input.getAttribute("value").length <= 20;
    if (!allow_submit) {
        p_error.innerHTML = "Comment too long!"
    }
}

form = document.querySelectorAll("form")[0];
form.addEventListener("submit", function(e) {
    if (!allow_submit) e.preventDefault();
});