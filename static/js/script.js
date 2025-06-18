let cart_list = localStorage.getItem('cart_list') ?? [];
cart_list = JSON.parse(cart_list);

function addToCart(btn){
    let card = btn.parentElement.parentElement.parentElement;
    let title = card.querySelector('.title').innerText.trim();
    let price = card.querySelector('.price').innerText.trim();
    let image = card.querySelector('.product-image').src;

    let find_product = cart_list.find(obj => {
        return obj.title === title;
    });

    price = parseFloat(price.replace('$',''));

    if(find_product === undefined) {
        cart_list.push(
            {
                title : title ,
                quantity : 1,
                price : price,
                image : image
            })
    }
    else {
        find_product.quantity++;
    }

    Swal.fire({
      position: "center",
      icon: "success",
      title: "Your product has been saved",
      showConfirmButton: false,
      timer: 1000
    });

    localStorage.setItem('cart_list',JSON.stringify(cart_list));
    updateCart();
}

// {# initialized #}
updateCart();

function updateCart(){
    let cart_list = localStorage.getItem('cart_list') ?? [];
    cart_list = JSON.parse(cart_list);

    let cart_count = document.querySelector('.cartNumber');

    cart_count.innerText = cart_list.length;
}






























