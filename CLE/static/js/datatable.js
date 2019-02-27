$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#studentdata').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    } );
    // $('#studentdata thead tr').clone(true).appendTo( '#studentdata thead' );
    // $('#studentdata thead tr:eq(1) th').each( function (i) {
    //     var title = $(this).text();
    //     $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    //
    //     $( 'input', this ).on( 'keyup change', function () {
    //         if ( table.column(i).search() !== this.value ) {
    //             table
    //                 .column(i)
    //                 .search( this.value )
    //                 .draw();
    //         }
    //     } );
    // } );

    // var table = $('#studentdata').DataTable( {
    //     orderCellsTop: true,
    //     fixedHeader: true
    // } );
} );
