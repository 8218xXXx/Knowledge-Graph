/*
 * @Author: mingming
 * @Date:   2017-07-01 18:43:30
 * @Last Modified by:   mingming
 * @Last Modified time: 2017-07-02 15:23:24
 */

'use strict';
$(function() {
	$('main').css('margin-bottom', $('footer').height());


	// 下拉菜单功能实现(1.点击打开、关闭)
	$(".vivio-store form strong>span>span:nth-child(2)").click(function(e) {
		$(this).parent().find('.menu').toggleClass('open');
	});
	// (2.点击省份加载对应城市)
	$('#province>a').click(function() {
		$(this).parent().toggleClass('open').find('.active').removeClass('active');
		$(this).addClass('active');
		var userProvince = $(this).html();
		$('#userProvince').html(userProvince);
		userCity(userProvince);
		return false;
	});

	// (3.获取用户省份的城市列表)
	function userCity(province) {
		var allCity = $('#userCity').find("a");
		for (var i = 0; i < allCity.length; i++) {
			if ($(allCity[i]).data('parent') === province) {
				$(allCity[i]).css('display', 'block');
			} else {
				$(allCity[i]).css('display', 'none');
			}
		}
	}

	// (4.用户选择城市)
	$('#userCity>a').click(function() {
		$(this).parent().toggleClass('open').find('.active').removeClass('active');
		$(this).addClass('active');
		var userCity = $(this).html();
		$('#vivio-user-city').html(userCity);
		$('#userProvince').html($(this).data('parent'));
		return false;
	});


});