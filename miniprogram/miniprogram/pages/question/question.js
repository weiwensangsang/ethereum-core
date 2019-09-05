// miniprogram/pages/develop.js
Page({
  data: {
    _id: "暂无数据"
  },

  onLoad: function(options) {
    var that = this;
    that.setData({
      _id: options._id
    })
  }

})