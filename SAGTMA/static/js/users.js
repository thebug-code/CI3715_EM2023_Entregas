$(document).ready(function () {
  // Modificar usuario
  $(document).on("click", ".edit-user", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/users",
      data: { id },
      success: function (data) {
        $("#edit-user-modal").modal("show");
        var user = data.users[0];
        var roles = data.roles;

        $("#edit-username").val(user.username);
        $("#edit-names").val(user.names);
        $("#edit-surnames").val(user.surnames);
        $("#edit-id-number").val(user.id_number);
        
        // Obtener el select de roles y vaciar su contenido
        const editRolesSelect = $('#edit-roles');
        editRolesSelect.empty();

        // Agregar una opción por cada rol
        roles.forEach(function(role) {
          const option = $('<option>')
          .attr('value', role.id)
          .text(role.name);
    
        // Si el rol es el actual, seleccionarlo por defecto
        if (role.id === user.role_id) {
          option.attr('selected', 'selected');
        }

        // Agregar la opción al select
        editRolesSelect.append(option);
      });

        $("#edit-user-form").attr(
          "action",
          "/user-profiles/" + id + "/edit/"
        );
      },
    });
  });

  // Eliminar usuario
  $(document).on("click", ".delete-user", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-user-modal").modal("show");
    $("#delete-user-form").attr(
      "action",
      "/user-profiles/" + id + "/delete/");
  });
});
