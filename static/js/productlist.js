(function($) {

    $('.wrapper .more').click(function(show) {	
		var showMe = $(this).closest('.product').find('.container-prod');	
		$(this).closest('.wrapper').find('.container-prod').not(showMe).removeClass('information');
		$('.container-prod').removeClass('social-sharing');
        showMe.stop(false, true).toggleClass('information').removeClass('social-sharing');
        show.preventDefault();
    });
	
	$('.wrapper .share').click(function(share) {	
		var showMe = $(this).closest('.product').find('.container-prod');	
		$(this).closest('.wrapper').find('.container-prod').not(showMe).removeClass('social-sharing');
		$('.container-prod').removeClass('information');
        showMe.stop(false, true).toggleClass('social-sharing').removeClass('information');
        share.preventDefault();
    });
	
	$('.wrapper .add').click(function(share) {	
		var showMe = $(this).closest('.product').find('.cart');	
        showMe.stop(false, true).addClass('added');
		var showMe = $(this).closest('.product').find('.container-prod');	
		showMe.stop(false, true).removeClass('social-sharing').removeClass('information');
        share.preventDefault();
    });

})(jQuery);