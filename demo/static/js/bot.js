
var text = $("#f-left");
text.focus();
function action() 
{
	if(text.val()==null||text.val()=="")
	{
		text.focus();
		return;
	}

	$(".b-body").append("<div class='mWord'><span></span><p>" + text.val() + "</p></div>");
	$(".b-body").scrollTop(10000000);
	var args= {
			type : "get",
			// url:"https://api.ownthink.com/bot",
			// url: "http://www.tuling123.com/openapi/api",
			url: "/littlechongchong",
			data: {"info":text.val()},
			// data : {"token" : "openbot", "info" : text.val()},
			// data: {"info":text.val(), "key":"f5403425efce4f658a6e25343525d1da", "userid":"demo"},
			success : function(redata)
			{
				console.log(redata);
				console.log(text.val());
				// var result = $.parseJSON(redata).data.info.text;
				// result = $.parseJSON(redata).text;
				result = redata
				$(".b-body").append("<div class='rotWord'><span></span> <p id='member'>" + result + "</p></div>");
				$(".b-body").scrollTop(10000000);
			}
		}
	
	ajax(args);
	text.val("");
	text.focus();
	
};

$("#btn").click(function()
{
	action();
});
$(document).keydown(function(event)
{
	if(event.keyCode==13)
	{
		action();
	}
});

function ajax(mJson)
{
	var type=mJson.type||'get';
	var url=mJson.url;
	var data=mJson.data;
	var success=mJson.success;
	var error=mJson.error;
	var dataStr='';
	
	if(data)
	{
		var arr = Object.keys(data);
		var len = arr.length;
		var i = 0;
		
		for (var key in data)
		{
			dataStr+=key+'='+data[key];
	
			if (++i<len)
			{
				dataStr+='&';
			}
		}
		
		if(type.toLowerCase()=='get')
		{
			url+='?'+dataStr;
		}
	}
	
	console.log(url);
	
	var xhr=new XMLHttpRequest();
	xhr.open(type,url,true);
	xhr.setRequestHeader('content-type' , 'application/x-www-form-urlencoded');
	xhr.send(null);

	xhr.onreadystatechange=function()
	{
		if(xhr.readyState==4)
		{
			if(xhr.status>=200&&xhr.status<300)
			{
				success&&success(xhr.responseText);
			}
			else
			{
				error&&error(xhr.status);
			}
		}
	}
}		
