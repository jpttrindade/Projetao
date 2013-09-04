/*$(document).ready(function(){
	$('#ranking').click(function(){
			$('aside').css({"margin-right":"400px"});
			$('aside').before('<article><iframe src="/ranking/"></iframe></article>');
		
	});
});*/
$(document).ready(function(){
	$('#id_colegio').change(function(){
		/*$('form').submit()*/
		var x = $(this).find(":selected").text();
		$(this).after("<p>"+x+" </p>");
	});
});

