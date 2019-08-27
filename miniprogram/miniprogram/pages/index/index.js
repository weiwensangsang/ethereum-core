//index.js
const app = getApp()

Page({
  data: {
    pageIndex: 1,
    pageSize: 10,
    pageCount: 0,
    amount: 0,
    list: [],

    currentTab: 0,
    loading: false,
    color: '#000',
    background: '#fff',
    show: true,
    animated: false,
    toView: 'red',
    scrollTop: 100,
    avatarUrl: './user-unlogin.png',
    userInfo: {},
    hasUserInfo: false,
    logged: false,
    takeSession: false,
    windowHeight: 0,
    scrollViewHeight: 0,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    requestResult: '',
    tabList: [{
        text: "首页",
        iconPath: "/images/tabbar/home_default.png",
        selectedIconPath: "/images/tabbar/home_active.png",
      }, {
        text: "动态",
        iconPath: "/images/tabbar/message_default.png",
        selectedIconPath: "/images/tabbar/message_active.png",
      },
      {
        text: "我的",
        iconPath: "/images/tabbar/me_default.png",
        selectedIconPath: "/images/tabbar/me_active.png",
        badge: 'New'
      }
    ]
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },

  onLoad: function() {
    var that = this;
    wx.getSystemInfo({
      success: function(res) {
        that.setData({
          windowHeight: res.windowHeight
        });
      }
    });
    let query = wx.createSelectorQuery().in(this);
    query.select('#tabbar').boundingClientRect();
    query.exec((res) => {
      that.setData({
        scrollViewHeight: that.data.windowHeight - res[0].height
      })
    })
    this.getData()
  },
  
  upper: function (e) {
    this.data.pageIndex = 1;
    this.getData()
  },

  lower: function (e) {
    if (this.data.pageIndex < this.data.pageCount) {

      this.data.pageIndex++;

      this.getData();
    } else {
      console.log("没数据了")
    }
  },

  onGetUserInfo: function(e) {
    if (!this.logged && e.detail.userInfo) {
      this.setData({
        logged: true,
        avatarUrl: e.detail.userInfo.avatarUrl,
        userInfo: e.detail.userInfo
      })
    }
  },
  tabChange(e) {
    // console.log('tab change', e);
    var that = this;
    if (this.data.currentTab === e.detail.index) {
      return false;
    } else {
      that.setData({
        currentTab: e.detail.index,
      })
    }
  },
  getData: function() {
    var that = this;
    if (that.pageIndex == 1) {
      console.log("获取中")
    }
    wx.cloud.callFunction({
      // 要调用的云函数名称
      name: 'getQuestions',
      // 传递给云函数的event参数
      data: {
        pageIndex: that.data.pageIndex,
        pageSize: that.data.pageSize
      }
    }).then(res => {
      var data = res.result;
      var tempList = data.list;
      var tempPageIndex = data.pageIndex;
      console.log('tempPageIndex ' + tempPageIndex)
      if (that.data.pageIndex == 1) { // 下拉刷新
        tempList = data.list;
        tempPageIndex = 1;
      } else { // 加载更多
        tempList = tempList.concat(data.list)
        tempPageIndex += 1;
        console.log('tempPageIndex ' + tempPageIndex)

      }
      that.setData({
        pageIndex: tempPageIndex,
        pageSize: data.pageSize,
        pageCount: data.pageCount,
        amount: data.amount,
        list: tempList
      })

      console.log('pageIndex ' + this.data.pageIndex)

    }).catch(err => {
      console.log(err)
    })
  }

})