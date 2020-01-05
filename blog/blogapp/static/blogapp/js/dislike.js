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
				// Change button colors due to state
				// .css didn't work for me
				like_element = $('#dislike'+element_id)
				if (like_element.attr("style") == "background-color: #c1affb" || like_element.attr("style") == "background-color: rgb(193, 175, 251);")  // Add or operator because django template generated RGB from hashcolor somehow
				{
					like_element.prop("style", "");
				}
				else
				{
					like_element.prop("style", "background-color: #c1affb;");
				}
		});
		}
		else if (element_type == 'comment'){
			$.get('/dislikecomment/', {comment_id: element_id}, function(data){
				$('#dislikes'+element_id).html(data);
				// Change button colors due to state
				// .css didn't work for me
				like_element = $('#dislike'+element_id)
				if (like_element.attr("style") == "background-color: #c1affb" || like_element.attr("style") == "background-color: rgb(193, 175, 251);")
				{
					like_element.prop("style", ""); 
				}
				else
				{
					like_element.prop("style", "background-color: #c1affb;");
				}
		});

		}
	});
});
