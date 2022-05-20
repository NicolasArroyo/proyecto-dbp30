const nameInput = document.getElementById("name")
const dobInput = document.getElementById("dob")

document.getElementById("addAuthorForm").onsubmit = function (event) {
    event.preventDefault();
    const name = nameInput.value;
    const dob = dobInput.value;

    fetch("/add_author/new", {
        method: "POST",
        body: JSON.stringify({
            "name": name,
            "dob": dob
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function (response) {
        return response.json();
    }).then(function (jsonResponse) {
        console.log(jsonResponse);
        author_already_exists = jsonResponse["author_already_exists"];
        document.getElementById("server-error").className = "hidden";
        if (author_already_exists) {
            document.getElementById("add-author-error").className = "";
        } else {
            document.getElementById("add-author-error").className = "hidden";
            window.location.href = "/home";
        }
    }).catch(function () {
        document.getElementById("server-error").className = "";
    });
}