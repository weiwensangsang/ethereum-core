const cloud = require('wx-server-sdk')
cloud.init()

const db = cloud.database()
const _ = db.command

// 云函数入口函数
exports.main = async (event, context) => {
  return await db.collection('question').add({
    data: {
      name: event.name,
      vote_A: event.vote_A,
      vote_B: event.vote_B,
      vote_C: event.vote_C
    }
  })

}