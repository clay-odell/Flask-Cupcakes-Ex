function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
$(function () {
  async function getCupCakes() {
    let resp = await axios.get("/api/cupcakes");
    for (let cupcake of resp.data.cupcakes) {
      $("#cupcakesUL").append(
        `<li>${capitalizeFirstLetter(cupcake.flavor)}</li>`
      );
    }
  }
  async function handleFormSubmit(evt) {
    evt.preventDefault();
    let flavor = $("#flavor").val();
    let size = $("#size").val();
    let rating = $("#rating").val();
    let image = $("#image").val();
    let resp = await axios.post("/api/cupcakes", {
      flavor: flavor,
      size: size,
      rating: rating,
      image: image,
    });
    $("#cupcakeForm")[0].reset();
    $("#cupcakesUL").empty();
    getCupCakes(); 
  }
  $("#cupcakeForm").submit(handleFormSubmit);

  getCupCakes();
});
