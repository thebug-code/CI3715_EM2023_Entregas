$(document).ready(function () {
  // Agregar detalles de proyecto
  $(document).on("click", ".add-project-detail", function () {
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
        const addVehiclesSelect = $("#add-vehicle");
        addVehiclesSelect.empty();

        // Agregar una opción por cada vehiculo
        vehicles.forEach(function (vehicle) {
          const option = $("<option>").attr("value", vehicle.id).attr("data-problem", vehicle.problem).text(`${vehicle.license_plate} | ${vehicle.brand} | ${vehicle.id_number} | ${vehicle.names} ${vehicle.surnames}`);

          // Agregar la opción al select
          addVehiclesSelect.append(option);
        });

        // Obtener el select de los departamentos y vaciar su contenido
        const addDepartmentsSelect = $("#add-department");
        addDepartmentsSelect.empty();

        // Agregar una opción por cada departamento
        departments.forEach(function (department) {
          const option = $("<option>").attr("value", department.id).text(department.description);

          // Agregar la opción al select
          addDepartmentsSelect.append(option);
        });

        // Obtener el select de los usuarios y vaciar su contenido
        const addUsersSelect = $("#add-manager");
        addUsersSelect.empty();

        // Agregar una opción por cada usuario
        users.forEach(function (user) {
          const option = $("<option>").attr("value", user.id).text(`${user.id_number} | ${user.names} ${user.surnames}`);

          // Agregar la opción al select
          addUsersSelect.append(option);
        });

        // Set the initial value of the problem field based on the selected vehicle
        updateProblemField("vehicle-select-add", "add-problem-field");

        // Attach an event listener to update the problem field when the user selects a different vehicle
        addVehiclesSelect.change(function () {
          updateProblemField("vehicle-select-add", "add-problem-field");
        });

        // Clear the problem field when the modal is closed
        $("#add-project-detail-modal").on("hidden.bs.modal", function () {
          clearProblemField("add-problem-field");
        });

        $("#add-project-detail-form").attr("action", "/project-details/" + id + "/register/");
      },
    });
  });

  // Modificar detalles de proyecto
  $(document).on("click", ".edit-project-detail", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/project-details",
      data: { id },
      success: function (data) {
        $("#edit-project-detail-modal").modal("show");
        var projectDetail = data.project_details[0];
        var users = data.dropdown_data.users;
        var vehicles = data.dropdown_data.vehicles;
        var departments = data.dropdown_data.departments;

        // Obtener el select de los vehiculos y vaciar su contenido
        const editVehiclesSelect = $("#edit-vehicle");
        editVehiclesSelect.empty();

        // Agregar una opción por cada vehiculo
        vehicles.forEach(function (vehicle) {
          const option = $("<option>").attr("value", vehicle.id).attr("data-problem", vehicle.problem).text(`${vehicle.license_plate} | ${vehicle.brand} | ${vehicle.id_number} | ${vehicle.names} ${vehicle.surnames}`);

          // Si el vehiculo es el actual, seleccionarlo por defecto
          if (vehicle.id === projectDetail.vehicle_id) {
            option.attr("selected", "selected");
          }

          // Agregar la opción al select
          editVehiclesSelect.append(option);
        });

        // Obtener el select de los departamentos y vaciar su contenido
        const editDepartmentsSelect = $("#edit-department");
        editDepartmentsSelect.empty();

        // Agregar una opción por cada departamento
        departments.forEach(function (department) {
          const option = $("<option>").attr("value", department.id).text(department.description);

          // Si el departamento es el actual, seleccionarlo por defecto
          if (department.id === projectDetail.department_id) {
            option.attr("selected", "selected");
          }

          // Agregar la opción al select
          editDepartmentsSelect.append(option);
        });

        // Obtener el select de los usuarios y vaciar su contenido
        const editUsersSelect = $("#edit-manager");
        editUsersSelect.empty();

        // Agregar una opción por cada usuario
        users.forEach(function (user) {
          const option = $("<option>").attr("value", user.id).text(`${user.id_number} | ${user.names} ${user.surnames}`);

          // Si el usuario es el actual, seleccionarlo por defecto
          if (user.id === projectDetail.manager_id) {
            option.attr("selected", "selected");
          }

          // Agregar la opción al select
          editUsersSelect.append(option);
        });

        // Set the initial value of the problem field based on the selected vehicle
        updateProblemField("vehicle-select-edit", "edit-problem-field");

        // Attach an event listener to update the problem field when the user selects a different vehicle
        editVehiclesSelect.change(function () {
          updateProblemField("vehicle-select-edit", "edit-problem-field");
        });

        // Clear the problem field when the modal is closed
        $("#edit-project-detail-modal").on("hidden.bs.modal", function () {
          clearProblemField("edit-problem-field");
        });

        $("#edit-solution").val(projectDetail.solution);
        $("#edit-amount").val(projectDetail.amount);
        $("#edit-observations").val(projectDetail.observations);

        $("#edit-project-detail-form").attr("action", "/project-details/" + id + "/edit/");
      },
    });
  });

  // Eliminar detalles de proyecto
  $(document).on("click", ".delete-project-detail", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $("#delete-project-detail-modal").modal("show");
    $("#delete-project-detail-form").attr("action", "/project-details/" + id + "/delete/");
  });
});

// Actualizar el campo de problema al seleccionar un vehículo
function updateProblemField(selectClass, selectId) {
  var vehicleSelect = document.getElementsByClassName(selectClass)[0];
  var selectedVehicleOption = vehicleSelect.options[vehicleSelect.selectedIndex];
  var problem = selectedVehicleOption.getAttribute("data-problem");

  var problemField = document.getElementById(selectId);
  problemField.innerHTML = '<label class="form-label" for="problem">Problema</label> <input type="text" class="form-control" name="problem" value="' + problem + '" readonly>';
}

// Limpiar el campo de problema
function clearProblemField(selectId) {
  var problemField = document.getElementById(selectId);
  problemField.innerHTML = "";
}
