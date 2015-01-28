$( document ).ready(function() {
    // Shift nav in mobile when clicking the menu.
    $(document).on('click', "[data-toggle='wy-nav-top']", function() {
      $("[data-toggle='wy-nav-shift']").toggleClass("shift");
      $("[data-toggle='rst-versions']").toggleClass("shift");
    });
    // Close menu when you click a link.
    $(document).on('click', ".wy-menu-vertical .current ul li a", function() {
      $("[data-toggle='wy-nav-shift']").removeClass("shift");
      $("[data-toggle='rst-versions']").toggleClass("shift");
    });
    $(document).on('click', "[data-toggle='rst-current-version']", function() {
      $("[data-toggle='rst-versions']").toggleClass("shift-up");
    });

    $(document).on('click', "a[href^='#']", SphinxRtdTheme.scrollToAnchor);
    SphinxRtdTheme.scrollToAnchor(window.location.hash);
});

window.SphinxRtdTheme = (function (jquery) {
    var stickyNav = (function () {
        var navBar,
            win,
            stickyNavCssClass = 'stickynav',
            applyStickNav = function () {
                if (navBar.height() <= win.height()) {
                    navBar.addClass(stickyNavCssClass);
                } else {
                    navBar.removeClass(stickyNavCssClass);
                }
            },
            enable = function () {
                applyStickNav();
                win.on('resize', applyStickNav);
            },
            init = function () {
                navBar = jquery('nav.wy-nav-side:first');
                win    = jquery(window);
            };
        jquery(init);
        return {
            enable : enable
        };
    }());

    var scrollToAnchor = function(href){
        href = typeof(href) == "string" ? href : jquery(this).attr("href");
        if(!href) return;
        var fromTop = 80;
        var target = jquery(href);

        if(target.length) {
            var topPos = target.offset().top; 
            setTimeout(function() {
                jquery('html, body').scrollTop(topPos - fromTop);
            }, 2); // Tiny timeout to fire after browser's anchor scroll
            if(history && "pushState" in history) {
                history.pushState({}, document.title, window.location.pathname + href);
                return false;
            }
        }
    }

    return {
        StickyNav: stickyNav,
        scrollToAnchor: scrollToAnchor
    };
}($));
