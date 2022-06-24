let xhr = new XMLHttpRequest();

var data = JSON.stringify({ "name":
    "qwe", "lastname": "rty" });
xhr.open("POST", "", true)
xhr.setRequestHeader("Content-Type", "application/json")
xhr.send(data)
