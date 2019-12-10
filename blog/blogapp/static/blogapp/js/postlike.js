$('#like').click(function(){
	var post_id;
	got_post_id = $(this).attr("data-postid");
	$.get('/likepost/', {post_id: got_post_id}, function(data){
		$('#likes').html(data);
		$('#like').hide();
	});
});
