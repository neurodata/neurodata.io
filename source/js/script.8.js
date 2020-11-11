$(document).ready(function () {

  if (false) {
	//load homepage gif only on mobile
	$(window).on("load resize scroll", function (e) {
		if (($(window).width() < 1025) && ($(".main .video .mobile").length > 0)) {
			//do nothing, image exists already
		} else if ($(window).width() < 1025) {
			$(".main .video").prepend('<video autoplay muted preload loop playsinline class="mobile"><source src="static/video/NeurodataIntroVideo_mobile.mp4" type="video/mp4" /></video>')
		}
	});
	//safari bug resolved with this duplicated
	if (($(window).width() < 1025) && ($(".main .video .mobile").length > 0)) {
		//do nothing, image exists already
	} else if ($(window).width() < 1025) {
		$(".main .video").prepend('<video autoplay muted preload loop playsinline class="mobile"><source src="static/video/NeurodataIntroVideo_mobile.mp4" type="video/mp4" /></video>')
	}
  }

	//init tool tip
	$('.tooltip').tooltipster();

	//display learn more text
	$("a.button.expand").on("click", function (e) {
		$(".header p").toggleClass("active");
		e.preventDefault();
	});

	//display why neurodata text
	$("a.button.expand").on("click", function (e) {
		$(".copy p").toggleClass("active");
		e.preventDefault();
	});

	//display projects on mobile
	$("a.expand_projects").on("click", function (e) {
		let x = $('#' + $(this).attr('data'))
		if (x.css('display') === "none") {
			x.show();
		} else {
			x.hide();
		}
		e.preventDefault();
	});

	//toggle mobile menu links
	$('#mobile-nav').on("click", function () {
		$(this).toggleClass('open');
		$(".mobile-links").toggleClass('open');
		$(".mobile-links ul").toggleClass('open');
		$(".main").toggleClass('blur');
	});
	$('.mobile-links a').on("click", function () {
		if ($(this).attr('class') !== "expand_projects") {
			$('#mobile-nav').toggleClass('open');
			$(".mobile-links").toggleClass('open');
			$(".mobile-links ul").toggleClass('open');
			$(".main").toggleClass('blur');
		}
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
		} else {
			if ($(".table.database input[type='checkbox']:not(:checked)").length > 0) {
				$(".table.database input[type='checkbox'][value='All']").prop('checked', false);
			}
		}
		paintCheckboxes();
		renderCalendar();
	});

	//smooth scroll anchor links
	$(function () {
		var navHeight = $(".doc-nav").height();
		var mainNavHeight = $(".wrapper>.nav").height();
		$('a[href*="#"]:not([href="#"])').on("click", function () {
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
		$('select[name=links]').on("change", function () {
				var target = $($(this).val());
				target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
				if (target.length) {
					$('html, body').animate({
						scrollTop: target.offset().top - navHeight - mainNavHeight - 30
					}, 1000);
					return false;
				}
		});
	});
	$(function () {
		$('.doc-nav select').on("change", function () {
			try {
				if ($("#" + $(this).val()).size()) {
					$('html,body').animate({
						scrollTop: $("#" + $(this).val()).offset().top - 100
					}, 'slow');
				}
			} catch {}
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

	$(window).on('load', function () {
		equalheight('.col.even');
	});
	$(window).on("resize", function () {
		equalheight('.col.even');
	});

	var coll = document.getElementsByClassName("collapsible");
	var i;
	for (i = 0; i < coll.length; i++) {
		coll[i].addEventListener("click", function () {
			this.classList.toggle("active");
			var content = this.nextElementSibling;
			if (content.style.maxHeight) {
				content.style.maxHeight = null;
			} else {
				content.style.maxHeight = content.scrollHeight + "px";
			}
		});
	}

});
