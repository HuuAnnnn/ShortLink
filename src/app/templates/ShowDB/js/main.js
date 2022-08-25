// $('[data-toggle="tooltip"]').tooltip();
const act_btn = document.querySelector(".disabled")

if (act_btn) {
  act_btn.addEventListener('click', (e) => {
    e.preventDefault();
    act_btn.classList.add('cursor-not-allowed');
  })
}

