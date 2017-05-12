$( document ).ready(function() {
	// Handler for .ready() called.

	//establecemos las variables del formulario abierto
	var form_conductor_open = true;
	var form_empresa_open = false;
	var datos_auto_open = false;

	$('#datos_empresa').hide();
	$('#auto').hide();

  	//asignamos el cambio de formulario a los botones superiores .btn-persona
	$('#btn_datos_conductor').click( function(event) {
	  	event.preventDefault();
	  	if (form_conductor_open == false) {
	  		$(this).addClass("active");
	  		$('#btn_datos_empresa').removeClass("active");

	  		$('#datos_empresa').slideUp(450, function() {
	  			$('#datos_conductor').slideDown(450);
	  			form_empresa_open = false;
	  			form_conductor_open = true;
	  		});
	  	}
	});

   $('#btn_datos_empresa').click( function(event) {
	   	event.preventDefault();
	   	if (form_empresa_open == false) {
	   		$(this).addClass("active");
	  		$('#btn_datos_conductor').removeClass("active");
	  		
	   		$('#datos_conductor').slideUp(450, function() {
	  			$('#datos_empresa').slideDown(450);
	  			form_empresa_open = true;
	  			form_conductor_open = false;
	  		});
	  	}
	});

   $('#toogle-datos').click( function(event) {
	   	event.preventDefault();
	   	$( "#auto" ).slideToggle( "slow", function() {
	   		if ( datos_auto_open == false) {
	   			datos_auto_open = true;
	   			$('#toogle-datos').text("Ocultar datos Contratación");
	   		} else {
	   			datos_auto_open = false;
	   			$('#toogle-datos').text("Mostrar datos Contratación");
	   		}
		});
	});
});