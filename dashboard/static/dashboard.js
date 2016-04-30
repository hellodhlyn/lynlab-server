const reload_interval = 20;
var reload_left = 0;
var notified_bus = [];

var isPaused = true;

// For notifactions
function onShowNotification () {
	console.log('notification is shown!');
}
function onCloseNotification () {
	console.log('notification is closed!');
}
function onClickNotification () {
	console.log('notification was clicked!');
}
function onErrorNotification () {
	console.error('Error showing notification. You may need to request permission.');
}
function onPermissionGranted () {
	console.log('Permission has been granted by the user');
}
function onPermissionDenied () {
	console.warn('Permission has been denied by the user');
}
function doNotification (id, busNum, leftTime, people) {
	if (notified_bus.includes(id)) return;
	notified_bus.push(id);

	var message = busNum + '번 버스가 ' + leftTime + ' 후에 도착합니다. (' + people + '명 탑승)';

	var myNotification = new Notify('버스가 곧 도착합니다.', {
		body: message,
		tag: 'LYnDashboard_BUS',
		icon: '/static/bus.png',
		notifyShow: onShowNotification,
		notifyClose: onCloseNotification,
		notifyClick: onClickNotification,
		notifyError: onErrorNotification,
		timeout: 20
	});
	myNotification.show();
}

$(document).ready(function() {
	function request() {
		$('.dashboard-buses').fadeOut('fast', function() {
			$(this).load('/dashboard/bus', function() {
				$(this).fadeIn('fast');
			});
		});
	}

	// Notification auth
	$('body').append('<button id="permission-request-button"></button>');
	$('#permission-request-button').click(function() {
		if (Notify.needsPermission && Notify.isSupported()) {
            Notify.requestPermission(onPermissionGranted, onPermissionDenied);
        }
	});
	$('#permission-request-button').click();

	// Set timers
	var reload_timer = setInterval(function() {
		if (!isPaused) {
			if (reload_left > 0) {
				reload_left -= 1;
			}
			else {
				request();
				reload_left = reload_interval;
			}
		}
		$('#reload-time').html(reload_left)
	}, 1000);

	// Pause-resume toggle
	$('#btn-pause').click(function() {
		if ($('#btn-pause').children().hasClass('pause')) {
			isPaused = true;
			$('#btn-pause').html('<i class="play icon"></i>');
		}
		else {
			isPaused = false;
			$('#btn-pause').html('<i class="pause icon"></i>');
		}
	});

	request();
});