$(document).ready(function () {
  // Modificar vehiculo de cliente
  $(document).on("click", ".edit-vehicle", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/vehicles",
      data: { id },
      success: function (data) {
        $("#edit-vehicle-modal").modal("show");
        var client = data[0];

        $("#edit-license-plate ").val(client.license_plate);
        $("#edit-brand").val(client.brand);
        $("#edit-model").val(client.model);
        $("#edit-year").val(client.year);
        $("#edit-body-number").val(client.body_number);
        $("#edit-engine-number").val(client.engine_number);
        $("#edit-color").val(client.color);
        $("#edit-problem").val(client.problem);
        $("#edit-vehicle-form").attr("action", "/client-details/" + id + "/edit/");
      },
    });
  });

  // Eliminar vehiculo
  $(document).on("click", ".delete-vehicle", function () ({
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-vehicle-modal").modal("show");
    $("#delete-vehicle-form").attr("action", "/client-details/" + id + "/delete/");
  });
});
