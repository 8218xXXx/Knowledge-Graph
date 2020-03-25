/*
 * @Author: mingming
 * @Date:   2017-06-15 21:47:31
 * @Last Modified by:   admin
 * @Last Modified time: 2017-07-06 15:17:49
 */

'use strict';

$(function() {
	var carouselItem = $('#carousel-vivio-generic .carousel-inner .item');
	function carousel() {
		//3.设置轮播图
		$(window).resize(function(event) {
			$('#carousel-vivio-generic').height($(window).height());
			$('#carousel-vivio-generic').width($(window).width());
			$('main').css('margin-top', $(window).height()).css('margin-bottom', $('footer').height());
			$('#carousel-vivio-generic .item').height($(window).height());

		}).trigger("resize");

		$(window).scroll(function() {
			var sc = $(window).scrollTop();
			var rheight = $(window).height();
			if (sc > rheight) {
				$('footer').css("display", "block");
				$('#carousel-vivio-generic').css("display", "none");
			} else {
				$('footer').css("display", "none");
				$('#carousel-vivio-generic').css("display", "block");
			}
			// 遮罩效果
			var carouselBlurNum = sc * 0.02;
			$('#carousel-vivio-generic>.carousel-inner>.item').css("filter", "blur(" + carouselBlurNum + "px)")
				.css("-webkit-filter", "blur(" + carouselBlurNum + "px)")
				.css("-moz-filter", "blur(" + carouselBlurNum + "px)")
				.css("-ms-filter", "blur(" + carouselBlurNum + "px)")
				.css("filter", "progid:DXImageTransform.Microsoft.Blur(PixelRadius=" + carouselBlurNum + ", MakeShadow=false)");
			footer();

		}).trigger("scroll");


		setInterval(function time() {
			// 轮播图
			$(carouselItem).each(function(index, item) {
				if ($(item).hasClass('active')) {
					$(item).addClass('showTitle');
				} else {
					$(item).removeClass('showTitle');
				}
			});
		}, 0);
	};

	function footer() {
		var rheight = $(window).height();
		var footerlBlurNum = (getScrollHeight() - $(window).scrollTop() - rheight) * 0.02;
		$('footer').css("filter", "blur(" + footerlBlurNum + "px)")
			.css("-webkit-filter", "blur(" + footerlBlurNum + "px)")
			.css("-moz-filter", "blur(" + footerlBlurNum + "px)")
			.css("-ms-filter", "blur(" + footerlBlurNum + "px)")
			.css("filter", "progid:DXImageTransform.Microsoft.Blur(PixelRadius=" + footerlBlurNum + ", MakeShadow=false)");
		// 取文档内容实际高度 
		function getScrollHeight() {
			return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
		}
	}


	carousel();

});