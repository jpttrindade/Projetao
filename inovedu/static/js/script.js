$(document).ready(function(){
	$("#id_turma").attr('disabled', 'disabled');
	$('#id_colegio').change(function(){
		$("#list_turma").load('/turma/'+$('#id_colegio option:selected').text()+'/ #id_turma');	
	});
});



/*$(document).ready(function(){
	$('#ranking').click(function(){
			$('aside').css({"margin-right":"400px"});
			$('aside').before('<article><iframe src="/ranking/"></iframe></article>');
		
	});
});*/
/*$(document).ready(function(){
	$('#id_colegio').change(function(){
		$('form').submit()
		var x = $(this).find(":selected").text();
		$(this).after("<p>"+x+" </p>");
	});
});
*/
/*
		$.ajax({
            url: "/",
            dataType: "json",
            success: function(response) {
            
            }
        });
*/


/*
<tr>
	<th> <label for="id_turma">Turma: </label> </th>
	<td> <select id="id_turma" name="turma">
			<option value="" selected="selected">Selecione</option>
			<option value="1">Projetao</option>
		</select></td>
</tr>*/
