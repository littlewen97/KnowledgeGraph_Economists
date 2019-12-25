var text = $("#f-left");
$("#btn").click(function(){
	action();
});

$(document).keydown(function(event)
{
	if(event.keyCode==13)
	{
		action();
	}
});

function action(){
	if(text.val()==null||text.val()=="")
	{
		alert("消息不能为空");
		text.focus();
		return;
	}

	$(".b-body").append("<div class='mWord'><span></span><p>" + text.val() + "</p></div>");
	$(".b-body").scrollTop(10000000);
	$.get('/pullQuestion/',{'text':text.val()},function(data){
		$(".b-body").append("<div class='rotWord'><span></span><p>" + data + "</p></div>");
		$(".b-body").scrollTop(10000000);
	});
	text.val("");
	text.focus();
};

