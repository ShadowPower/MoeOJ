var oj = (function () {
    // 根据时间更改背景配色
    function changeBackgroundByTime () {
        var background = document.getElementById('background');
        if (background == null)
            return;

        var currentTime = new Date();
        var hours = currentTime.getHours();
        if (hours >= 19 || hours < 7)
            background.setAttribute('class', 'background night');
        else if (hours >= 7 && hours < 17)
            background.setAttribute('class', 'background day');
        else
            background.setAttribute('class', 'background dusk');
    }

    // 导出函数
    return {
    }
})();