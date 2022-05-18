document.getElementById("search-form").onsubmit = function(e) {
    e.preventDefault();
    const toSearchInput = document.getElementById("to-search");
    const toSearch = toSearchInput.value.toLowerCase();

    const bookCardTemplate = document.querySelector("[data-book-template]");
    const bookCardContainer = document.querySelector("[data-book-cards-container]");

    fetch("/home/search", {
        method: 'POST',
        body: JSON.stringify({
            "toSearch": toSearch
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(jsonResponse) {
        books = jsonResponse.map(book => {
            console.log(book);
            const card = bookCardTemplate.content.cloneNode(true).children[0];
            const header = card.querySelector("[data-header]");
            const body = card.querySelector("[data-body]");
            header.textContent = book.id;
            body.textContent = book.title;
            bookCardContainer.append(card);
            return { id: book.id, title: book.title, element: card };
        })
        console.log(books);

        books.forEach(book => {
          const isVisible = book.title.toLowerCase().includes(toSearch)
          console.log(isVisible);
          book.element.classList.toggle("hide", !isVisible);
        })
    });
}