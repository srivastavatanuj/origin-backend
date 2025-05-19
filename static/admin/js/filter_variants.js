document.addEventListener("DOMContentLoaded", function () {
  const product = document.getElementById("id_product");
  const variants = document.getElementById("id_product_variant");

  if (product) {
    // Clone all options initially (snapshot, not live)
    const originalOptions = Array.from(variants.options).map((opt) =>
      opt.cloneNode(true)
    );

    product.onchange = (e) => {
      const productName = e.currentTarget?.value;

      const filteredOptions = originalOptions.filter((item) =>
        item.text.includes(productName)
      );

      // Clear current options
      variants.innerHTML = "";

      // Add filtered clones
      filteredOptions.forEach((item) => variants.add(item.cloneNode(true)));
    };
  }
});
