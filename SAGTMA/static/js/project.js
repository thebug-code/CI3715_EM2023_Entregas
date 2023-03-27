$(document).ready(function () {
  // Modificar proyecto
  $(document).on("click", ".edit-project", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/projects",
      data: { id },
      success: function (data) {
        $("#edit-project-modal").modal("show");
        var project = data[0];

        $("#edit-description").val(project.description);
        $("#edit-start-date").val(project.start_date);
        $("#edit-deadline").val(project.deadline);
        $("#edit-project-form").attr(
          "action",
          "/project-portfolio/edit/" + id + "/"
        );
      },
    });
  });

  // Eliminar proyecto
  $(document).on("click", ".delete-project", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-project-modal").modal("show");
    $("#delete-project-form").attr(
      "action",
      "/project-portfolio/" + id + "/delete/"
    );
  });

  // Cambiar status de proyecto
  $(document).on("click", ".change-project-status", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];
    $("#change-project-status-modal").modal("show");
    $("#modal-body-cs").empty();

    // Verifica si se activa o desactiva proyecto
    if (form.attr("name") == "enable-project") {
      $("#modal-body-cs").append(
        "<p>¿Está seguro que desea activar este proyecto?</p>"
      );
      $("#submit-button-cs").attr("name", "enable-project");
      $("#submit-button-cs").addClass("btn-primary");
      $("#submit-button-cs").text("Activar");
    } else {
      $("#modal-body-cs").append(
        "<p>¿Está seguro que desea cerrar este proyecto?</p>"
      );
      $("#submit-button-cs").attr("name", "disable-project");
      $("#submit-button-cs").addClass("btn-danger");
      $("#submit-button-cs").text("Cerrar");
    }

    $("#change-project-status-form").attr(
      "action",
      "/project-portfolio/edit/" + id + "/status/"
    );
  });
});
