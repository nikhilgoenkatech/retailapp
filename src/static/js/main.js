
const toggleModal = () => {
  document.querySelector('.modal')
    .classList.toggle('modal--hidden');
  document.querySelector('.overlay')
    .classList.toggle('overlay--hidden');
}

document.querySelector('#generate_report_id')
  .addEventListener('click', toggleModal);

document.querySelector('.overlay')
  .addEventListener('click', toggleModal);

document.querySelector('#close-modal-id')
  .addEventListener('click', toggleModal);

document.querySelector('.modal__close-bar span')
  .addEventListener('click', toggleModal);

document.querySelector('.overlay')
  .addEventListener('click', toggleModal);

