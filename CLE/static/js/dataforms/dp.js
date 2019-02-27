$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-dp .modal-content").html("");
        $("#modal-dp").modal("show");
      },
      success: function (data) {
        $("#modal-dp .modal-content").html(data.html_form);
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
          $("#dp-table tbody").html(data.html_dp_list);
          if(data.error_message != null){
            $("#errorMessage .modal-body").html(data.error_message);
            $('#errorMessage').modal('show');
          }
          else{
            $("#successMessage .modal-body").html(data.message);
            $('#successMessage').modal('show');
          }
          $("#modal-dp").modal("hide");
        }
        else {
          $("#modal-dp .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };




  /* Binding */

  // Create book
  $(".js-create-dp").click(loadForm);
  $("#modal-dp").on("submit", ".js-dp-create-form", saveForm);

  // Update book
  $("#dp-table").on("click", ".js-update-dp", loadForm);
  $("#modal-dp").on("submit", ".js-dp-update-form", saveForm);

  // Delete book
  $("#dp-table").on("click", ".js-delete-dp", loadForm);
  $("#modal-dp").on("submit", ".js-dp-delete-form", saveForm);

});
