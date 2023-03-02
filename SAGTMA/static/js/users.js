// ========== Modal de eliminar usuario ==========
var deleteModal = document.getElementById('deleteModal');
deleteModal.addEventListener('show.bs.modal', function (event) {
  // Obtiene el id del usuario
  var button = event.relatedTarget;
  var user_id = button.getAttribute('data-bs-whatever');

  // Modifica la acción del formulario para que tenga el id del usuario
  var form = deleteModal.querySelector('form');
  var action = form.getAttribute('action').split('/');
  action[action.length - 2] = user_id;
  new_action = action.join('/');
  form.setAttribute('action', new_action);
});