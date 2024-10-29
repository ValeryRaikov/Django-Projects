const updateBtns = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener("click", (e) => {
        const productId = e.target.dataset.product;
        const action = e.target.dataset.action;

        // console.log('USER: ', user );
        if (user === "AnonymousUser") {
            addCookieItem(productId, action);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

const addCookieItem = (productId, action) => {
    if (action === "add") {
        if (cart[productId] === undefined) {
            cart[productId] = {
                quantity: 1,
            };
        } else {
            cart[productId]["quantity"] += 1;
        }
    }

    if (action === "remove") {
        cart[productId]["quantity"] -= 1;

        if (cart[productId]["quantity"] <= 0) {
            delete cart[productId];
        }
    }

    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

const updateUserOrder = (productId, action) => {
    const url = "/update-item/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            productId,
            action,
        }),
    })
    .then(response => response.json())
    .then(location.reload())
    .catch(error => console.error(error));
}
