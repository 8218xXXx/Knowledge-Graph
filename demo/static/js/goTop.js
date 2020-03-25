/*
 * @Author: mingming
 * @Date:   2017-07-02 14:14:56
 * @Last Modified by:   admin
 * @Last Modified time: 2017-07-03 15:48:48
 */

'use strict';
$(function() {
	var flag = 0;
	function gotoTop() {
		$(window).scroll(function() {
			var sc = $(window).scrollTop();
			var rheight = $(window).height()
			if (sc > rheight * 0.6 && flag === 0) {
				$($(".top")[0]).animate({
					bottom: 30
				}, 500);
				flag = 1;
			} else if (sc < rheight * 0.6 && flag === 1) {
				$($(".top")[0]).animate({
					bottom: -50
				}, 500);
				flag = 0;
			}
		});
		$($(".top")[0]).click(function() {
			var sc = $(window).scrollTop();
			$('body,html').animate({
				scrollTop: 0
			}, 300);
			return false;
		});
	}
	gotoTop();
});