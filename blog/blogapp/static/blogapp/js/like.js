$(document).ready(function(){
	$('.like').click(function(){
		var element_id;
		var element_type;
		element_type = $(this).parents('.post').length ? 'post' : 'comment';
		element_id = $(this).attr("data-id");
		//I don't proud if this if else statement
		if (element_type == 'post'){
			$.get('/likepost/', {post_id: element_id}, function(data){
				$('#likes'+element_id).html(data);
				$('#like'+element_id).prop("disabled", true);
		});
		}
		else if (element_type == 'comment'){
			$.get('/likecomment/', {comment_id: element_id}, function(data){
				$('#likes'+element_id).html(data);
				$('#like'+element_id).prop("disabled", true);
		});

		}
	});
});
