// AJAX Add to Cart
document.addEventListener("DOMContentLoaded", () => {
  // Show toast helper
  function showToast(msg) {
    let toast = document.querySelector(".toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "toast";
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2500);
  }

  // Handle all "Add to Cart" buttons
  document.querySelectorAll(".add-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const id = btn.dataset.id;

      // Get qty if on product detail page
      const qtyInput = document.getElementById("qty-input");
      const qty = qtyInput ? parseInt(qtyInput.value) : 1;

      try {
        const res = await fetch(`/add/${id}`, { method: "POST" });
        const data = await res.json();

        // Update cart badge & label in header
        const badge = document.querySelector(".badge");
        const label = document.querySelector(".cart-label");
        if (data.count > 0) {
          if (badge) {
            badge.textContent = data.count;
          } else {
            const cartBtn = document.querySelector(".cart-btn");
            const newBadge = document.createElement("span");
            newBadge.className = "badge";
            newBadge.textContent = data.count;
            cartBtn.insertBefore(newBadge, cartBtn.firstChild);
          }
        }
        if (label) label.textContent = `Cart · $${data.total}`;

        // Visual feedback on button
        const original = btn.textContent;
        btn.textContent = "✓ Added";
        btn.classList.add("added");
        setTimeout(() => {
          btn.textContent = original;
          btn.classList.remove("added");
        }, 1500);

        showToast("Added to cart!");
      } catch (err) {
        console.error("Cart error:", err);
      }
    });
  });
});
