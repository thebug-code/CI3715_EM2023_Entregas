$(document).ready(function () {
  // Modificar proyecto
  $(document).on("click", ".modify-project", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/projects",
      data: { id },
      success: function (data) {
        $("#modifyModal").modal("show");
        var project = data[0];

        $("#descriptionM").val(project.description);
        $("#start_dateM").val(project.start_date);
        $("#deadlineM").val(project.deadline);
        $("#modifyProjectForm").attr(
          "action",
          "/project-portfolio/modify/" + id + "/"
        );
      },
    });
  });

  // Eliminar proyecto
  $(document).on("click", ".delete-project", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#deleteModal").modal("show");
    $("#deleteProjectForm").attr(
      "action",
      "/project-portfolio/delete/" + id + "/"
    );
  });

  // Cambiar status de proyecto
  $(document).on("click", ".change-status-project", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];
    $("#changeStatusModal").modal("show");
    $("#modalBodyCS").empty();

    // Verifica si se activa o desactiva proyecto
    if (form.attr("name") == "enable_project") {
      $("#modalBodyCS").append(
        "<p>¿Está seguro que desea activar este proyecto?</p>"
      );
      $("#submitButtonCS").attr("name", "enable_project");
      $("#submitButtonCS").addClass("btn-primary");
      $("#submitButtonCS").text("Activar");
    } else {
      $("#modalBodyCS").append(
        "<p>¿Está seguro que desea cerrar este proyecto?</p>"
      );
      $("#submitButtonCS").attr("name", "disable_project");
      $("#submitButtonCS").addClass("btn-danger");
      $("#submitButtonCS").text("Cerrar");
    }

    $("#changeStatusProjectForm").attr(
      "action",
      "/project-portfolio/modify/" + id + "/status/"
    );
  });
});
