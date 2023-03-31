$(document).ready(function () {
  // Agregar detalles de proyecto
  $(document).on('click', '.add-project-detail', function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];
    
    $.getJSON({
      url: "/api/v1/project-details-dropdown-data",
      success: function (data) {
        $("#add-project-detail-modal").modal("show");
        var users = data.users;
        var vehicles = data.vehicles;
        var departments = data.departments;
     
        // Obtener el select de los vehiculos y vaciar su contenido
        const addVehiclesSelect = $('#add-vehicle');
        addVehiclesSelect.empty();

        // Agregar una opción por cada vehiculo
        vehicles.forEach(function(vehicle) {
          const option = $('<option>')
          .attr('value', vehicle.id)
          .attr('data-problem', vehicle.problem)
          .text(vehicle.license_plate + ' - ' + vehicle.brand + ' - ' +
            vehicle.id_number + ' - ' + vehicle.names + ' ' + vehicle.surnames);
    
          // Agregar la opción al select
          addVehiclesSelect.append(option);
        });

        // Obtener el select de los departamentos y vaciar su contenido
        const addDepartmentsSelect = $('#add-department');
        addDepartmentsSelect.empty();
        
        // Agregar una opción por cada departamento
        departments.forEach(function(department) {
          const option = $('<option>')
          .attr('value', department.id)
          .text(department.description);
          
          // Agregar la opción al select 
          addDepartmentsSelect.append(option);
        });

        // Obtener el select de los usuarios y vaciar su contenido
        const addUsersSelect = $('#add-manager');
        addUsersSelect.empty();

        // Agregar una opción por cada usuario
        users.forEach(function(user) {
          const option = $('<option>')
          .attr('value', user.id)
          .text(user.id_number + ' - ' + user.names + ' ' + user.surnames);

          // Agregar la opción al select
          addUsersSelect.append(option);
        });

        // Set the initial value of the problem field based on the selected vehicle
        updateProblemField();

        // Attach an event listener to update the problem field when the user selects a different vehicle
        //addVehiclesSelect.on('change', updateProblemField);

        $("#add-project-detail-form").attr(
          "action",
          "/project-details/" + id + "/register/"
        );
      },
    });
  });

  // Modificar usuario
  //$(document).on("click", ".edit-user", function () {
  //  var form = $(this);
  //  id = form.attr("id").match(/\d+/)[0];

  //  $.getJSON({
  //    url: "/api/v1/users",
  //    data: { id },
  //    success: function (data) {
  //      $("#edit-user-modal").modal("show");
  //      var user = data.users[0];
  //      var roles = data.roles;

  //      $("#edit-username").val(user.username);
  //      $("#edit-names").val(user.names);
  //      $("#edit-surnames").val(user.surnames);
  //      $("#edit-id-number").val(user.id_number);
  //      
  //      // Obtener el select de roles y vaciar su contenido
  //      const editRolesSelect = $('#edit-roles');
  //      editRolesSelect.empty();

  //      // Agregar una opción por cada rol
  //      roles.forEach(function(role) {
  //        const option = $('<option>')
  //        .attr('value', role.id)
  //        .text(role.name);
  //  
  //      // Si el rol es el actual, seleccionarlo por defecto
  //      if (role.id === user.role_id) {
  //        option.attr('selected', 'selected');
  //      }

  //      // Agregar la opción al select
  //      editRolesSelect.append(option);
  //    });

  //      $("#edit-user-form").attr(
  //        "action",
  //        "/user-profiles/" + id + "/edit/"
  //      );
  //    },
  //  });
  //});

  // Eliminar usuario
  //$(document).on("click", ".delete-user", function () {
  //  var form = $(this);
  //  id = form.attr("id").match(/\d+/)[0];

  //  $("#delete-user-modal").modal("show");
  //  $("#delete-user-form").attr(
  //    "action",
  //    "/user-profiles/" + id + "/delete/");
  //});
});

// Actualizar el campo de problema al seleccionar un vehículo
function updateProblemField() {
  var vehicleSelect = document.getElementsByName('vehicle')[0];
  var selectedVehicleOption = vehicleSelect.options[vehicleSelect.selectedIndex];
  var problem = selectedVehicleOption.getAttribute('data-problem');

  var problemField = document.getElementById('problem-field');
  problemField.innerHTML = '<label class="form-label" for="problem">Problema</label> <input type="text" class="form-control" name="problem" value="' + problem + '" readonly>';
}

// Limpiar el campo de problema
function clearProblemField() {
    var problemField = document.getElementById('problem-field');
    problemField.innerHTML = '';
}
