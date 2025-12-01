const API_BASE_URL = window.location.origin;
const USER_ID = "demo-user"; // simple fixed user for the lab

// DOM elements
const homeView = document.getElementById("home-view");
const cartView = document.getElementById("cart-view");
const orderView = document.getElementById("order-view");

const productsDiv = document.getElementById("products");
const cartItemsDiv = document.getElementById("cart-items");
const cartTotalSpan = document.getElementById("cart-total");
const cartCountSpan = document.getElementById("cart-count");
const cartMessage = document.getElementById("cart-message");
const orderMessage = document.getElementById("order-message");

const navHomeBtn = document.getElementById("nav-home");
const navCartBtn = document.getElementById("nav-cart");
const checkoutBtn = document.getElementById("checkout-btn");
const backHomeBtn = document.getElementById("back-home-btn");

// ---------- VIEW SWITCHING ----------
function showHome() {
  homeView.classList.remove("hidden");
  cartView.classList.add("hidden");
  orderView.classList.add("hidden");
}

function showCart() {
  homeView.classList.add("hidden");
  cartView.classList.remove("hidden");
  orderView.classList.add("hidden");
}

function showOrder() {
  homeView.classList.add("hidden");
  cartView.classList.add("hidden");
  orderView.classList.remove("hidden");
}

navHomeBtn.addEventListener("click", () => {
  showHome();
});

navCartBtn.addEventListener("click", () => {
  showCart();
  loadCart();
});

backHomeBtn.addEventListener("click", () => {
  showHome();
});

// ---------- API HELPERS ----------
async function apiGet(path) {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`POST ${path} failed: ${res.status} ${text}`);
  }
  return res.json();
}

// ---------- PRODUCTS ----------
async function loadProducts() {
  productsDiv.innerHTML = "Loading products...";
  try {
    const products = await apiGet("/api/v1/products");
    if (!Array.isArray(products) || products.length === 0) {
      productsDiv.innerHTML = "<p>No products found.</p>";
      return;
    }

    productsDiv.innerHTML = "";
    products.forEach((p) => {
      const card = document.createElement("div");
      card.className = "card";

      const price = p.price ?? p.unit_price ?? 0;

      card.innerHTML = `
        <h3>${p.name}</h3>
        <p>${p.category ?? ""}</p>
        <p><strong>$${price.toFixed ? price.toFixed(2) : price}</strong></p>
        <button data-id="${p.id}">Add to Cart</button>
      `;

      card.querySelector("button").addEventListener("click", () => {
        addToCart(p.id, 1, price);
      });

      productsDiv.appendChild(card);
    });
  } catch (err) {
    console.error(err);
    productsDiv.innerHTML = `<p id="error-message">Failed to load products.</p>`;
  }
}

// ---------- CART ----------
async function loadCart() {
  cartMessage.textContent = "";
  cartItemsDiv.innerHTML = "Loading cart...";
  try {
    const cart = await apiGet("/api/v1/cart");
    const items = cart.items ?? cart;

    if (!Array.isArray(items) || items.length === 0) {
      cartItemsDiv.innerHTML = "<p>Your cart is empty.</p>";
      cartTotalSpan.textContent = "0.00";
      cartCountSpan.textContent = "0";
      return;
    }

    cartItemsDiv.innerHTML = "";
    let total = 0;
    let count = 0;

    items.forEach((item) => {
      const row = document.createElement("div");
      row.className = "cart-row";

      const q = item.quantity ?? 1;
      const price = item.price ?? item.unit_price ?? 0;
      total += price * q;
      count += q;

      row.innerHTML = `
        <span>${item.product_name ?? item.name} (x${q})</span>
        <span>$${price.toFixed ? price.toFixed(2) : price}</span>
      `;
      cartItemsDiv.appendChild(row);
    });

    cartTotalSpan.textContent = total.toFixed(2);
    cartCountSpan.textContent = count.toString();
  } catch (err) {
    console.error(err);
    cartItemsDiv.innerHTML = `<p id="error-message">Failed to load cart.</p>`;
  }
}

async function addToCart(productId, quantity = 1) {
  try {
    await apiPost("/api/v1/cart/items", {
      user_id: USER_ID,
      product_id: productId,
      quantity,
    });
    cartMessage.textContent = "Item added to cart.";
    // refresh small cart badge
    await loadCart();
  } catch (err) {
    console.error(err);
    cartMessage.textContent = "Failed to add item to cart.";
  }
}

// ---------- CHECKOUT ----------
checkoutBtn.addEventListener("click", async () => {
  cartMessage.textContent = "";
  try {
    const order = await apiPost("/api/v1/orders", {
      user_id: USER_ID,
    });

    const orderId = order.id ?? order.order_id ?? "(no id)";
    orderMessage.textContent = `Order placed successfully. Order ID: ${orderId}`;
    showOrder();
    // reset cart badge
    cartCountSpan.textContent = "0";
    cartTotalSpan.textContent = "0.00";
  } catch (err) {
    console.error(err);
    cartMessage.textContent = "Failed to place order.";
  }
});

// ---------- INITIAL LOAD ----------
document.addEventListener("DOMContentLoaded", async () => {
  showHome();
  await loadProducts();
  // optional: preload cart count
  await loadCart();
});
