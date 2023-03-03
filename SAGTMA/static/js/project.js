// Modificar proyecto
$(document).ready(function(){
  $(document).on('click', '.modifyProject', function() {
    var form = $(this)
    $.ajax({
     url: "/select",
     method: "POST",
     data: {project_id: form.attr("id")},
     success: function(data) {
      $('#modifyModal').modal('show');
      var data_rs = JSON.parse(data);
      $('#descriptionM').val(data_rs[0]['description']);
      $('#start_dateM').val(data_rs[0]['start_date']);
      $('#deadlineM').val(data_rs[0]['deadline']);
      $('#modifyProjectForm').attr('action', "/project-portfolio/modify/" + form.attr("id"));
   }
  });
 });

  // Eliminar proyecto
  $(document).on('click', '.deleteProject', function() {
    var form = $(this)
    $('#deleteModal').modal('show');
    $('#deleteProjectForm').attr('action', "/project-portfolio/delete/" + form.attr("id"));
 });
});
