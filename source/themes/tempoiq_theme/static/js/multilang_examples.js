;
(function ($) {
    "use strict";
    $.tempoiq = $.tempoiq || {};
    $.tempoiq.docs = $.tempoiq.docs || {};
    $.tempoiq.utils = $.tempoiq.utils || {};

    /**
     * Assigns own enumerable properties of source object(s) to the destination
     * object for all destination properties that resolve to `undefined`. Once a
     * property is set, additional defaults of the same property will be ignored.
     *
     * @static
     * @memberOf _
     * @type Function
     * @category Objects
     * @param {Object} object The destination object.
     * @param {...Object} [source] The source objects.
     * @param- {Object} [guard] Allows working with `_.reduce` without using its
     *  `key` and `object` arguments as sources.
     * @returns {Object} Returns the destination object.
     * @example
     *
     * var object = { 'name': 'barney' };
     * _.defaults(object, { 'name': 'fred', 'employer': 'slate' });
     * // => { 'name': 'barney', 'employer': 'slate' }
     */
    var defaults = $.tempoiq.utils.defaults = function (object) {
        if (!object) {
            return object;
        }
        for (var argsIndex = 1, argsLength = arguments.length; argsIndex < argsLength; argsIndex++) {
            var iterable = arguments[argsIndex];
            if (iterable) {
                for (var key in iterable) {
                    if (typeof object[key] == 'undefined') {
                        object[key] = iterable[key];
                    }
                }
            }
        }
        return object;
    };


    var MultiLanguageExampleManager = $.tempoiq.docs.MultiLanguageExampleManager = function (el, options) {
        var base = this;

        function initialize() {
            base.options = defaults(options || {}, base.defaultOptions);
            base.$snippet_list = $(".snippets-container");
            //For each container, create a MultiLanguageSnippet
            base.snippet_list = base.$snippet_list.map(function (idx, el) {
                return new MultiLanguageSnippet(el, base.options);
            }, this);

            for (var i = 0; i < base.snippet_list.length; i++) {
                $(base.snippet_list[i]).on("languageChanged", onSnippetLanguageChanged);
            }
        }

        function onSnippetLanguageChanged(event, lang) {
            for (var i = 0; i < base.snippet_list.length; i++) {
                base.snippet_list[i].setLanguage(lang);
            }
        }

        initialize();
        return base;
    };

    MultiLanguageExampleManager.prototype.defaultOptions = {
        defaultLanguage: "javascript"
    };


    /**
     * Takes a snippets element and returns a constructed and event wired up multiclient example
     * @type {Function}
     */
    var MultiLanguageSnippet = $.tempoiq.docs.MultiLanguageSnippet = function (el, options) {
        var base = this;

        function initialize() {
            base.options = defaults(options || {}, base.defaultOptions);
            if (el.jquery) {
                base.$el = el;
                base.el = el[0];
            } else {
                base.el = el;
                base.$el = $(el);
            }
            base._snippetLanguages = {};
            initializeHeadings();
            initializeSnippets();
        }

        function initializeHeadings() {
            base.$headings = base.$el.find(".heading");
            base.$headings.each(function (idx, heading) {
                var $heading = $(heading);
                $heading.on('click', base.onLanguageChanged);
                base._snippetLanguages[$heading.data("language")] = idx;
            });

            if (base.options.defaultLanguage && base._snippetLanguages[base.options.defaultLanguage] !== undefined) {
                var header_to_activate = base.$headings[base._snippetLanguages[base.options.defaultLanguage]];
                $(header_to_activate).addClass("active-heading");
            } else {
                $(base.$headings[0]).addClass("active-heading");
            }
        }

        function initializeSnippets() {
            base.$snippets = base.$el.find(".snippet");
            base.snippets = base.$snippets.map(function (idx, s) {
                return new LanguageSnippet(s);
            });
            if (base.options.defaultLanguage && base._snippetLanguages[base.options.defaultLanguage] !== undefined) {
                base.snippets.each(function (idx, s) {
                    if (s.language == base.options.defaultLanguage) s.show();
                    else s.hide();
                });
            } else {
                base.snippets.each(function (idx, s) {
                    if (idx == 0) s.show();
                    else s.hide();
                });
            }
        }

        base.onLanguageChanged = function (event) {
            if (event) event.preventDefault();
            var ofsetFromTop = 80,
                $body = $('body'),
                scrollTop     = $body.scrollTop(),
                elementOffset = base.$el.offset().top - ofsetFromTop,
                distance = elementOffset - scrollTop;

            $(base).trigger("languageChanged", $(this).data("language"));
            var newScrollTop = $('body').scrollTop(),
                topPos = base.$el.offset().top;
            $body.scrollTop(topPos - distance - ofsetFromTop);
        };

        base.setLanguage = function (lang) {
            //Set active header
            base.$headings.each(function (idx, heading) {
                var $heading = $(heading);
                if ($heading.data("language") == lang) {
                    $heading.addClass("active-heading")
                } else {
                    $heading.removeClass("active-heading")
                }
            });
            var active_idx = base._snippetLanguages[lang];
            if (active_idx !== undefined) {
                for (var i = 0; i < base.snippets.length; i++) {
                    if (i == active_idx) {
                        base.snippets[i].show();
                    } else {
                        base.snippets[i].hide();
                    }
                }
            }
        };

        initialize();
        return base;
    };

    MultiLanguageSnippet.prototype.defaultOptions = {};

    var LanguageSnippet = $.tempoiq.docs.LanguageSnippet = function (el) {
        var base = this;

        function initialize() {
            //base.options = defaults(options || {}, base.defaultOptions);
            if (el.jquery) {
                base.$el = el;
                base.el = el[0];
            } else {
                base.el = el;
                base.$el = $(el);
            }
            base.language = base.$el.data("language");
        }

        base.show = function () {
            base.$el.removeClass("hidden-snippet");
            base.$el.addClass("active-snippet");
        };
        base.hide = function () {
            base.$el.addClass("hidden-snippet");
            base.$el.removeClass("active-snippet");
        };

        initialize();
        return base;
    };

    LanguageSnippet.prototype.defaultOptions = {};
})(jQuery);