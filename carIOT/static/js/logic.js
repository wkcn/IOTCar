$(document).ready(function(){
    var map = new AMap.Map('container',{
        zoom: 1,
        center: [106.471586, 36.408494]
    });
    map.setFeatures(['bg','road','point']);
    AMap.plugin(['AMap.ToolBar','AMap.Scale','AMap.OverView'],
        function(){
            map.addControl(new AMap.ToolBar());

            map.addControl(new AMap.Scale());

            map.addControl(new AMap.OverView({isOpen:true}));
        });


    var _onClick = function(e){
        console.log(e.target.G.anything);
        swal({
            html: e.target.G.anything.replace(/\n/g, "<br />")
        });
    }
    var add_point = function(x, y, title) {
        var marker = new AMap.Marker({
            position: [x, y],
            title: title,
            clickable: true,
            animation: "AMAP_ANIMATION_DROP",
            topWhenMouseOver: true,
            anything: title,
        });
        marker.setMap(map);
        AMap.event.addListener(marker, 'click', _onClick);
    }

    // add_point(116.480983, 39.989628, "这里是详细信息！\n支持换行");
    // add_point(118.480983, 40.234, "这里是第二条信息");

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

    function loadCars(n) {
        $.ajax({
            url: 'http://45.32.48.44:5000/get_n_location',
            type: 'GET',
            dataType: 'json',
            data: {n: n},
            success: function(data) {
                console.log(data);
                for (var prop in data) {
                    var info = "",
                    x = data[prop]["Longitude"],
                    y = data[prop]["Latitude"];

                    info += "#汽车ID: " + data[prop]["CarId"] + '\n';
                    info += "汽油容量: " + data[prop]["oil_capacity"] + '\n';
                    info += "温度: " + data[prop]["temperature"] + "℃" + '\n';
                    info += "经度: " + data[prop]["Longitude"] + '\n';
                    info += "纬度: " + data[prop]["Latitude"] + '\n';

                    info += "记录时间: " + prop;

                    add_point(x, y, info);
                }
            }
        })
        .done(function() {
            console.log("success");
        })
        .fail(function() {
            console.log("error");
        })
        .always(function() {
            console.log("complete");
        });
    }

    loadCars(50);

})