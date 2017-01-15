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
    // 导出函数
    return {
    }
})();