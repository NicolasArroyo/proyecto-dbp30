const ISBNInput = document.getElementById("ISBN");
const titleInput = document.getElementById("title");
const subjectInput = document.getElementById("subject");
const languageInput = document.getElementById("language");
const numberOfPagesInput = document.getElementById("number_of_pages");
const publicationDateInput = document.getElementById("publication_date");
const publisherInput = document.getElementById("publisher");
const priceInput = document.getElementById("price");
const authorOption = document.getElementById("author")


document.getElementById("addBookForm").onsubmit = function (event) {
    event.preventDefault();
    const ISBN = ISBNInput.value;
    const title = titleInput.value;
    const subject = subjectInput.value;
    const language = languageInput.value;
    const numberOfPages = numberOfPagesInput.value;
    const publicationDate = publicationDateInput.value;
    const publisher = publisherInput.value;
    const price = priceInput.value;
    const author_id = author.value;

    fetch("/add_book/new", {
        method: "POST",
        body: JSON.stringify({
            "ISBN": ISBN,
            "title": title,
            "subject": subject,
            "language": language,
            "numberOfPages": numberOfPages,
            "publicationDate": publicationDate,
            "publisher": publisher,
            "price": price,
            "author_id": author_id
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function (response) {
        return response.json();
    }).then(function (jsonResponse) {
        console.log(jsonResponse);
        book_already_exists = jsonResponse["book_already_exists"];
        document.getElementById("server-error").className = "hidden";
        if (book_already_exists) {
            document.getElementById("add-book-error").className = "";
        } else {
            document.getElementById("add-book-error").className = "hidden";
            window.location.href = "/home";
        }
    }).catch(function () {
        document.getElementById("server-error").className = "";
    });
}


/*
document.getElementById("addBookForm").onsubmit = function (event) {
    event.preventDefault();
    const ISBN = ISBNInput.value;
    const title = titleInput.value;
    const subject = subjectInput.value;
    const language = languageInput.value;
    const numberOfPages = numberOfPagesInput.value;
    const publicationDate = publicationDateInput.value;
    const publisher = publisherInput.value;
    const price = priceInput.value;

    fetch("/add_book/new", {
        method: "POST",
        body: JSON.stringify({
            "ISBN": ISBN,
            "title": title,
            "subject": subject,
            "language": language,
            "numberOfPages": numberOfPages,
            "publicationDate": publicationDate,
            "publisher": publisher,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function (response) {
        return response.json();
    }).then(function (jsonResponse) {
        console.log(jsonResponse);
        book_already_exists = jsonResponse["book_already_exists"];
        document.getElementById("server-error").className = "hidden";
        if (book_already_exists) {
            document.getElementById("add-book-error").className = "";
        } else {
            document.getElementById("add-book-error").className = "hidden";
            window.location.href = "/home";
        }
    }).catch(function () {
        document.getElementById("server-error").className = "";
    });
}*/
