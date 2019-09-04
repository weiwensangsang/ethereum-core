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

  onLoad: function() {
    this.setPage()
    this.upper();
  },

  setPage: function() {
    var that = this;
    wx.getSystemInfo({
      success: function (res) {
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
  },

  upper: function(e) {
    wx.showToast({
      title: '刷新中',
      icon: 'loading',
      duration: 2000
    });
    this.data.pageIndex = 1;
    var that = this;
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
      setTimeout(function() {
        wx.showToast({
          title: '已更新',
          icon: 'success',
          duration: 500
        })
      }, 500)
    }).catch(err => {
      console.errpe(err)
    })
  },





  lower: function(e) {
    if (this.data.pageIndex < this.data.pageCount) {
      wx.showToast({
        title: '下一页',
        icon: 'loading',
        duration: 4000
      })
      this.data.pageIndex++;

      var that = this;
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

        tempList = tempList.concat(vm.list)
        tempPageIndex += 1;

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

    } else {
      setTimeout(function() {
        wx.showToast({
          title: '到底了',
          icon: 'success',
          duration: 2000
        })
      }, 500)
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
  }
})