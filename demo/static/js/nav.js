/*
 * @Author: mingming
 * @Date:   2017-06-29 18:44:28
 * @Last Modified by:   admin
 * @Last Modified time: 2017-07-07 15:52:36
 */

'use strict';
$(function() {
	function navBar() {
		// 1.导航条鼠标经过li,为active添加notcurrent类   鼠标离开 为active删除notcurrent类 
		$('#vivio-navbar-collapse .vivio-navbar-nav li').mouseover(function(event) {
			if ($('#vivio-navbar-collapse .vivio-navbar-nav .active').attr('id') === "vivio-product-link") {
				if ($(this).attr('id') !== "vivio-product-link") {
					$('#vivio-navbar-collapse .vivio-navbar-nav .active').addClass('notCurrent');
				}
			} else {
				$('#vivio-navbar-collapse .vivio-navbar-nav .active').addClass('notCurrent');
			}

		});
		$('#vivio-navbar-collapse .vivio-navbar-nav').mouseout(function(event) {

			$('#vivio-navbar-collapse .vivio-navbar-nav .active.notCurrent').removeClass('notCurrent');

		});

		//2.导航关闭按钮切换 （小屏幕）
		$('.navbar-toggle .vivio-icon-bt').click(function() {	
					flagNav=1;
			if ($('.navbar-toggle .vivio-icon-close').css('opacity') == 1) {
				$('.navbar-toggle .vivio-icon-bar').css('opacity', '1');
				$('.navbar-toggle .vivio-icon-bar').css('transform', 'scale(1,1)');
				$('#vivio-navbar-collapse').css('transition-delay', '.7s').height(0);
				$('body').css('overflow-y', 'scroll');
				$('.navbar-toggle .vivio-icon-close').css('opacity', '0');
				$('.navbar-toggle .vivio-icon-close').css('transform', 'scale(0,0)');
				$('#vivio-navbar-collapse .vivio-navbar-nav li> a').css('opacity', '0').css('transform', 'translateX(-50px)');


			} else {
				$('.navbar-toggle .vivio-icon-bar').css('opacity', '0');
				$('.navbar-toggle .vivio-icon-bar').css('transform', 'scale(0,0)');
				$('#vivio-navbar-collapse .vivio-navbar-nav li> a').css('opacity', '1').css('transform', 'translateX(50px)');
				$('#vivio-navbar-collapse').css('transition-delay', '0s').height($(window).height());
				$('body').css('overflow-y', 'hidden');
				$('.navbar-toggle .vivio-icon-close').css('opacity', '1');
				$('.navbar-toggle .vivio-icon-close').css('transform', 'scale(1,1)');
			}

		});
	var flagNav=0;
		$(window).resize(function(event) {
			if ($(window).width() > 768&&flagNav===1) {
				$('#vivio-navbar-collapse .vivio-navbar-nav li> a').css('opacity', '1').css('transform', 'translateX(50px)');
			} else if(flagNav===1){
				$('#vivio-navbar-collapse').css('transition-delay', '.7s').height(0);
				$('#vivio-navbar-collapse .vivio-navbar-nav li> a').css('opacity', '0').css('transform', 'translateX(-50px)');

			}
		});

	};
	navBar();
});