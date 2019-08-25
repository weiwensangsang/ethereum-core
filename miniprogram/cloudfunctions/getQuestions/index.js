// 云函数入口文件
const cloud = require('wx-server-sdk')

cloud.init()
const db = cloud.database()
// 云函数入口函数
exports.main = async(event, context) => {
  return await db.collection('question')
    .orderBy('createTime', 'desc')
    .limit(5) // 限制返回数量为 5 条
    .get()
    .then(res => {
      console.log(res.data)
    })
    .catch(err => {
      console.error(err)
    })
}