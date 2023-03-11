$(document).ready(function () {
  // Modificar cliente
  $(document).on("click", ".modify-client", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/clients",
      data: { id },
      success: function (data) {
        $("#modifyModal").modal("show");
        var client = data[0];

        $("#modifyIdNumber").val(client.id_number);
        $("#modifyNames").val(client.names);
        $("#modifySurnames").val(client.surnames);
        $("#modifyBirthdate").val(client.birthdate);
        $("#modifyPhoneNumber").val(client.phone_number);
        $("#modifyEmail").val(client.email);
        $("#modifyAddress").val(client.address);
        $("#modifyClientForm").attr(
          "action",
          "/client-details/modify/" + id + "/"
        );
      },
    });
  });

  // Eliminar cliente
  $(document).on("click", ".delete-client", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#deleteModal").modal("show");
    $("#deleteClientForm").attr("action", "/client-details/delete/" + id + "/");
  });
});
