
$(document).ready(function() {
    /* LazyLoad images */
    function lazyLoadImages() {
        $('.lazy-load').each(function() {
            if ($(this).offset().top < window.innerHeight + window.scrollY + 500) {
                $(this).attr('src', $(this).attr('data-src'));
                $(this).removeClass('lazy-load');
            }
        });
    }

    // Initial load
    lazyLoadImages();

    // On scroll
    $(window).scroll(function() {
        lazyLoadImages();
    });

    // Handle older browsers that may not support dataset
    $('img').each(function(){
        if ($(this).attr('data-src') && !$(this).hasClass('lazy-load')) {
            $(this).attr('src', $(this).attr('data-src'));
        }
    });

    $('.show-more a').click(function(){
        $('.past-races .col-md-12').css('max-height', '100%');
        $('.past-races .col-md-12').css('overflow', 'visible');
        $('.show-more').css('display', 'none');
    });

    /* Mobile menu toggle */
    $('#mobile-menu-button').click(function(){
        $('#mobile-menu').toggleClass('hidden');
    });

    /* Close mobile menu when clicking outside */
    $(document).click(function(event) {
        if (!$(event.target).closest('#mobile-menu').length &&
            !$(event.target).closest('#mobile-menu-button').length) {
            $('#mobile-menu').addClass('hidden');
        }
    });

    /* Improve table responsiveness on mobile */
    $('table').each(function() {
        if (!$(this).parent().hasClass('overflow-x-auto')) {
            $(this).wrap('<div class="overflow-x-auto"></div>');
        }
    });

    /* Custom tab functionality for race results */
    window.showTab = function(tabId, tabGroupPrefix) {
        // Hide all tabs in this group
        $(`[id^="${tabGroupPrefix}-"][id$="-results"]`).addClass('hidden');

        // Show the selected tab
        $(`#${tabId}`).removeClass('hidden');

        // Update active tab styling
        $(`#${tabGroupPrefix}-tabs a`).removeClass('bg-red-100');
        $(`#${tabGroupPrefix}-tabs a[href="#${tabId}"]`).addClass('bg-red-100');

        // Prevent default anchor behavior
        return false;
    };

    // Initialize first tab for each race type
    $('[id$="-tabs"]').each(function() {
        const tabGroup = $(this).attr('id').replace('-tabs', '');
        $(`#${tabGroup}-overall-results`).removeClass('hidden');
        $(`#${tabGroup}-tabs a:first`).addClass('bg-red-100');
    });

    /* Homepage Carousel */
    if ($('#carousel-homepage').length) {
        let currentSlide = 0;
        const slides = $('.carousel-slide');
        const indicators = $('.carousel-indicator');
        const totalSlides = slides.length;

        function showSlide(index) {
            slides.removeClass('opacity-100').addClass('opacity-0');
            indicators.removeClass('bg-white').addClass('bg-white/50');

            slides.eq(index).removeClass('opacity-0').addClass('opacity-100');
            indicators.eq(index).removeClass('bg-white/50').addClass('bg-white');
            currentSlide = index;
        }

        function nextSlide() {
            showSlide((currentSlide + 1) % totalSlides);
        }

        function prevSlide() {
            showSlide((currentSlide - 1 + totalSlides) % totalSlides);
        }

        // Navigation buttons
        $('.carousel-next').click(nextSlide);
        $('.carousel-prev').click(prevSlide);

        // Indicator buttons
        indicators.each(function(index) {
            $(this).click(function() {
                showSlide(index);
            });
        });

        // Auto-advance carousel every 5 seconds
        let autoAdvance = setInterval(nextSlide, 5000);

        // Pause auto-advance on hover
        $('#carousel-homepage').hover(
            function() { clearInterval(autoAdvance); },
            function() { autoAdvance = setInterval(nextSlide, 5000); }
        );

        // Keyboard navigation
        $(document).keydown(function(e) {
            if ($('#carousel-homepage:hover').length > 0) {
                if (e.keyCode === 37) prevSlide(); // Left arrow
                if (e.keyCode === 39) nextSlide(); // Right arrow
            }
        });
    }
});
