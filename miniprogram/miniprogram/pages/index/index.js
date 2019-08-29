//index.js
const app = getApp()
const {
  $Message
} = require('../../iview/dist/base/index');

Page({
  data: {
    pageIndex: 1,
    pageSize: 10,
    pageCount: 0,
    amount: 0,
    list: [],
    showTopLoad: false,

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
    this.getData('top')
  },

  upper: function(e) {
    this.data.pageIndex = 1;
    var that = this;
    console.log("获取中")
    wx.cloud.callFunction({
      // 要调用的云函数名称
      name: 'getQuestions',
      // 传递给云函数的event参数
      data: {
        pageIndex: that.data.pageIndex,
        pageSize: that.data.pageSize
      }
    }).then(res => {
      var vm = res.result;
      var tempList = that.data.list;
      var tempPageIndex = that.data.pageIndex;
      tempList = vm.list;
      tempPageIndex = 1;
      that.setData({
        pageIndex: tempPageIndex,
        pageSize: vm.pageSize,
        pageCount: vm.pageCount,
        amount: vm.amount,
        list: tempList
      })
      console.log('获取完第一页')
      this.showTopLoad = false;
    }).catch(err => {
      console.log(err)
    })
  },





  lower: function(e) {
    // if (this.data.pageIndex < this.data.pageCount) {

    //   this.data.pageIndex++;

    //   this.getData();
    // } else {
    //   console.log("没数据了")
    // }
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
  getData: function(direction) {
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
      var vm = res.result;
      var tempList = that.data.list;
      var tempPageIndex = that.data.pageIndex;
      if (that.data.pageIndex == 1) {
        tempList = vm.list;
        tempPageIndex = 1;
      } else { // 加载更多
        tempList = tempList.concat(vm.list)
        tempPageIndex += 1;
      }
      that.setData({
        pageIndex: tempPageIndex,
        pageSize: vm.pageSize,
        pageCount: vm.pageCount,
        amount: vm.amount,
        list: tempList
      })
    }).catch(err => {
      console.log(err)
    })
  }

})