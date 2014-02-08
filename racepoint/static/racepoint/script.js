/* =================================== */
/*  App: django-racepoint              */
/* =================================== */

// the god object
var RP = {
	
	// constructor
	init: function() {
		if($('#racepoint_point').length > 0) RP.point.init();
		csrf_token = $.cookie('csrftoken');
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				xhr.setRequestHeader('X-CSRFToken', csrf_token);
			}
		});
	},
	
	// at the point
	point: {
		dom: false,
		init: function() {
			RP.point.dom = $('#racepoint_point');
			RP.point.arrivals.init();
			RP.point.departures.init();
		},
		arrivals: {
			form: false,
			input_team: false,
			modal: false,
			init: function() {
				RP.point.arrivals.form = RP.point.dom.find('form');
				RP.point.arrivals.input_team = RP.point.arrivals.form.find('#input_team');
				RP.point.arrivals.modal = $('#racepoint_select_players');
				RP.point.arrivals.form.submit(function(e) {
					e.preventDefault();
					$.post(
						'ajax/',
						{
							task: 'get_players',
							team: RP.point.arrivals.input_team.val()
						},
						function(data) {
							RP.point.arrivals.modal.find('.modal-body').html(data);
							RP.point.arrivals.modal.find('button.btn-primary').click(function() {
								RP.point.arrivals.add();
							});
							RP.point.arrivals.modal.modal();
						},
						'html'
					);
				});
			},
			add: function() {
				players = RP.point.arrivals.modal.find(':checked').map(function() {
					return this.value;
				}).get();
				$.post(
					'ajax/',
					{
						task: 'add_arrival',
						team: RP.point.arrivals.input_team.val(),
						players: players
					},
					function(data) {
						if(data) {
							RP.point.arrivals.modal.modal('hide');
						} else {
							alert('Error!');
						}
					},
					'json'
				);
			}
		},
		departures: {
			init: function() {
				
			}
		}
	}
	
}

// brrmm, brrrrm!
$(document).ready(RP.init);
