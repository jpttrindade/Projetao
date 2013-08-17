$(document).ready(function() {
		//actions menu
		$('.subMenu').hide(); // hide all sub-menus
		$("#menuPrincipalProfessor li" ).hover(function() {
			$(this).find('.subMenu').stop(true,true).fadeIn();
		}, function() {
			$(this).find('.subMenu').stop(true,true).fadeOut();
		});
});
