const updateWebMapForm = document.querySelector("#update_webmap_form");
const updateWebMapSpinner = document.querySelector("#update_webmap_spinner");
const updateWebMapBtn = document.querySelector("#update_webmap_btn");

if (updateWebMapForm && updateWebMapSpinner && updateWebMapBtn) {
  updateWebMapForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(updateWebMapForm);

    updateWebMapBtn.classList.add("visually-hidden");
    updateWebMapSpinner.classList.remove("visually-hidden");

    const response = await fetch(updateWebMapForm.action, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      document.location.href = "/updatewebmapsuccess";
    } else {
      console.error(data.error);
    }
    updateWebMapBtn.classList.remove("visually-hidden");
    updateWebMapSpinner.classList.add("visually-hidden");
  });
}
