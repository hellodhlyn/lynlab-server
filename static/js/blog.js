var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	beforeSend: function(xhr, settings){
		if(!csrfSafeMethod(settings.type) && !this.crossDomain){
			xhr.setRequestHeader("X-CSRFToken",csrftoken);
		}
	}
});

function loadTwitterApi() {
	window.twttr = (function(d, s, id) {
		var js, fjs = d.getElementsByTagName(s)[0],
		t = window.twttr || {};
		if (d.getElementById(id)) return t;
		js = d.createElement(s);
		js.id = id;
		js.src = "https://platform.twitter.com/widgets.js";
		fjs.parentNode.insertBefore(js, fjs);

		t._e = [];
		t.ready = function(f) {
			t._e.push(f);
		};

		return t;
	}(document, "script", "twitter-wjs"));
}

function toggleFilter() {
	$('#filter-modal').modal({
		onApprove: function() {
			$('.filter.button').each(function(){
				if ($('#'+$(this).attr('id')).hasClass('blue')) {
					$.cookie($(this).attr('id'), 0);
				}
				else {
					$.cookie($(this).attr('id'), 1);
				}
			})
		}
	})
	.modal('show');
}

function toggleFilterButton(id) {
	if ($('#filter'+id).hasClass('blue')) {
		$('#filter'+id).removeClass('blue')
	}
	else {
		$('#filter'+id).addClass('blue')	
	}
}

function getFilter() {
	var length = $('.filter.button').length+1;
	var list = Array();
	$('.filter.button').each(function(){
		if (!$('#'+$(this).attr('id')).hasClass('blue')) {
			list.push($(this).attr('id').replace(/[^0-9]/g,""));
		}
	})

	var result = '';
	for (var i=0; i<list.length; i++) {
		result = result + list[i] + ',';
	}
	return result;
}

function loadPosts(page) {
	$('#more-button').remove();
	var filters = getFilter();

	$.ajax({
		url: '/api/blog/posts/',
		method: 'post',
		data: {
			'page': page,
			'filters': filters,
		},
		dataType:'html',
		success : function(data){
			$('.posts').append(data);
			$('.posts').append('<button class="ui basic fluid button" id="more-button" onclick="loadPosts('+(page+1)+');">더 보기</button>');
		}
	});
}

function loadPosts(page, key, value) {
	$('#more-button').remove();
	var filters = getFilter();

	$.ajax({
		url: '/api/blog/posts/',
		method: 'post',
		data: {
			'key': key,
			'value': value,
			'page': page,
			'filters': filters,
		},
		dataType:'html',
		success : function(data){
			$('.posts').append(data);
			$('.posts').append('<button class="ui basic fluid button" id="more-button" onclick="loadPosts('+(page+1)+', \''+key+'\', \''+value+'\');">더 보기</button>');
		}
	});
}

$(document).ready(function() {
	$('.filter.button').each(function(){
		if ($.cookie($(this).attr('id')) == null) {
			if (!$('#'+$(this).attr('id')).hasClass('blue')) {
				$.cookie($(this).attr('id'), 0);
			}
			else {
				$.cookie($(this).attr('id'), 1);
			}
		}
		else {
			if ($.cookie($(this).attr('id')) == 0) {
				$('#'+$(this).attr('id')).addClass('blue');
			}
			else {
				$('#'+$(this).attr('id')).removeClass('blue');
			}
		}
	})
});