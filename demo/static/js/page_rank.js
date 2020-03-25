// JavaScript Document

$(function () {
    var myChart = echarts.init(document.getElementById('main'), 'dark');
    myChart.showLoading();
    $.get('../static/data/text.gexf', function (xml) {//les-miserables  six
        myChart.hideLoading();
        var graph = echarts.dataTool.gexf.parse(xml);
        var categories = [];
        for (var i = 0; i < 5; i++) {
            categories[i] = {
                name: '可信级别：' + (i + 1)
            };
        }
        graph.nodes.forEach(function (node) {
            console.log(node)
            node.itemStyle = null;
            node.value = node.attributes.trust_value;
            console.log(node.value)
            node.symbolSize /= 1.0;
            node.label = {
                normal: {
                    show:true
                }
            };
            node.draggable = true;
            node.category = node.attributes.modularity_class;
            // node.category = 0;//跟 legend 联系在一起 legend 有几个，这边就有几个 数组；
        });
        mytextStyle = {
            color: '#fff',                           //文字颜色
            fontStyle: "normal",                     //italic斜体  oblique倾斜
            fontWeight: "bolder",                    //文字粗细bold   bolder   lighter  100 | 200 | 300 | 400...
            fontFamily: "Helvetica",                //字体系列
            fontSize: 18,                              //字体大小
        };

        option = {
            title: {
                text: '用户信任度聚类分析',
                subtext: '数据来源于Adgovato',
                sublink: "http://127.0.0.1:9999/evaluation_2",
                textStyle: mytextStyle,
                z: 2,
                top: '14%',
                left: '68%',
                color: 'white',
                borderColor: "#000",
                borderWidth: 0,
                shadowColor: "red",
            },
            tooltip: {},
            legend: [{
                orient: 'vertical',
                x: '10%',
                y: '20%',
                textStyle: {
                    color: '#fff'          // 图例文字颜色
                },
                size: 10,
                data: categories.map(function (a) {//  map() 方法返回一个由原数组中的每个元素调用一个指定方法后的返回值组成的新数组。
                    return a.name;
                })
            }],
            animationDuration: 5000,
            animationEasingUpdate: 'quinticInOut',
            series: [
                {
                    name: '信任数值',
                    type: 'graph',
                    layout: 'circular',
                    circular: {
                        rotateLabel: true,
                        layoutAnimation: true
                    },
                    legendHoverLink: true,
                    // force\circular
                    data: graph.nodes,
                    links: graph.links,
                    categories: categories,
                    roam: true,
                    focusNodeAdjacency: true,
                    itemStyle: {
                        normal: {
                            borderColor: '#FFC',
                            borderWidth: 1,
                            shadowBlur: 1,
                            shadowColor: 'rgba(0, 0, 0, 0.3)',
                            opacity: 0.6,
                        },
                        emphasis: {
                            borderWidth: 1.5,
                        }
                    },
                    label: {
                        normal: {
                            position: 'right',
                            formatter: '{b}'
                        }
                    },
                    lineStyle: {
                        normal: {
                            show: false,
                            color: 'source',
                            curveness: 0.2,
                            width: 1.5,
                        },
                        emphasis: {
                            width: 3.5,
                        }
                    },
                    edgeLabel: {
                        normal: {
                            show: false,
                        },
                        // emphasis: {
                        //     show: true,
                        // }
                    },
                    force: {
                        edgeLength: [100, 150],
                        repulsion: 200,
                        layoutAnimation: true
                    },
                    emphasis: {
                        lineStyle: {
                            width: 10,
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
    }, 'xml');
})