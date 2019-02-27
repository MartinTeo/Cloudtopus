$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-server .modal-content").html("");
        $("#modal-server").modal("show");
      },
      success: function (data) {
        $("#modal-server .modal-content").html(data.html_form);
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
          $("#server-table tbody").html(data.html_server_list);
          if(data.error_message != null){
            $("#errorMessage .modal-body").html(data.error_message);
            $('#errorMessage').modal('show');
          }
          else{
            $("#successMessage .modal-body").html(data.message);
            $('#successMessage').modal('show');
          }
          $("#modal-server").modal("hide");
        }
        else {
          $("#modal-server .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };




  /* Binding */

  // Create book
  $(".js-create-server").click(loadForm);
  $("#modal-server").on("submit", ".js-server-create-form", saveForm);

  // Update book
  $("#server-table").on("click", ".js-update-server", loadForm);
  $("#modal-server").on("submit", ".js-server-update-form", saveForm);

  // Delete book
  $("#server-table").on("click", ".js-delete-server", loadForm);
  $("#modal-server").on("submit", ".js-server-delete-form", saveForm);

});
