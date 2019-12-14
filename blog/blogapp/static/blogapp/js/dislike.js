$(document).ready(function(){
	$('.dislike').click(function(){
		var element_id;
		var element_type;
		element_type = $(this).parents('.post').length ? 'post' : 'comment';
		element_id = $(this).attr("data-id");
		//I don't proud of this if else statement :)
		if (element_type == 'post'){
			$.get('/dislikepost/', {post_id: element_id}, function(data){
				$('#dislikes'+element_id).html(data);
				$('#dislike'+element_id).prop("disabled", true);
		});
		}
		else if (element_type == 'comment'){
			$.get('/dislikecomment/', {comment_id: element_id}, function(data){
				$('#dislikes'+element_id).html(data);
				$('#dislike'+element_id).prop("disabled", true);
		});

		}
	});
});
