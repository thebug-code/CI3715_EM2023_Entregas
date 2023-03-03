// Modificar proyecto
$(document).ready(function () {
  $(document).on("click", ".modify-project", function () {
    var form = $(this);
    $.ajax({
      url: "/select",
      method: "POST",
      data: { project_id: form.attr("id") },
      success: function (data) {
        $("#modifyModal").modal("show");
        var data_rs = JSON.parse(data);
        $("#descriptionM").val(data_rs[0]["description"]);
        $("#start_dateM").val(data_rs[0]["start_date"]);
        $("#deadlineM").val(data_rs[0]["deadline"]);
        $("#modifyProjectForm").attr(
          "action",
          "/project-portfolio/modify/" + form.attr("id") + "/"
        );
      },
    });
  });

  // Eliminar proyecto
  $(document).on("click", ".delete-project", function () {
    var form = $(this);
    $("#deleteModal").modal("show");
    $("#deleteProjectForm").attr(
      "action",
      "/project-portfolio/delete/" + form.attr("id") + "/"
    );
  });

  // Cambiar status de proyecto
  $(document).on("click", ".change-status-project", function () {
    var form = $(this);
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
      "/project-portfolio/modify/"+ form.attr("id") + "/status/"
    );
  });
});
