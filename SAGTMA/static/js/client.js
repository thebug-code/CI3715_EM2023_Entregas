$(document).ready(function () {
  // Modificar cliente
  $(document).on("click", ".edit-client", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/clients",
      data: { id },
      success: function (data) {
        $("#edit-client-modal").modal("show");
        var client = data[0];

        $("#edit-id-number").val(client.id_number);
        $("#edit-names").val(client.names);
        $("#edit-surnames").val(client.surnames);
        $("#edit-birthdate").val(client.birthdate);
        $("#edit-phone-number").val(client.phone_number);
        $("#edit-email").val(client.email);
        $("#edit-address").val(client.address);
        $("#edit-client-form").attr(
          "action",
          "/client-details/edit/" + id + "/"
        );
      },
    });
  });

  // Eliminar cliente
  $(document).on("click", ".delete-client", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-client-modal").modal("show");
    $("#delete-client-form").attr(
      "action",
      "/client-details/delete/"+ id + "/"
    );
  });
});
