$(document).ready(function () {

	//load homepage gif only on mobile
	$(window).bind("load resize scroll", function (e) {
		if (($(window).width() < 1025) && ($(".main .video .mobile").length > 0)) {
			//do nothing, image exists already
		}
		else if ($(window).width() < 1025) {
			$(".main .video").prepend('<video autoplay muted preload loop class="mobile"><source src="static/video/NeurodataIntroVideo_mobile.mp4" type="video/mp4" /></video>')
		}
	});
	//safari bug resolved with this duplicated
	if (($(window).width() < 1025) && ($(".main .video .mobile").length > 0)) {
		//do nothing, image exists already
	}
	else if ($(window).width() < 1025) {
		$(".main .video").prepend('<video autoplay muted preload loop class="mobile"><source src="static/video/NeurodataIntroVideo_mobile.mp4" type="video/mp4" /></video>')
	}

	//init tool tip
	$('.tooltip').tooltipster();

	//center dynamic tooltips
	$(".tool-wrap .options .link span h5").each(function () {
		var width = $(this).width();
		var halfWidth = width / 2;
		$(this).css("left", - halfWidth);
	});

	//display learn more text
	$("a.button.expand").click(function () {
		$(".header p").toggleClass("active");
	});

	//toggle mobile menu links
	$('#mobile-nav').click(function () {
		$(this).toggleClass('open');
		$(".mobile-links").toggleClass('open');
		$(".mobile-links ul").toggleClass('open');
		$(".main").toggleClass('blur');
	});
	$('.mobile-links a').click(function () {
		$('#mobile-nav').toggleClass('open');
		$(".mobile-links").toggleClass('open');
		$(".mobile-links ul").toggleClass('open');
		$(".main").toggleClass('blur');
	});

	//black homepage background
	if ($("#video").length > 0) {
		$("body").addClass("dark");
	}

	//custom checkboxes
	function paintCheckboxes() {
		$(".table.database input[type='checkbox']").each(function () {
			$(this).siblings("span").removeClass("checked")
			if ($(this).is(":checked")) {
				$(this).siblings("span").addClass("checked");
			}
		});
	}
	paintCheckboxes();

	$(".table.database input[type='checkbox']").on("click", function () {
		if ($(this).val() == "All") {
			$(".table.database input[type='checkbox']").prop('checked', true);
		}
		else {
			if ($(".table.database input[type='checkbox']:not(:checked)").length > 0) {
				$(".table.database input[type='checkbox'][value='All']").prop('checked', false);
			}
		}
		paintCheckboxes();
		renderCalendar();
	});

	//fixed nav on scroll
	$(window).bind("load resize scroll", function (e) {
		//desktop
		if (($(".doc-nav").length > 0) && ($(window).width() > 1024)) {
			//get header height
			var headerHeight = $('.header').height();
			//make nav fixed
			if ($(window).scrollTop() > headerHeight) {
				$('.doc-nav').addClass('fixed');
				$('.doc-nav').width($(this).width() - 230);
				var docNavHeight = $('.doc-nav').height();
				$('.docs').css('margin-top', docNavHeight);
				$('.detail-wrap').css('margin-top', docNavHeight);
				$('.about').css('margin-top', docNavHeight);
			}
			//make nav static
			if ($(window).scrollTop() < headerHeight) {
				$('.doc-nav').removeClass('fixed');
				$('.docs').css('margin-top', '0px');
				$('.detail-wrap').css('margin-top', '0px');
				$('.about').css('margin-top', '0px');
				$('.doc-nav').width("100%");
			}
		}
		//mobile, remove all
		else {
			$('.doc-nav').removeClass('fixed');
			$('.docs').css('margin-top', '0px');
			$('.detail-wrap').css('margin-top', '0px');
			$('.about').css('margin-top', '0px');
			$('.doc-nav').width("100%");
		}
	});

	//smooth scroll anchor links
	$(function () {
		var navHeight = $(".doc-nav").height();
		$('a[href*="#"]:not([href="#"])').click(function () {
			if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
				var target = $(this.hash);
				target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
				if (target.length) {
					$('html, body').animate({
						scrollTop: target.offset().top - navHeight - 10
					}, 1000);
					return false;
				}
			}
		});
	});
	$(function () {
		$('.doc-nav select').change(function () {
			$('html,body').animate({ scrollTop: $("#" + $(this).val()).offset().top - 100 }, 'slow');
		});
	});

	//set columns to same height
	equalheight = function (container) {

		var currentTallest = 0,
			currentRowStart = 0,
			rowDivs = new Array(),
			$el,
			topPosition = 0;

		$(container).each(function () {

			$el = $(this);
			$($el).height('auto')
			topPostion = $el.position().top;

			if (currentRowStart != topPostion) {
				for (currentDiv = 0; currentDiv < rowDivs.length; currentDiv++) {
					rowDivs[currentDiv].height(currentTallest);
				}
				rowDivs.length = 0; // empty the array
				currentRowStart = topPostion;
				currentTallest = $el.height();
				rowDivs.push($el);
			} else {
				rowDivs.push($el);
				currentTallest = (currentTallest < $el.height()) ? ($el.height()) : (currentTallest);
			}
			for (currentDiv = 0; currentDiv < rowDivs.length; currentDiv++) {
				rowDivs[currentDiv].height(currentTallest);
			}

		});
	}

	$(window).load(function () {
		equalheight('.col.even');
	});
	$(window).resize(function () {
		equalheight('.col.even');
	});

});