$(document).ready(function () {
  // Modificar vehiculo de cliente
  $(document).on("click", ".modify-client-vehicle", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/vehicles",
      data: { id },
      success: function (data) {
        $("#modifyModal").modal("show");
        var client = data[0];

        $("#modify-license-plate ").val(client.license_plate);
        $("#modify-brand").val(client.brand);
        $("#modify-model").val(client.model);
        $("#modify-year").val(client.year);
        $("#modify-body-number").val(client.body_number);
        $("#modify-engine-number").val(client.engine_number);
        $("#modify-color").val(client.color);
        $("#modify-problem").val(client.problem);
        $("#modify-client-vehicle-form").attr(
          "action",
          "/client-details/" + id + "/modify"
        );
      },
    });
  });

  // Eliminar vehiculo
  $(document).on("click", ".delete-vehicle", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#deleteModal").modal("show");
    $("#deleteVehicleForm").attr(
      "action",
      "/client-details/" + id + "/delete"
    );
  });
});
