$(document).ready(function() {
  // Eliminar departamento
  $(document).on('click', '.delete-dept', function() {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#deleteModal").modal('show');
    $("#delete-dept-form").attr(
      "action",
      "/workshop-departments/delete/" + id + "/"
    );
  });

  // Editar departamento
  $(document).on("click", ".modify-dept", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/departments",
      data: { id },
      success: function (data) {
        $("#modifyModal").modal("show");
        var dept = data[0];

        $("#modify-description").val(dept.description);
        $("#modify-dept-form").attr(
          "action",
          "/workshop-departments/modify/" + id + "/"
        );
      },
    });
  });
});
