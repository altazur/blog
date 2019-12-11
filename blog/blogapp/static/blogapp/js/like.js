$(document).ready(function(){
	$('.like').click(function(){
		var element_id;
		element_id = $(this).attr("data-id");
		$.get('/likepost/', {post_id: element_id}, function(data){
			$('#likes'+element_id).html(data);
			$('#like'+element_id).hide();
		});
	});
});
