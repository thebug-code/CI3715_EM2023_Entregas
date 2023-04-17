$(document).ready(function () {
  // Eliminar unidad de medida
  $(document).on("click", ".delete-measure-unit", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-measure-unit-modal").modal("show");
    $("#delete-measure-unit-form").attr("action", "/measurement-units/" + id + "/delete/");
  });

  // Editar unidad de medida
  $(document).on("click", ".edit-measure-unit", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/measurement-units/",
      data: { "measurement-unit-id": id },
      success: function (data) {
        $("#edit-measure-unit-modal").modal("show");
        var measure_unit = data[0];

        $("#edit-dimension").val(measure_unit.dimension);
        $("#edit-unit").val(measure_unit.unit);

        $("#edit-measure-unit-form").attr("action", "/measurement-units/" + id + "/edit/");
      },
    });
  });
});
