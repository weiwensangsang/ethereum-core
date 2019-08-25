//index.js
const app = getApp()

Page({
  data: {
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
    list: [{
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
  getUserInfo: function (e) {
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
    console.log(e)
  },
  lower: function(e) {
    console.log(e)
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