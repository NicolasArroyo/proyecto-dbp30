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

        return { id: book.id, title: book.title, element: card };
    })
});
