// miniprogram/pages/develop.js
Page({
  data: {
    focus: false,
    inputValue: '',
    name: '你会打呼噜吗？',
    vote_A: "会",
    vote_B: "不会",
    vote_C: "吃瓜通道",
  },
  inputData: function(e) {
    var value = e.detail.value;
    switch (e.currentTarget.id) {
      case "name":
        this.setData({
          name: value
        });
        break;
      case "vote_A":
        this.setData({
          vote_A: value
        });
        break;
      case "vote_B":
        this.setData({
          vote_B: value
        });
        break;
      case "vote_C":
        this.setData({
          vote_C: value
        });
        break;
    }
  },
  createQusetion: function(e) {
   
    let that = this
    wx.cloud.callFunction({
      // 要调用的云函数名称
      name: 'createQuestion',
      // 传递给云函数的event参数
      data: {
        name: that.data.name + Math.floor(Math.random() * 1000000 + 1),
        vote_A: that.data.vote_A,
        vote_B: that.data.vote_B,
        vote_C: that.data.vote_C
      }
    }).then(res => {
      wx.showToast({
        title: "成功",
        duration: 2000
      })
    }).catch(err => {
      wx.showToast({
        title: "失败",
        duration: 2000
      })
    })
  }
})