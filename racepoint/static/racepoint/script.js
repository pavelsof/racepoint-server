/* =================================== */
/*  App: django-racepoint              */
/* =================================== */

// the god object
var RP = {
	
	AJAX_URL: 'ajax/',
	
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
			RP.point.here.init();
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
						RP.AJAX_URL,
						{
							task: 'get_players',
							team: RP.point.arrivals.input_team.val()
						},
						function(data) {
							RP.point.arrivals.modal.find('.modal-body').html(data);
							RP.point.arrivals.modal.modal();
						},
						'html'
					);
				});
				RP.point.arrivals.modal.find('button.btn-primary').click(function(e) {
					e.preventDefault();
					RP.point.arrivals.add();
				});
			},
			add: function() {
				players = RP.point.arrivals.modal.find(':checked').map(function() {
					return this.value;
				}).get();
				$.post(
					RP.AJAX_URL,
					{
						task: 'add_arrival',
						team: RP.point.arrivals.input_team.val(),
						players: players
					},
					function(data) {
						if(data) {
							RP.point.here.reload();
							RP.point.arrivals.modal.modal('hide');
						} else {
							alert('Error!');
						}
					},
					'json'
				);
			}
		},
		here: {
			dom: false,
			init: function() {
				RP.point.here.dom = RP.point.dom.find('tbody.teams_here');
				RP.point.here.attach_listeners();
			},
			reload: function() {
				$.post(
					RP.AJAX_URL,
					{
						task: 'get_teams_here'
					},
					function(data) {
						RP.point.here.dom.html(data);
						RP.point.here.attach_listeners();
					},
					'html'
				);
			},
			attach_listeners: function() {
				RP.point.here.dom.find('a').click(function(e) {
					e.preventDefault();
					team_id = $(this).data('team');
					if(team_id) RP.point.departures.add(team_id);
				});
			}
		},
		departures: {
			dom: false,
			init: function() {
				RP.point.departures.dom = RP.point.dom.find('tbody.teams_left');
			},
			add: function(team_id) {
				$.post(
					RP.AJAX_URL,
					{
						task: 'add_departure',
						team: team_id
					},
					function(data) {
						if(data) {
							RP.point.here.reload();
							RP.point.departures.reload();
						}
					},
					'json'
				);
			},
			reload: function() {
				$.post(
					RP.AJAX_URL,
					{
						task: 'get_teams_left'
					},
					function(data) {
						RP.point.departures.dom.html(data);
					},
					'html'
				);
			}
		}
	}
	
}

// brrmm, brrrrm!
$(document).ready(RP.init);
