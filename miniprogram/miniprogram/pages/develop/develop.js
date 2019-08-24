// miniprogram/pages/develop.js
Page({
  data: {
    focus: false,
    inputValue: '',
    name: '',
    vote_A: "23",
    vote_B: "23",
    vote_C: "23",
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
    console.log(that.data)
    wx.cloud.callFunction({
      // 要调用的云函数名称
      name: 'createQuestion',
      // 传递给云函数的event参数
      data: {
        name: that.data.name,
        vote_A: that.data.vote_A,
        vote_B: that.data.vote_B,
        vote_C: that.data.vote_C
      }
    }).then(res => {
      console.log(res.result)
    }).catch(err => {
      console.log(err)
    })
  }
})