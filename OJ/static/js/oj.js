var oj = (function () {
    window.onload = function () {
        $('#change-pagination').on('click', function (e) {
            e.preventDefault();
            $(this).blur();
            UIkit.modal.prompt('请输入页码 (7/20):', '').then(function(page) {
                console.log('跳转到:', page)
            });
        });
    }

    // 导出函数
    return {
    }
})();