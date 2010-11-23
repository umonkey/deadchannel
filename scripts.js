$(document).ready(function(){
	$('a.external').attr('target', '_blank');
	$('a[href*="://"]:not([href^="http://beta.deadchannel.ru/"])').attr('target', '_blank');
});
