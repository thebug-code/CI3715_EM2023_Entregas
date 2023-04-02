$(document).ready(function () {
  // Eliminar departamento
  $(document).on("click", ".delete-dept", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-dept-modal").modal("show");
    $("#delete-dept-form").attr("action", "/workshop-departments/" + id + "/delete/");
  });

  // Editar departamento
  $(document).on("click", ".edit-dept", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/departments",
      data: { id },
      success: function (data) {
        $("#edit-dept-modal").modal("show");
        var dept = data[0];

        $("#edit-description").val(dept.description);
        $("#edit-dept-form").attr("action", "/workshop-departments/" + id + "/edit/");
      },
    });
  });
});
