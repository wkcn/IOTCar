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
        }
    );


    var _onClick = function(e){
        console.log(e.target);
        swal({
            html: e.target.G.title.replace(/\n/g, "<br />") + "速度: " + parseInt(e.target.ji.extData["speed"]) + "km/s"
        });
    }
    var markers = [];
    var add_point = function(x, y, title) {
        var marker = new AMap.Marker({
            position: [x, y],
            title: title,
            clickable: true,
            animation: "AMAP_ANIMATION_DROP",
            topWhenMouseOver: true,
            title: title,
            extData: {"speed": 0.1}
        });
        marker.setMap(map);
        // var ll = new AMap.LngLat(106.471586, 36.408494);
        // marker.moveTo(ll, 1000);

        markers.push(marker);

        AMap.event.addListener(marker, 'click', _onClick);
    }

    var setMoveTo = function() {
        $(markers).each(function(n, el) {
            var pos = el.getPosition();
            var ll = pos.offset(Math.random()*200-100, Math.random()*50-25);
            var speed = Math.random()*150 + 40;
            el.setExtData({"speed": speed});
            el.moveTo(ll, speed);
        });
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

    function loadCars() {
        $.ajax({
            url: 'http://45.32.48.44:5000/get_latest_location',
            type: 'GET',
            dataType: 'json',
            // data: {n: n},
            success: function(data) {
                console.log(data);
                for (var prop in data) {
                    var info = "",
                    x = data[prop]["Longitude"],
                    y = data[prop]["Latitude"];

                    info += "#汽车ID: " + data[prop]["CarId"] + '\n';
                    info += "车主姓名: " + data[prop]["DriverName"] + '\n';
                    info += "联系方式: " + data[prop]["DriverTel"] + '\n';
                    info += "汽油容量: " + data[prop]["oil_capacity"] + '\n';
                    info += "经度: " + data[prop]["Longitude"] + '\n';
                    info += "纬度: " + data[prop]["Latitude"] + '\n';
                    info += "温度: " + data[prop]["temperature"] + "℃" + '\n';

                    // info += "记录时间: " + prop;

                    add_point(x, y, info);
                    setMoveTo();
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

    loadCars();

    var content= "<div class='mobile'>M</div>";
    var mobile = new AMap.Marker({
        content: content,
        position: [113.388644,23.06786],
        title: "No Data",
        topWhenMouseOver: true,
        // offset: new AMap.Pixel(-10,0),
        clickable: true,
    });
    mobile.setMap(map);

    var _onMobileClick = function(e){
        // console.log(e.target);
        swal({
            html: e.target.ji.title.replace(/\n/g, "<br />")
        });
    }

    AMap.event.addListener(mobile, 'click', _onMobileClick);


    function setMobile() {
        $.ajax({
            url: 'http://45.32.48.44:5000/get_latest_GPS?n=1',
            type: 'GET',
            dataType: 'json',
            // data: {n: n},
            success: function(data) {
                // console.log(data);
                for(var p in data) {
                    var x = data[p]["longitude"],
                    y = data[p]["latitude"];
                    mobile.setPosition(new AMap.LngLat(x, y));
                    return;
                }
            }
        });

        $.ajax({
            url: 'http://45.32.48.44:5000/get_latest_sensors?n=1',
            type: 'GET',
            dataType: 'json',
            // data: {n: n},
            success: function(data) {
                // console.log(data);
                for(var p in data) {
                    var info = "";
                    for(var pp in data[p]) {
                        info += pp + ": " + data[p][pp] + '\n';
                    }
                    mobile.setTitle(info);
                    return;
                }
            }
        });
    }

    
    setInterval(function() {
        // console.log("set move to");
        setMoveTo();
        setMobile();
    }, 3000)

})