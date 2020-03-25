/* eslint-disable */
(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else {
    root.globalConfig = factory(root.b);
  }
})(typeof self !== 'undefined' ? self : this, function () {
  
  /* 配置项开始 */

  var globalConfig = {
		// ano by terry 20180810 内部开发使用时放开.
//		baseUrl: './api',//  byRobin 20180905本地开发用
		// modify by terry 20180724 因为项目部署到 /intellinlp-kg-web/v2，所以需要向上跳2级，后续根据需要进行调整.
		// ano by terry 20180810 打包系统至外网服务器时，需放开（因外网Nginx代理多设置了一个api路径，固需要写两个）.
       baseUrl: './api/api',  //打包用  byRobin 20180905
	 // modify by terry 20180726 新的demo.jovemind.com使用.
	 // baseUrl: 'http://43.240.136.146:8090/intellinlp-kg-web/api',
    modeList: [
      {
        mode: 1,
        desc: '第一种模式'
      },
      {
        mode: 2,
        desc: '第二种模式'
      },
      {
        mode: 3,
        desc: '第三种模式'
      },
    ],
      // 20180713 cein 节点颜色
    nodecolorsel:[
		{
			mode: 1,
			desc: '类型'
		},
		{
			mode: 2,
			desc: '聚类'
		},
		{
			mode: 3,
			desc: '度'
//			desc: this.$t('Degree')
		},
		],
		linkcolorsel:[
		{
			mode: 1,
			desc: '类型'
		},
		{
			mode: 2,
			desc: '点'
		},
		{
			mode: 3,
			desc: '线索数量'
		},
		],
    nodeColor: [
    	[
    		{
	    		mode: 1,
	    		color: '#49A7FF',
		    	desc: '机构'
		    },
		    {
		    	mode: 2,
		    	color: '#ef6f99',
		    	desc: '人'
		    },
		    {
		    	mode: 3,
		    	color: '#2ABC73',
		    	desc: '产品'
		    },
		    {
		    	mode: 4,
		    	color: '#8E9DEF',
		    	desc: '地点'
		    }
    	],
    	[
    		{
	    		mode: 1,
	    		color: '#007300',
		    	desc: '聚类1'
		    },
		    {
		    	mode: 2,
		    	color: '#B238AD',
		    	desc: '聚类2'
		    },
		    {
		    	mode: 3,
		    	color: '#FF8F00',
		    	desc: '聚类3'
		    },
		    {
		    	mode: 4,
		    	color: '#E24272',
		    	desc: '聚类4'
		    }
    	],
    	[
    		{
	    		mode: 1,
	    		color: '#FF8F00',
		    	desc: '度1'
		    },
		    {
		    	mode: 2,
		    	color: '#E24272',
		    	desc: '度2'
		    },
		    {
		    	mode: 3,
		    	color: '#B238AD',
		    	desc: '度3'
		    },
		    {
		    	mode: 4,
		    	color: '#8E9DEF',
		    	desc: '度4'
		    }
    	],
			[
        {
          mode: 1,
          color: '#49A7FF',
          desc: '机构'
        },
        {
          mode: 2,
          color: '#EF6F99',
          desc: '人'
        },
        {
          mode: 3,
          color: '#8E9DEF',
          desc: '产品'
        },
        {
          mode: 4,
          color: '#2ABC73',
          desc: '地点'
        }
      ],
      [
        {
          mode: 1,
          color: '#FF8F00',
          desc: '线索1-10'
        },
        {
          mode: 2,
          color: '#E24272',
          desc: '线索10-100'
        },
        {
          mode: 3,
          color: '#B238AD',
          desc: '线索100-200'
        },
        {
          mode: 4,
          color: '#8E9DEF',
          desc: '线索200-1000'
        }
      ],
      [
        {
          mode: 1,
          color: '#289AA3',
          desc: '竞争'
        },
        {
          mode: 2,
          color: '#4B8CE3',
          desc: '合作'
        },
        {
          mode: 3,
          color: '#515FA5',
          desc: '控股'
        },
        {
          mode: 4,
          color: '#4EA484',
          desc: '共现'
        }
      ]
    ]
    
  };
  

  
  
  
  

  /* 配置项结束 */

  return globalConfig;
});
