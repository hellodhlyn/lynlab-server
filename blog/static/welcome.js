$(document).ready(function() {
	$('.ui.dropdown').dropdown();

	$('#sidebar-icon').on('click', function() {
        $("#main-sidebar")
            .sidebar('setting', 'transition', 'overlay')
            .sidebar('toggle');
	});
});