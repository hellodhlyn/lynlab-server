var reload_interval = 10;
var reload_left = -1;

$(document).ready(function() {
	var reload_timer = setInterval(function () {
		if (reload_left > 0) {
			reload_left -= 1;
		}
		$('#reload-time').html(reload_left)
	}, 1000);

	// Request bus info
	var req_url = '/dashboard/bus';
	$.get(req_url, function(data) {
		$('.dashboard-buses').html(data);
		reload_left = 10;
	});

	setInterval(function () {
		$('.dashboard-buses').fadeOut('fast', function() {
			$(this).load('/dashboard/bus', function() {
				$(this).fadeIn('fast');
			});
		});
		reload_left = 10;
	}, reload_interval * 1000);
});