// JavaScript Document
$(function () {
    var myChart = echarts.init(document.getElementById('main'), 'dark');
    myChart.showLoading();
    $.get('/static/data/entity_attribution.json', function (webkitDep) {
        myChart.hideLoading();
        webkitDep.nodes.forEach(function (node) {
            node.value = node.value;
            node.category = node.category;
        });
        mytextStyle = {
            color: '#fff',                           //文字颜色
            fontStyle: "normal",                     //italic斜体  oblique倾斜
            fontWeight: "bolder",                    //文字粗细bold   bolder   lighter  100 | 200 | 300 | 400...
            fontFamily: "Helvetica",                //字体系列
            fontSize: 18,                              //字体大小
        };
        option = {
            legend: {
                data:webkitDep.categories.map(function (a) {//  map() 方法返回一个由原数组中的每个元素调用一个指定方法后的返回值组成的新数组。
                    return a.name;
                }),
                 x: '10%',
                 y: '30%',
                orient: 'vertical',
                textStyle: {
                    color: '#fff'          // 图例文字颜色
                },
                size: 10,
            },
            title: {
                text: '中文分词技术可视化',
                // subtext: '数据来源于Adgovato',
                // sublink: "http://127.0.0.1:9999/evaluation_2",
                textStyle: mytextStyle,
                z: 2,
                top: '14%',
                left: '68%',
                color: 'white',
                borderColor: "#000",
                borderWidth: 0,
                shadowColor: "red",
            },
            tooltip: {
                show:true,
                // formatter: "{c}",
                formatter: function (params) {
                    console.log(params)
                    if (params.dataType == "edge"){
                        return params.data['value'];
                    }
                }
            },
            animationDuration: 5000,
            animationEasingUpdate: 'quinticInOut',
            series: [{
                type: 'graph',
                layout: 'force',
                animation: true,
                label: {
                    normal: {
                        show: true,
                        position: 'right',
                        formatter: '{b}'
                    }
                },
                roam: true,
                focusNodeAdjacency: true,
                focusNodeAdjacency: true,
                edgeSymbol:['none', 'arrow'],
                draggable: true,
                data: webkitDep.nodes.map(function (node, idx) {
                    node.id = idx;
                    console.log(idx)
                    return node;
                }),
                categories: webkitDep.categories,
                lineStyle: {
                        normal: {
                            show: 'true',
                            color: 'target',
                            curveness: 0.1,
                            width: 1.5,
                        }
                    },
                force: {
                    // initLayout: 'circular',
                    // repulsion: 20,
                    edgeLength: 5,
                    repulsion: 20,
                    gravity: 0.3
                },
                edges: webkitDep.links
            }]
        };
        myChart.setOption(option);
    });
})