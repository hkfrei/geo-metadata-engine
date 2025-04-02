// update webmap elements
const updateWebMapForm = document.querySelector("#update_webmap_form");
const updateWebMapSpinner = document.querySelector("#update_webmap_spinner");
const updateWebMapBtn = document.querySelector("#update_webmap_btn");

// create webmap elements
const createWebMapForm = document.querySelector("#create_webmap_form");
const createWebMapBtn = document.querySelector("#create_webmap_btn");
const createWebMapSpinner = document.querySelector("#create_webmap_spinner");

// code for creating a new webmap.
if (createWebMapForm && createWebMapSpinner && createWebMapBtn) {
  createWebMapForm.addEventListener("submit", async (event) => {
    console.log("create submit clicked...");
    event.preventDefault();
    await processFormAction({
      form: createWebMapForm,
      btn: createWebMapBtn,
      spinner: createWebMapSpinner,
      href: "/createwebmapsuccess",
    });
  });
}

// code for updating a webmap
if (updateWebMapForm && updateWebMapSpinner && updateWebMapBtn) {
  updateWebMapForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await processFormAction({
      form: updateWebMapForm,
      btn: updateWebMapBtn,
      spinner: updateWebMapSpinner,
      href: "/updatewebmapsuccess",
    });
  });
}

/**
 * Handles the submission of a form by showing a loading spinner, sending the form data via a POST request,
 * and redirecting the user to a specified URL upon success. If the request fails, it logs the error to the console.
 *
 * @param {object} params - The parameters for the function.
 * @param {HTMLFormElement} params.form - The form element to be submitted.
 * @param {HTMLElement} params.btn - The button element to be hidden during processing.
 * @param {HTMLElement} params.spinner - The spinner element to be shown during processing.
 * @param {string} params.href - The URL to redirect to upon successful form submission.
 */
const processFormAction = async ({ form, btn, spinner, href }) => {
  const toggleSpinner = (show) => {
    btn.classList.toggle("visually-hidden", show);
    spinner.classList.toggle("visually-hidden", !show);
  };

  try {
    const formData = new FormData(form);
    toggleSpinner(true);

    const response = await fetch(form.action, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      document.location.href = href;
    } else {
      console.error(data.error || "An unknown error occurred.");
    }
  } catch (error) {
    console.error("Error processing form action:", error);
  } finally {
    toggleSpinner(false);
  }
};
