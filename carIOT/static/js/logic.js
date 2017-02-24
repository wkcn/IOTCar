$(document).ready(function(){
    /*页面加载完成猴开始*/
    // 新建一个地图，中心点为中华人民共和国
    var map = new AMap.Map('container',{
        zoom: 1,
        center: [106.471586, 36.408494]
    });
    // 设置地图显示背景，道路，点
    map.setFeatures(['bg','road','point']);
    // 为地图添加工具条，缩放条，小地图
    AMap.plugin(['AMap.ToolBar','AMap.Scale','AMap.OverView'],
        function(){
            map.addControl(new AMap.ToolBar());
            map.addControl(new AMap.Scale());
            map.addControl(new AMap.OverView({isOpen:true}));
        }
    );

    // 每个坐标点点击之后会弹框，内容为坐标点的 标题 和 速度
    var _onClick = function(e){
        console.log(e.target);
        // 调用swal库显示弹窗
        swal({
            html: e.target.G.title.replace(/\n/g, "<br />") + "速度: " + parseInt(e.target.ji.extData["speed"]) + "km/s"
        });
    }
    // 所有坐标点的集合
    var markers = [];
    // 增加坐标点，参数为经度纬度和标题内容
    var add_point = function(x, y, title) {
        // 生成一个坐标点对象
        var marker = new AMap.Marker({
            // 坐标点位置
            position: [x, y],
            // 坐标点标题内容
            title: title,
            // 坐标点可以点击
            clickable: true,
            // 坐标点的出场效果
            animation: "AMAP_ANIMATION_DROP",
            // 坐标点被鼠标指了会跑到最上面来
            topWhenMouseOver: true,
            // 写错了
            // title: title,
            // 坐标点的额外信息
            extData: {"speed": 0.1}
        });
        // 绑定坐标点到地图对象上
        marker.setMap(map);
        // 储存坐标点到列表里面，待会才找得回来
        markers.push(marker);
        // 绑定坐标点的点击事件到上面那个函数上，就是可以弹窗显示坐标点的信息
        AMap.event.addListener(marker, 'click', _onClick);
    }
    // 给坐标点一个随机的目标地点和速度，让它自己移动起来，看起来就像是真的东西一样，
    // 但是这个东西有一个小问题就是它的方向是完全随机的，所以坐标点会在地图上不断地乱逛，
    // 而不是像真的车一样往一个固定地目的地走
    // 有解决办法但我不想写
    var setMoveTo = function() {
        // 循环遍历刚才那个储存坐标点的数组
        $(markers).each(function(n, el) {
            // 获取到坐标点现在的位置
            var pos = el.getPosition();
            // 给它来一个随机的位移
            var ll = pos.offset(Math.random()*200-100, Math.random()*50-25);
            // 给坐标点来一个随机的速度
            var speed = Math.random()*150 + 40;
            // 把这个速度写到坐标点的属性里面，待会显示弹窗的时候才有的玩
            el.setExtData({"speed": speed});
            // 让这个坐标点动起来
            el.moveTo(ll, speed);
        });
    }

    $("button.add").click(function(event) {
        // 从输入框里提取经度
        var x = parseFloat($("input[name='x']").val());
        // 从输入框里提取纬度
        var y = parseFloat($("input[name='y']").val());
        // 从输入框里提取标题内容
        var title = $("textarea.info").val();
        // 把这三个东西都打印出来，用于调试
        console.log(x, y, title);
        // 新增一个坐标点
        add_point(x, y, title);
    });

    // 点击了圆圆的绿色加号按钮会发生的事情
    $(".add-btn").click(function(event) {
        // 改变输入框的可见性
        $(".inputs").fadeToggle();
        // 改变加号的旋转角度。加号旋转45度角看起来就是一个叉啦
        $(".add-btn img").toggleClass('rotate');
    });

    // 从服务器里读取车辆信息
    function loadCars() {
        // 发送异步请求
        $.ajax({
            // 请求的地址和路径
            url: 'http://45.32.48.44:5000/get_latest_location',
            // 请求的方式
            type: 'GET',
            // 请求的数据类型
            dataType: 'json',
            // 完成后的操作
            success: function(data) {
                // 把获取到的东西打印出来
                console.log(data);
                // 循环遍历车辆数组
                for (var prop in data) {
                    // 先声明一个储存标题内容的变量
                    var info = "",
                    // 获取纬度
                    x = data[prop]["Longitude"],
                    // 获取经度
                    y = data[prop]["Latitude"];
                    // 加入一堆信息
                    info += "#汽车ID: " + data[prop]["CarId"] + '\n';
                    info += "车主姓名: " + data[prop]["DriverName"] + '\n';
                    info += "联系方式: " + data[prop]["DriverTel"] + '\n';
                    info += "汽油容量: " + data[prop]["oil_capacity"] + '\n';
                    info += "经度: " + data[prop]["Longitude"] + '\n';
                    info += "纬度: " + data[prop]["Latitude"] + '\n';
                    info += "温度: " + data[prop]["temperature"] + "℃" + '\n';

                    // info += "记录时间: " + prop;
                    // 在地图上新增一个车辆坐标点
                    add_point(x, y, info);
                }
                // 随机给个目的地
                setMoveTo();
            }
        });
    }

    // 启动获取车辆信息的函数
    loadCars();

    // 声明一个红红圈的M
    var content= "<div class='mobile'>M</div>";
    // 实例化那个红圈
    var mobile = new AMap.Marker({
        // 红圈显示为红圈而不是蓝色的圆锥
        content: content,
        // 红圈的初始位置
        position: [113.388644,23.06786],
        // 红圈的初始内容
        title: "No Data",
        // 红圈也会被指了跑上来
        topWhenMouseOver: true,
        // 红圈可以点击
        clickable: true,
    });
    // 绑定红圈到地图上
    mobile.setMap(map);

    // 红圈被点击的操作函数
    var _onMobileClick = function(e){
        // console.log(e.target);
        // 弹窗显示红圈里的内容信息
        swal({
            html: e.target.ji.title.replace(/\n/g, "<br />")
        });
    }

    // 绑定红圈的点击事件到上面那个函数上
    AMap.event.addListener(mobile, 'click', _onMobileClick);

    // 设置红圈的位置等信息
    function setMobile() {
        // 向服务器请求信息
        $.ajax({
            // 请求的地址和路径
            url: 'http://45.32.48.44:5000/get_latest_GPS?n=1',
            // 请求方式
            type: 'GET',
            // 内容格式
            dataType: 'json',
            // 成功后操作
            success: function(data) {
                // console.log(data);
                // 遍历返回的所有属性
                for(var p in data) {
                    // 获取经度
                    var x = data[p]["longitude"],
                    // 获取纬度
                    y = data[p]["latitude"];
                    // 设置红圈位置
                    mobile.setPosition(new AMap.LngLat(x, y));
                    // 返回
                    return;
                }
            }
        });

        // 又是异步请起内容信息
        $.ajax({
            // 请求的地址和路径
            url: 'http://45.32.48.44:5000/get_latest_sensors?n=1',
            // 请求方式
            type: 'GET',
            // 请求返回的格式
            dataType: 'json',
            // 请求成功的操作
            success: function(data) {
                // 遍历返回的属性
                for(var p in data) {
                    // 声明临时储存变量
                    var info = "";
                    // 遍历所有属性
                    for(var pp in data[p]) {
                        // 属性和值链接起来放到变量里
                        info += pp + ": " + data[p][pp] + '\n';
                    }
                    // 变量内容放到红圈的属性里
                    mobile.setTitle(info);
                    // 返回
                    return;
                }
            }
        });
    }

    // 设置无限循环，3秒一次
    setInterval(function() {
        // 给所有点一个随机目标和速度
        setMoveTo();
        // 获取红圈最新的位置和属性
        setMobile();
    }, 3000)

})