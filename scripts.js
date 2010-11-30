$(document).ready(function(){
	$('a.external').attr('target', '_blank');
	$('a[href*="://"]:not([href^="http://beta.deadchannel.ru/"])').attr('target', '_blank');

	$('#submitlink').click(function(){
		$('#submit').show('slow');
	});

	$('#submitlink textarea').focus(function(){
		$(this).html('lala.');
	});
});
