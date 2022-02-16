/*
  This pen cleverly utilizes SVG filters to create a "Morphing Text" effect. Essentially, it layers 2 text elements on top of each other, and blurs them depending on which text element should be more visible. Once the blurring is applied, both texts are fed through a threshold filter together, which produces the "gooey" effect. Check the CSS - Comment the #container rule's filter out to see how the blurring works!
*/
$(document).ready(function () {

  $.ajax({
    url: "https://shopee.co.th/api/v2/flash_sale/flash_sale_get_items?offset=0&limit=16&sort_soldout=true&need_personalize=true&with_dp_items=true",
    context: document.body,
    type: 'get',
    dataType: 'json',
    success: function (data) {
      // console.log(data.data);

      $.each(data.data.items, function (index, value) {

        console.log(value);



        var html2 = '<div class="grid__item large--one-fifth medium--one-quarter">' +
          '	<div class="grid__item_wrapper">' +
          '<div class="grid__image product-image">' +
          '<a href="./product.html">' +
          '<img src="https://cf.shopee.co.th/file/' + value.image + '"alt="Demo Product Sample">' +
          '</a>' +
          '<span class="sale-icon">ลด ' + value.discount + '</span>' +
          '<div class="quickview">' +
          '<div class="product-ajax-cart hidden-xs hidden-sm">' +
          '<div data-handle="consequuntur-magni-dolores"class="quick_shop-div">' +
          '<a href="#quick-shop-modal" class="btn quick_shop">' +
          '<i class="fa fa-eye" title="Quick View"></i>' +
          '</a>' +
          '</div>' +
          '</div>' +
          '</div>' +
          '</div>' +
          '<div class="rating-star">' +
          '<span class="spr-badge" id="spr_badge_3008529987" data-rating="0.0">' +
          '<span class="spr-starrating spr-badge-starrating">' +
          '<i class="spr-icon spr-icon-star-empty" style=""></i>' +
          '<i class="spr-icon spr-icon-star-empty" style=""></i>' +
          '<i class="spr-icon spr-icon-star-empty" style=""></i>' +
          '<i class="spr-icon spr-icon-star-empty" style=""></i>' +
          '<i class="spr-icon spr-icon-star-empty" style=""></i>' +
          '</span>' +
          '<span class="spr-badge-caption">No reviews </span>' +
          '</span>' +
          '</div>' +
          '<p class="h6 product-title">' +
          '<a href="./product.html">' + value.name + '</a>' +
          '</p>' +
          '<p class="product-price">' +
          '<strong>On Sale</strong>' +
          '<span class="money" >฿ ' + value.price / 100000 + '</span>' +
          '<span class="visually-hidden">Regular price</span>' +
          '<s><span class="money" >฿ ' + value.price_before_discount / 100000 + '</span></s>' +
          '</p>' +

          '<div class="list-mode-description">' +
          'Quisque vel enim quis purus ultrices consequat, sed tincidunt massa blandit' +
          'ipsum interdum tristique cras dictum, lacus eu molestie elementum nulla est' +
          'auctor. Etiam dan lorem quis ligula elementum porttitor quisem. Duis eget' +
          'purus urna fusce sed scelerisque ante. Lorem ipsum dolor sit amet' +
          'consectetur...' +
          '</div>' +
          '<ul class="action-button">' +
          '	<li class="add-to-cart-form">' +
          '<form action="#" method="post" enctype="multipart/form-data"' +
          '	id="AddToCartForm" class="form-vertical">' +
          '	<div class="effect-ajax-cart">' +
          '<input type="hidden" name="quantity" value="1">' +
          '	<button type="submit" name="add" id="AddToCart"' +
          '	class="btn btn-1 add-to-cart" title="Buy Now">' +
          '<span id="AddToCartText"><i class="fa fa-shopping-cart"></i>' +
          '	Buy Now</span>' +
          '</button>' +
          '</div>' +
          '</form>' +
          '	</li>' +
          '<li class="wishlist">' +
          '<a class="wish-list btn" href="./wish-list.html"><i class="fa fa-heart"' +
          '	title="Wishlist"></i></a>' +
          '</li>' +
          '<li class="email">' +
          '<a target="_blank" class="btn email-to-friend" href="#"><i' +
          'class="fa fa-envelope" title="Email to friend"></i></a>' +
          '</li>' +
          '</ul>' +
          '</div>' +
          '</div>';

        $('.sale-products').append(html2);
      }

      );
      // console.log(data.items[0])
    }
  });


});


const elts = {
  text1: document.getElementById("text1"),
  text2: document.getElementById("text2")
};


// The strings to morph between. You can change these to anything you want!
const texts = [
  "Product",
  "Price",
  "Comparison",
  "Systems",
  "Using",
  "Web Scraping",
  "From",
  "Popular",
  "E-commerce",
  "Platforms",
  "Shopee",
  "Lazada",
  "JD-Central",

];
// Product Price Comparison System using Web Scraping from Popular E-commerce Platforms (Shopee, Lazada, JD-Central)

// Controls the speed of morphing.
const morphTime = 1;
const cooldownTime = 0.25;

let textIndex = texts.length - 1;
let time = new Date();
let morph = 0;
let cooldown = cooldownTime;

elts.text1.textContent = texts[textIndex % texts.length];
elts.text2.textContent = texts[(textIndex + 1) % texts.length];

function doMorph() {
  morph -= cooldown;
  cooldown = 0;

  let fraction = morph / morphTime;

  if (fraction > 1) {
    cooldown = cooldownTime;
    fraction = 1;
  }

  setMorph(fraction);
}

// A lot of the magic happens here, this is what applies the blur filter to the text.
function setMorph(fraction) {
  // fraction = Math.cos(fraction * Math.PI) / -2 + .5;

  elts.text2.style.filter = `blur(${Math.min(8 / fraction - 8, 100)}px)`;
  elts.text2.style.opacity = `${Math.pow(fraction, 0.4) * 100}%`;

  fraction = 1 - fraction;
  elts.text1.style.filter = `blur(${Math.min(8 / fraction - 8, 100)}px)`;
  elts.text1.style.opacity = `${Math.pow(fraction, 0.4) * 100}%`;

  elts.text1.textContent = texts[textIndex % texts.length];
  elts.text2.textContent = texts[(textIndex + 1) % texts.length];
}

function doCooldown() {
  morph = 0;

  elts.text2.style.filter = "";
  elts.text2.style.opacity = "100%";

  elts.text1.style.filter = "";
  elts.text1.style.opacity = "0%";
}

// Animation loop, which is called every frame.
function animate() {
  requestAnimationFrame(animate);

  let newTime = new Date();
  let shouldIncrementIndex = cooldown > 0;
  let dt = (newTime - time) / 1000;
  time = newTime;

  cooldown -= dt;

  if (cooldown <= 0) {
    if (shouldIncrementIndex) {
      textIndex++;
    }

    doMorph();
  } else {
    doCooldown();
  }
}

// Start the animation.
animate();

/* Shadow Radial */



/* Please ❤ this if you like it! */


