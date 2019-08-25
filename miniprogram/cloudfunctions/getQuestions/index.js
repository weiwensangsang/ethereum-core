// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init()
const db = cloud.database()
// 云函数入口函数
exports.main = async(event, context) => {
  var pageIndex = event.pageIndex;
  var pageSize = event.pageSize;

  var amount = await db.collection('question')
    .count()
    .then(res => {
      return res.total
    })

  var pageCount = Math.ceil(amount / pageSize);

  var list = await db.collection('question')
    .orderBy('createTime', 'desc')
    .skip((pageIndex - 1) * pageSize)
    .limit(pageSize) // 限制返回数量为 5 条
    .get().then(res => {
      return res.data
    })

  return {
    amount: amount,
    pageCount: pageCount,
    pageSize: pageSize,
    list: list
  }
}