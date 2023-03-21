$(document).ready(function() {
    // Eliminar departamento
    $(document).on('click', '.delete-dept', function() {
        var form = $(this);
        id = form.attr("id").match(/\d+/)[0];

        $("#deleteModal").modal('show');
        $("#delete-dept-form").attr(
            "action",
            "/workshop-departments/delete/" + id + "/"
        );
    });
});
