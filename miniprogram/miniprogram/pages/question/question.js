// miniprogram/pages/develop.js
Page({
  data: {
    _id: "",
    name: ""
  },

  onLoad: function(options) {
    var that = this;
    that.setData({
      _id: options._id,
      name: options.name
    })
  }

})