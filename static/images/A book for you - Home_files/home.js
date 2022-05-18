function cardIsInCardContainer(card) {
    const bookCardContainer = document.querySelector("[data-book-cards-container]");

    for (var i = 0; i < bookCardContainer.children.length; i++) {
        child = bookCardContainer.children[i];

        if (child.querySelector("[data-body]").textContent == card.querySelector("[data-body]").textContent ) {
            return true;
        }
    }

    return false;
}

let books = []

books.forEach(book => {
    const isVisible = book.title.toLowerCase().includes(toSearch)
    book.element.classList.toggle("hide", !isVisible);
})

document.getElementById("search-form").onsubmit = function(e) {
    e.preventDefault();
    const toSearchInput = document.getElementById("to-search");
    const toSearch = toSearchInput.value.toLowerCase();

    const bookCardTemplate = document.querySelector("[data-book-template]");
    const bookCardContainer = document.querySelector("[data-book-cards-container]");

    fetch("/home/search", {
        method: 'GET'
    }).then(function(response) {
        return response.json();
    }).then(function(jsonResponse) {
        books = jsonResponse.map(book => {
            const card = bookCardTemplate.content.cloneNode(true).children[0];
            const header = card.querySelector("[data-header]");
            const body = card.querySelector("[data-body]");
            // header.textContent = book.id;
            header.textContent = book.title;
            body.textContent = book.id

            if (!cardIsInCardContainer(card)) {
                bookCardContainer.append(card);
            }
            return { id: book.id, title: book.title, element: card };
        })
    });
}

rentForms = document.getElementsByClassName("rent-form");

for (rentForm of rentForms) {
    console.log(rentForm);
}

// document.getElementById("search-form").onsubmit = function(e) {
//     e.preventDefault();
//     const toSearchInput = document.getElementById("to-search");
//     const toSearch = toSearchInput.value.toLowerCase();

//     const bookCardTemplate = document.querySelector("[data-book-template]");
//     const bookCardContainer = document.querySelector("[data-book-cards-container]");

//     fetch("/home/search", {
//         method: 'GET'
//     }).then(function(response) {
//         return response.json();
//     }).then(function(jsonResponse) {
//         books = jsonResponse.map(book => {
//             const card = bookCardTemplate.content.cloneNode(true).children[0];
//             const header = card.querySelector("[data-header]");
//             const body = card.querySelector("[data-body]");
//             // header.textContent = book.id;
//             header.textContent = book.title;
//             body.textContent = book.id

//             if (!cardIsInCardContainer(card)) {
//                 bookCardContainer.append(card);
//             }
//             return { id: book.id, title: book.title, element: card };
//         })
//     });
// }
