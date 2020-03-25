// JavaScript Document
$(function () {
    var myChart = echarts.init(document.getElementById('main'), 'dark');
    myChart.showLoading();
    $.get('../static/data/test_json.json', function (webkitDep) {
        myChart.hideLoading();
        webkitDep.nodes.forEach(function (node) {
            node.value = node.value;
            node.category = node.category;
        });
        option = {
            tooltip: {},
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

            animationDuration: 5000,
            animationEasingUpdate: 'quinticInOut',
            series: [{
                type: 'graph',
                layout: 'force',
                animation: true,

                label: {
                    normal: {
                        position: 'right',
                        formatter: '{b}'
                    }
                },
                roam: true,
                focusNodeAdjacency: true,
                focusNodeAdjacency: true,
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
                            color: 'source',
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