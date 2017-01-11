/*! UIkit 3.0.0-beta.1 | http://www.getuikit.com | (c) 2014 - 2016 YOOtheme | MIT License */

(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(require('uikit')) :
    typeof define === 'function' && define.amd ? define(['uikit'], factory) :
    (factory(global.UIkit));
}(this, (function (uikit) { 'use strict';

var $ = uikit.util.$;
var ajax = uikit.util.ajax;
var on = uikit.util.on;
UIkit.component('upload', {

    props: {
        allow: String,
        clsDragover: String,
        concurrent: Number,
        dataType: String,
        mime: String,
        msgInvalidMime: String,
        msgInvalidName: String,
        multiple: Boolean,
        name: String,
        params: Object,
        type: String,
        url: String
    },

    defaults: {
        allow: false,
        clsDragover: 'uk-dragover',
        concurrent: 1,
        dataType: undefined,
        mime: false,
        msgInvalidMime: 'Invalid File Type: %s',
        msgInvalidName: 'Invalid File Name: %s',
        multiple: false,
        name: 'files[]',
        params: {},
        type: 'POST',
        url: '',
        abort: null,
        beforeAll: null,
        beforeSend: null,
        complete: null,
        completeAll: null,
        error: null,
        fail: function fail(msg) {
            alert(msg);
        },

        load: null,
        loadEnd: null,
        loadStart: null,
        progress: null
    },

    events: {
        change: function change(e) {

            if (!$(e.target).is('input[type="file"]')) {
                return;
            }

            e.preventDefault();

            if (e.target.files) {
                this.upload(e.target.files);
            }

            e.target.value = '';
        },
        drop: function drop(e) {
            e.preventDefault();
            e.stopPropagation();

            var transfer = e.originalEvent.dataTransfer;

            if (!transfer || !transfer.files) {
                return;
            }

            this.$el.removeClass(this.clsDragover);

            this.upload(transfer.files);
        },
        dragenter: function dragenter(e) {
            e.preventDefault();
            e.stopPropagation();
        },
        dragover: function dragover(e) {
            e.preventDefault();
            e.stopPropagation();
            this.$el.addClass(this.clsDragover);
        },
        dragleave: function dragleave(e) {
            e.preventDefault();
            e.stopPropagation();
            this.$el.removeClass(this.clsDragover);
        }
    },

    methods: {
        upload: function upload(files) {
            var _this = this;

            if (!files.length) {
                return;
            }

            this.$el.trigger('upload', [files]);

            for (var i = 0; i < files.length; i++) {

                if (this.allow) {
                    if (!match(this.allow, files[i].name)) {
                        this.fail(this.msgInvalidName.replace(/%s/, this.allow));
                        return;
                    }
                }

                if (this.mime) {
                    if (!match(this.mime, files[i].type)) {
                        this.fail(this.msgInvalidMime.replace(/%s/, this.mime));
                        return;
                    }
                }
            }

            if (!this.multiple) {
                files = [files[0]];
            }

            this.beforeAll && this.beforeAll(this, files);

            var chunks = chunk(files, this.concurrent),
                upload = function upload(files) {

                var data = new FormData();

                files.forEach(function (file) {
                    return data.append(_this.name, file);
                });

                for (var key in _this.params) {
                    data.append(key, _this.params[key]);
                }

                ajax({
                    data: data,
                    url: _this.url,
                    type: _this.type,
                    dataType: _this.dataType,
                    beforeSend: _this.beforeSend,
                    complete: [_this.complete, function (xhr, status) {
                        if (chunks.length) {
                            upload(chunks.shift());
                        } else {
                            _this.completeAll && _this.completeAll(xhr);
                        }

                        if (status === 'abort') {
                            _this.abort && _this.abort(xhr);
                        }
                    }],
                    cache: false,
                    contentType: false,
                    processData: false,
                    xhr: function xhr() {
                        var xhr = $.ajaxSettings.xhr();
                        xhr.upload && _this.progress && on(xhr.upload, 'progress', _this.progress);
                        ['loadStart', 'load', 'loadEnd', 'error', 'abort'].forEach(function (type) {
                            return _this[type] && on(xhr, type.toLowerCase(), _this[type]);
                        });
                        return xhr;
                    }
                });
            };

            upload(chunks.shift());
        }
    }

});

function match(pattern, path) {
    return path.match(new RegExp('^' + pattern.replace(/\//g, '\\/').replace(/\*\*/g, '(\\/[^\\/]+)*').replace(/\*/g, '[^\\/]+').replace(/((?!\\))\?/g, '$1.') + '$', 'i'));
}

function chunk(files, size) {
    var chunks = [];
    for (var i = 0; i < files.length; i += size) {
        var chunk = [];
        for (var j = 0; j < size; j++) {
            chunk.push(files[i + j]);
        }
        chunks.push(chunk);
    }
    return chunks;
}

})));