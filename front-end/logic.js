$(document).ready(function(){
    var map = new AMap.Map('container',{
        zoom: 10,
        center: [116.39,39.9]  
    });
    map.setFeatures(['bg','road','point']);
    AMap.plugin(['AMap.ToolBar','AMap.Scale','AMap.OverView'],
        function(){
            map.addControl(new AMap.ToolBar());

            map.addControl(new AMap.Scale());

            map.addControl(new AMap.OverView({isOpen:true}));
        });
    var add_point = function(x, y, title) {

        var marker = new AMap.Marker({
            position: [x, y],
            title: title,
            clickable: true,
            animation: "AMAP_ANIMATION_DROP",
        });
        marker.setMap(map);
    }

    add_point(116.480983, 39.989628, "这里是详细信息！\n支持换行");

    $("button.add").click(function(event) {
        var x = parseFloat($("input[name='x']").val());
        var y = parseFloat($("input[name='y']").val());
        var title = $("textarea.info").val();
        console.log(x, y, title);
        add_point(x, y, title);
    });

    $(".add-btn").click(function(event) {
        $(".inputs").fadeToggle();
        $(".add-btn img").toggleClass('rotate');
    });

})