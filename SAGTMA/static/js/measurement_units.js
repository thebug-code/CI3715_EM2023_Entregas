$(document).ready(function () {
  // Eliminar unidad de medida
  $(document).on("click", ".delete-measure-unit", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-measure-unit-modal").modal("show");
    $("#delete-measure-unit-form").attr("action", "/measurement-units/" + id + "/delete/");
  });
});
