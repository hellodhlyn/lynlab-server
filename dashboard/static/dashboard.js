$(document).ready(function() {
	// Request bus info
	var req_url = '/dashboard/bus';
	$.get(req_url, function(data) {
		$('.dashboard-buses').html(data);
	});

	var auto_refresh = setInterval(function () {
	    $('.dashboard-buses').fadeOut('fast', function() {
	        $(this).load('/dashboard/bus', function() {
	            $(this).fadeIn('fast');
	        });
	    });
	}, 10 * 1000);
});