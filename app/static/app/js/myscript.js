$('#slider1, #slider2, #slider3,#slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var increasequantity = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/plus_cart",
        data: {
            product_id: id
        },
        success:function(data){
            increasequantity.innerText=data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var increasequantity = this.parentNode.children[2]
    $.ajax({
        type:"GET",
        url:"/minus_cart",
        data: {
            product_id: id
        },
        success:function(data){
            increasequantity.innerText=data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total_amount').innerText = data.total_amount
        }
    })
})

$('.remove_cart').click(function(event) {
    event.preventDefault();
    var id = $(this).attr("pid").toString();
    var remove = this;
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            product_id: id
        },
        success: function(data) {
            // Update amounts
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('total_amount').innerText = data.total_amount;

            // Remove the item from the DOM
            remove.parentNode.parentNode.parentNode.parentNode.remove();
        }
    });
});