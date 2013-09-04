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

$(document).ready(function(){
	/*select = $("#id_turma").hide();*/
	var escolha_turma = null;
	
	$('#id_colegio').change(function(){
		nome_colegio = $('#id_colegio').find(":selected").text();
		if(nome_colegio != "Selecione"){
				escolha_turma = $("#list_turma");
				$("#list_turma").load('/turma/'+nome_colegio+'/ #id_turma', function(data){
/*				select.value(data.option);*/
				/*$("#id_turma").css();*/				
				$('#list_turma').empty();
				$('#list_turma').after("<br> Turma "+data);				
			});
			
		} else {
			$('#list_turma').empty();
		}

	});

	

});

$(document).on("submit", "form" ,function(e){
		$.post("/cadastrar_aluno/", { turma:  $('form').serialize() } );
});

/*
<tr>
	<th> <label for="id_turma">Turma: </label> </th>
	<td> <select id="id_turma" name="turma">
			<option value="" selected="selected">Selecione</option>
			<option value="1">Projetao</option>
		</select></td>
</tr>*/
