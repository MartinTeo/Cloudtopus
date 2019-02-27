$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-trailhead .modal-content").html("");
        $("#modal-trailhead").modal("show");
      },
      success: function (data) {
        $("#modal-trailhead .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#trailhead-table tbody").html(data.html_trailhead_list);
          if(data.error_message != null){
            $("#errorMessage .modal-body").html(data.error_message);
            $('#errorMessage').modal('show');
          }
          else{
            $("#successMessage .modal-body").html(data.message);
            $('#successMessage').modal('show');
          }
          $("#modal-trailhead").modal("hide");
        }
        else {
          $("#modal-trailhead .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };




  /* Binding */

  // Create book
  $(".js-create-trailhead").click(loadForm);
  $("#modal-trailhead").on("submit", ".js-trailhead-create-form", saveForm);

  // Update book
  $("#trailhead-table").on("click", ".js-update-trailhead", loadForm);
  $("#modal-trailhead").on("submit", ".js-trailhead-update-form", saveForm);

  // Delete book
  $("#trailhead-table").on("click", ".js-delete-trailhead", loadForm);
  $("#modal-trailhead").on("submit", ".js-trailhead-delete-form", saveForm);

});
