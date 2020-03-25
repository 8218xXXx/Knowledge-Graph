/*
 * @Author: admin
 * @Date:   2017-07-03 15:55:41
 * @Last Modified by:   mingming
 * @Last Modified time: 2017-07-06 18:44:29
 */

'use strict';
$(function() {
	$(window).scroll(function() {
		x9Nav();
		indexS11();
		indexHigh();
		indexS3();
		indexS5();
		indexS8();
	}).trigger('scroll');
	var flag = 0;

	function x9Nav() {
		if ($(window).scrollTop() && flag == 0) {
			$($('.vivioNav')[0]).animate({
				top: -80
			}, 500, 'swing');
			$($('.topBar')[0]).animate({
				"margin-top": 0
			}, 500, 'swing');
			flag = 1;
		} else if ($(window).scrollTop() === 0 && flag == 1) {
			$($('.vivioNav')[0]).animate({
				top: 0
			}, 500);
			$($('.topBar')[0]).animate({
				"margin-top": 80
			}, 500);
			flag = 0;
		}
	};

	function indexHigh() {
		var sc = $(window).scrollTop();
		var rheight = $(window).height();
		if (sc < rheight) {
			$(".start.index-high").addClass('showX9');
		} else if (sc > rheight && sc > ($('.start.index-high').height() + $('.start.index-high .title').height() + $('.start.index-high .figure').height())) {
			$(".start.index-high").removeClass('showX9');

		}

	};

	function indexS11() {
		var sc = $(window).scrollTop();
		var rheight = $(window).height();
		var num = sc - rheight;
		num = num * 0.04;
		if (num > 28.4) {
			num = 28.4;
		}
		$(".start.index-s11 .figure em").css("transform", "translateY(-" + num + "px)");
	};

	function indexS3() {
		var sc = $(window).scrollTop();
		if (sc > 2600 && sc < 4700) {
			$($('.index-s3 .figure._animation em')[0]).css('transform', 'scale(1)');
			$($('.index-s3 .figure._animation em')[1]).css('transform', 'scale(1)');
			$($('.index-s3 .figure._animation em')[3]).css('opacity', '1');
			$($('.index-s3 .figure._animation em')[4]).css('opacity', '1');
		} else {
			$($('.index-s3 .figure._animation em')[0]).css('transform', 'scale(0)');
			$($('.index-s3 .figure._animation em')[1]).css('transform', 'scale(0)');
			$($('.index-s3 .figure._animation em')[3]).css('opacity', '0');
			$($('.index-s3 .figure._animation em')[4]).css('opacity', '0');
		}

	};

	function indexS5() {
		var sc = $(window).scrollTop();
		if (sc > 5014 && sc < 5414) {
			$('.index-s5 ._animation').css('right', '-70px').css('bottom', '104px');
		} else if (sc > 6514 || sc < 3714) {
			$('.index-s5 ._animation').css('right', '-353px').css('bottom', '27px');
		}
	};

	function indexS8() {
		var sc = $(window).scrollTop();
		if (sc > 6894) {
			var num = sc - 6894;
			num = num *0.04;
			$(".index-s8 .figure.left em").css("transform", "translateY(-" + num + "px)");
		}
	};
});