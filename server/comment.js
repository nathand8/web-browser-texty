p_error = document.querySelectorAll("#errors")[0];
console.log("p_error");
console.log(p_error)

function lengthCheck() {
    var value = this.getAttribute("value");
    console.log("lengthCheck! " + value.length)
    if (value.length > 20) {
        p_error.innerHTML = "Comment too long!"
    }
}

input = document.querySelectorAll("input")[0];
input.addEventListener("change", lengthCheck);