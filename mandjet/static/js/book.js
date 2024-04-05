function book() {
    var vehicleId = $('#vehicleIdInput').val();
    var start_date = $('#startDate').val();
    var end_date = $('#endDate').val();

    $.ajax({
        type: 'POST',
        url: bookUrl,
        data: {
            'vehicle_id': vehicleId,
            'startDate': start_date,
            'endDate': end_date,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            if (response.success) {
                alert("Successful Reservation!");
                window.location.href = '/home/';
                $('#reserveModal').modal('hide');
            } else {
                if (response.overlapping) {
                    alert("Vehicle is already reserved during the requested time period.");
                    window.location.href = '/home/';
                    $('#reserveModal').modal('hide');
                } else {
                    alert("Error: " + response.message);
                }
            }
        },
        error: function (xhr, status, error) {
            alert('An error occurred while processing the request.');
        }
    });
}