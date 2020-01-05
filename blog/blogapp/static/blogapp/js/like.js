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
				// Change button colors due to state
				// .css didn't work for me
				like_element = $('#like'+element_id)
				if (like_element.attr("style") == "background-color: #c1affb;")
				{
					like_element.attr("style") == "";
				}
				else
				{
					$('#like'+element_id).prop("background-color", "#claffb");
				}
		});

		}
		else if (element_type == 'comment'){
			$.get('/likecomment/', {comment_id: element_id}, function(data){
				$('#likes'+element_id).html(data);
				// Change button colors due to state
				// .css didn't work for me
				like_element = $('#like'+element_id)
				if (like_element.attr("style") == "background-color: #c1affb;")
				{
					like_element.attr("style") == "";
				}
				else
				{
					$('#like'+element_id).prop("background-color", "#claffb");
				}
		});

		}
	});
});
