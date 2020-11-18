divs = document.querySelectorAll("div")
console.log("Testing call_python(getAttribute, ...)")
for (var i = 0; i < divs.length; i++) {
    console.log(call_python("getAttribute", divs[i].handle, "class"));
}

console.log("Testing Node.getAttribute(...)")
for (var i = 0; i < divs.length; i++) {
    console.log(divs[i].getAttribute("class"));
}