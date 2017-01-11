/*! UIkit 3.0.0-beta.1 | http://www.getuikit.com | (c) 2014 - 2016 YOOtheme | MIT License */

(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('uikit')) :
    typeof define === 'function' && define.amd ? define(['uikit'], factory) :
    (factory(global.UIkit));
}(this, (function (uikit) { 'use strict';

var $ = uikit.util.$;
var flipPosition = uikit.util.flipPosition;
UIkit.component('tooltip', {

    mixins: [uikit.mixin.toggable, uikit.mixin.position],

    props: {
        delay: Number
    },

    defaults: {
        pos: 'top',
        delay: 0,
        animation: 'uk-animation-scale-up',
        duration: 100,
        cls: 'uk-active',
        clsPos: 'uk-tooltip'
    },

    ready: function ready() {
        this.content = this.$el.attr('title');
        this.$el.removeAttr('title').attr('aria-expanded', false);
    },


    methods: {
        show: function show() {
            var _this = this;

            clearTimeout(this.showTimer);

            if (this.$el.attr('aria-expanded') === 'true') {
                return;
            }

            this.tooltip = $('<div class="' + this.clsPos + '" aria-hidden="true"><div class="' + this.clsPos + '-inner">' + this.content + '</div></div>').appendTo(uikit.container);

            this.$el.attr('aria-expanded', true);

            this.positionAt(this.tooltip, this.$el);
            this.origin = this.getAxis() === 'y' ? flipPosition(this.dir) + '-' + this.align : this.align + '-' + flipPosition(this.dir);

            this.showTimer = setTimeout(function () {
                _this.toggleElement(_this.tooltip, true);

                _this.hideTimer = setInterval(function () {
                    if (!_this.$el.is(':visible')) {
                        _this.hide();
                    }
                }, 150);
            }, this.delay);
        },
        hide: function hide() {

            if (this.$el.is('input') && this.$el[0] === document.activeElement) {
                return;
            }

            clearTimeout(this.showTimer);
            clearInterval(this.hideTimer);
            this.$el.attr('aria-expanded', false);
            this.toggleElement(this.tooltip, false);
            this.tooltip.remove();
            this.tooltip = false;
        }
    },

    events: {
        'focus mouseenter': 'show',
        'blur mouseleave': 'hide'
    }

});

})));