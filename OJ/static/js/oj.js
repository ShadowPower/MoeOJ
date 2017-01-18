var oj = (function () {
    $(document).pjax('a[target!=_blank]', '#content', {fragment:'#content', timeout:8000});
    $(document).on('pjax:send', function() {
        //pjax链接点击后显示加载动画；
        console.log('开始载入');
    });
    $(document).on('pjax:complete', function() {
        //pjax链接加载完成后隐藏加载动画；
        console.log('载入完成');
    });

    // 分页
    $('#change-pagination').on('click', function (e) {
        e.preventDefault();
        $(this).blur();
        UIkit.modal.prompt('请输入页码 (7/20):', '').then(function(page) {
            console.log('跳转到:', page)
        });
    });

    // 导出函数
    return {
    }
})();