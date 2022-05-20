function cardIsInCardContainer(card) {
    const bookCardContainer = document.querySelector("[data-book-cards-container]");
    
    for (var i = 0; i < bookCardContainer.children.length; i++) {
        child = bookCardContainer.children[i];

        if (child.querySelector("[data-body]").textContent == card.querySelector("[data-body]").textContent) {
            if (child.querySelector("[data-header]").textContent == card.querySelector("[data-header]").textContent) {
                return true;
            }
        }
    }

    return false;
}

let books = []

const toSearchInput = document.getElementById("to-search");
toSearchInput.addEventListener("input", e => {
    const toSearchInput = document.getElementById("to-search");
    const toSearch = toSearchInput.value.toLowerCase();

    books.forEach(book => {
        const isVisible =
        book.title.toLowerCase().includes(toSearch)
        && !(toSearch.trim().length === 0);  // check if toSearch is full of spaces
        book.element.classList.toggle("hide", !isVisible);
    })

    // // Add a book to the shopping cart
    // books.forEach(book => {
    //     if (book.element.classList == "card") {
    //         console.log(book["element"].querySelector("[data-rent-button]").checked);
    //         if (book["element"].querySelector("[data-rent-button]").checked) {
    //             console.log(true);
    //         }
    //     }
    // })
})

fetch("/home/search", {
    method: 'GET'
}).then(function(response) {
    return response.json();
}).then(function(jsonResponse) {
    const bookCardTemplate = document.querySelector("[data-book-template]");
    const bookCardContainer = document.querySelector("[data-book-cards-container]");
    books = jsonResponse.map(book => {
        const card = bookCardTemplate.content.cloneNode(true).children[0];
        const header = card.querySelector("[data-header]");
        const body = card.querySelector("[data-body]");

        header.textContent = book.title;
        body.textContent = book.id;

        if (!cardIsInCardContainer(card)) {
            bookCardContainer.append(card);
        }

        return {id: book.id, title: book.title, element: card};
    })
});

// Add a book to the shopping cart
document.getElementById('submit-rent').onsubmit = function(e) {
    e.preventDefault();
    idBooksToRent = []
    
    books.forEach(book => {
        if (book.element.classList == "card") {
            if (book["element"].querySelector("[data-rent-button]").checked) {
                idBooksToRent.push(book["id"]);
            }
        }
    })

    fetch('/home/rent', {
        method: "POST",
        body: JSON.stringify({
            "idBooksToRent": idBooksToRent
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(jsonResponse) {
        // Check if there are books and show the message
        if (jsonResponse["noBooks"] === true) {
            document.getElementById("no-books-error").className = "";
        }
        else {
            document.getElementById("no-books-error").className = "hidden";
        }

        // Check if the rent was succesfull or not
        if (jsonResponse["succesfullRent"] === true) {
            console.log("Your books have been rented succcesfully.")
        }
        else {
            console.log("This book is already rented")
        }
    });
} 
