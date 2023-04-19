$(document).ready(function () {
  // Agregar un nuevo plan de acción
  $(document).on("click", ".add-action-plan", function () {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];

    $.getJSON({
      url: "/api/v1/action-plans-dropdown-data",
      data: { id },
      success: function (data) {
        $("#add-action-plan-modal").modal("show");
        var users = data.users;
        var actions = data.actions;
        var units = data.measureUnits;

        // Obtener el select de usuarios y vaciar su contenido
        const addPlanChargePersonSelect = $("#add-charge-person");
        addPlanChargePersonSelect.empty();

        // Agregar opción "Seleccione una opción"
        const defaultOptionUser = $("<option>").attr("value", "").attr("disabled", true).attr("selected", true).text("Seleccione un usuario");
        addPlanChargePersonSelect.append(defaultOptionUser);

        // Agregar una opción por cada usuario
        users.forEach(function (user) {
          const option = $("<option>")
            .attr("value", user.id)
            .text(user.names + " " + user.surnames);

          // Agregar la opción al select
          addPlanChargePersonSelect.append(option);
        });

        // Obtener los campos de acción existente y nueva acción
        const existingActionFields = $("#existing-action-fields");
        const newActionFields = $("#new-action-fields");

        // Obtener los select de accion existente
        const existingActionSelect = $("#existing-action");

        // Obtener el campo de nueva acción
        const newActionInput = $("#new-action");

        // Obtener el select de tipo de acción
        const actionTypeSelect = $("#action-type");

        // Agregar un listener para detectar cambios
        actionTypeSelect.change(function () {
          // Obtener el valor del select
          const actionType = $(this).val();

          // Actualizar el campo oculto "action-type-hidden" cada vez que cambie el valor del campo
          // "Tipo de acción"
          $("#action-type-hidden").val(actionType);

          // Mostrar u ocultar los campos según la opción seleccionada
          if (actionType === "existing") {
            newActionInput.prop("required", false);
            existingActionSelect.prop("required", true);
            newActionFields.hide();
            existingActionFields.show();

            // Obtener el select de acciones y vaciar su contenido
            const actionsSelect = existingActionFields.children().eq(1);
            actionsSelect.empty();

            // Agregar opción "Seleccione una opción"
            const defaultOptionAction = $("<option>").attr("value", "").attr("disabled", true).attr("selected", true).text("Seleccione una acción");
            actionsSelect.append(defaultOptionAction);

            // Agregar una opción por cada acción
            actions.forEach(function (action) {
              const option = $("<option>").attr("value", action.id).text(action.description);

              // Agregar la opción al select
              actionsSelect.append(option);
            });
          } else if (actionType === "new") {
            existingActionSelect.prop("required", false);
            newActionInput.prop("required", true);
            existingActionFields.hide();
            newActionFields.show();
          } else {
            existingActionSelect.prop("required", false);
            newActionInput.prop("required", false);
            existingActionFields.hide();
            newActionFields.hide();
          }
        });

        // Obtener el select de unidades de medida y vaciar su contenido
        const measureUnitSelect = $("#measure-unit-ms");
        measureUnitSelect.empty();

        // Agregar opción "Seleccione una opción"
        const defaultOptionUnit = $("<option>").attr("value", "").attr("disabled", true).attr("selected", true).text("Seleccione una unidad de medida");
        measureUnitSelect.append(defaultOptionUnit);

        // Agregar una opción por cada unidad de medida
        units.forEach(function (unit) {
          const option = $("<option>").attr("value", unit.id).text(unit.dimension).text(`${unit.dimension} ${unit.unit}`);

          // Agregar la opción al select
          measureUnitSelect.append(option);
        });

        $("#add-action-plan-form").attr("action", "/action-plans/" + id + "/register/");
      },
    });
  });

  // Eliminar un plan de acción
  $(document).on("click", ".delete-action-plan", function (event) {
    var form = $(this);
    id = form.attr("id").match(/\d+/)[0];
    const activityId = $(event.currentTarget).attr("data-activity-id");

    // Establece el valor del campo oculto "delete-activity-id" con el valor del id de la actividad
    $("#delete-activity-id").val(activityId);

    $("#delete-action-plan-modal").modal("show");
    $("#delete-action-plan-form").attr("action", "/action-plans/" + id + "/delete/");
  });

  // Editar un plan de acción
  $(document).on("click", ".edit-action-plan", function (event) {
    const actionId = $(event.currentTarget).attr("data-action-id");
    const activityId = $(event.currentTarget).attr("data-activity-id");
    const materialSupplyId = $(event.currentTarget).attr("data-material-supply-id");
    const humanTalentId = $(event.currentTarget).attr("data-human-talent-id");

    $.getJSON({
      url: "/api/v1/action-plans",
      data: { action_id: actionId, activity_id: activityId, material_supply_id: materialSupplyId, human_talent_id: humanTalentId },
      success: function (data) {
        $("#edit-action-plan-modal").modal("show");
        const actionPlan = data.actionPlans[actionId];
        const activity = actionPlan.activities[0];
        const users = data.users;
        const units = data.measureUnits;
        const humanTalent = activity.human_talents[0];
        const materialSupply = activity.material_supplies[0];

        // Obtener el select de usuarios y vaciar su contenido
        const editPlanChargePersonSelect = $("#edit-charge-person");
        editPlanChargePersonSelect.empty();

        // Agregar una opción por cada usuario
        users.forEach(function (user) {
          const option = $("<option>")
            .attr("value", user.id)
            .text(user.names + " " + user.surnames);

          // Si el usuario es el responsable del plan de acción, seleccionarlo
          // por defecto
          if (user.id === activity.charge_person_id) {
            option.attr("selected", "selected");
          }

          // Agregar la opción al select
          editPlanChargePersonSelect.append(option);
        });

        // Obtener el select de unidades de medida y vaciar su contenido
        const editMeasureUnitSelect = $("#edit-measure-unit-ms");
        editMeasureUnitSelect.empty();

        // Agregar una opción por cada unidad de medida
        units.forEach(function (unit) {
          const option = $("<option>").attr("value", unit.id).text(`${unit.dimension} ${unit.unit}`);

          // Si la unidad de medida es la misma que la del plan de acción, seleccionarla
          // por defecto
          if (unit.id === materialSupply.unit_id) {
            option.attr("selected", "selected");
          }

          // Agregar la opción al select
          editMeasureUnitSelect.append(option);
        });

        $("#edit-action").val(actionPlan.action);
        $("#edit-activity").val(activity.description);
        $("#edit-start-date").val(activity.start_date);
        $("#edit-deadline").val(activity.deadline);
        $("#edit-work-hours").val(activity.work_hours);
        $("#edit-amount-person-hl").val(humanTalent.amount_persons);
        $("#edit-cost-hl").val(humanTalent.cost_hl);
        $("#edit-category-ms").val(materialSupply.category);
        $("#edit-description-ms").val(materialSupply.description);
        $("#edit-amount-ms").val(materialSupply.amount);
        $("#edit-cost-ms").val(materialSupply.cost);

        // Establece los valores de los inputs
        $("#activity-id").val(activityId);
        $("#action-id").val(actionId);
        $("#human-talent-id").val(humanTalentId);
        $("#material-supply-id").val(materialSupplyId);

        $("#edit-action-plan-form").attr("action", "/action-plans/" + actionId + "/edit/");
      },
    });
  });
});

// Paginación del modal

// Obtener todos los botones de página
const pageBtns = document.querySelectorAll(".page-btn");

// Agregar un controlador de eventos a cada botón de página
pageBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    // Obtener el nombre de la página correspondiente a este botón
    const pageName = btn.dataset.page;

    // Ocultar todas las páginas
    document.querySelectorAll(".page").forEach((page) => {
      page.style.display = "none";
    });

    // Mostrar solo la página correspondiente a este botón
    document.querySelector(`.${pageName}`).style.display = "block";

    // Marcar este botón como activo y desmarcar los otros
    pageBtns.forEach((btn) => {
      btn.classList.remove("active");
    });
    btn.classList.add("active");
  });
});