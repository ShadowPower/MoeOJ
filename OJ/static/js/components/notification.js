/*! UIkit 3.0.0-beta.1 | http://www.getuikit.com | (c) 2014 - 2016 YOOtheme | MIT License */

(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('uikit')) :
    typeof define === 'function' && define.amd ? define(['uikit'], factory) :
    (factory(global.UIkit));
}(this, (function (uikit) { 'use strict';

var $ = uikit.util.$;
var Transition = uikit.util.Transition;
var containers = {};

UIkit.component('notification', {

    defaults: {
        message: '',
        status: '',
        timeout: 5000,
        group: null,
        pos: 'top-center',
        onClose: null
    },

    created: function created() {

        if (!containers[this.pos]) {
            containers[this.pos] = $('<div class="uk-notification uk-notification-' + this.pos + '"></div>').appendTo(uikit.container);
        }

        this.$mount($('<div class="uk-notification-message' + (this.status ? ' uk-notification-message-' + this.status : '') + '">\n                <a href="#" class="uk-notification-close" uk-close></a>\n                <div>' + this.message + '</div>\n            </div>').appendTo(containers[this.pos].show()));
    },
    ready: function ready() {
        var _this = this;

        var marginBottom = parseInt(this.$el.css('margin-bottom'), 10);

        Transition.start(this.$el.css({ opacity: 0, marginTop: -1 * this.$el.outerHeight(), marginBottom: 0 }), { opacity: 1, marginTop: 0, marginBottom: marginBottom }).then(function () {
            if (_this.timeout) {
                _this.timer = setTimeout(_this.close, _this.timeout);
                _this.$el.on('mouseenter', function () {
                    return clearTimeout(_this.timer);
                }).on('mouseleave', function () {
                    return _this.timer = setTimeout(_this.close, _this.timeout);
                });
            }
        });
    },


    events: {
        click: function click(e) {
            e.preventDefault();
            this.close();
        }
    },

    methods: {
        close: function close(immediate) {
            var _this2 = this;

            var remove = function remove() {

                _this2.onClose && _this2.onClose();
                _this2.$el.trigger('close', [_this2]).remove();

                if (!containers[_this2.pos].children().length) {
                    containers[_this2.pos].hide();
                }
            };

            if (this.timer) {
                clearTimeout(this.timer);
            }

            if (immediate) {
                remove();
            } else {
                Transition.start(this.$el, { opacity: 0, marginTop: -1 * this.$el.outerHeight(), marginBottom: 0 }).then(remove);
            }
        }
    }

});

UIkit.notification.closeAll = function (group, immediate) {

    var notification;
    UIkit.elements.forEach(function (el) {
        if ((notification = UIkit.getComponent(el, 'notification')) && (!group || group === notification.group)) {
            notification.close(immediate);
        }
    });
};

})));