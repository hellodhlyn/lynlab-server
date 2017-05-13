$(document).ready(() => {
    $('#menu-toggle').click(() => {
        $('.ui.sidebar')
		    .sidebar('setting', 'transition', 'overlay')
		    .sidebar('toggle');
    });
});