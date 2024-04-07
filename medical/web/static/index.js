function deleteTreatment(treatmentId) {
  fetch("/delete-treatment", {
    method: "POST",
    body: JSON.stringify({ treatmentId: treatmentId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}