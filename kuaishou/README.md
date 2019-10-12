flidder 夜神 chrome ss b站
chrome设置启动时最大化
模拟器按照搜狗输入法


        
        b站名字格式 ‘关键字’合集 “大于10个字的第一句话”
        标签 tik tok 快手 关键字
        简介 一样
        

        

static function OnBeforeResponse(oSession: Session) {
        if (m_Hide304s && oSession.responseCode == 304) {
            oSession["ui-hide"] = "true";
        }
        
        if (oSession.fullUrl.Contains("aweme/v1/search/item")) {
            oSession.utilDecodeResponse();
            var path = "C:\\Users\\weiwensangsang\\Documents\\GitHub\\WeBattle\\kuaishou\\resource\\douyin\\"
            var fso;
            var file;
            var s = oSession.GetRequestBodyAsString().Split('&')
			var key = decodeURI(s[0]).Split('=')[1]
            var name =  key + '_' + s[1].Split('=')[1]
			
			
            var filename = path + key + '\\' + name +'.json';

            fso = new ActiveXObject("Scripting.FileSystemObject");
			if (!fso.FolderExists(path + key)){
				fso.CreateFolder(path + key);
			}
            file = fso.OpenTextFile(filename, 2 ,true, 0);
            var o = oSession.GetResponseBodyAsString();

            var rJSON = Fiddler.WebFormats.JSON.JsonDecode(o);

            var d = Fiddler.WebFormats.JSON.JsonEncode(rJSON.JSONObject)

            file.writeLine (d);
            file.close();
            
        }
    }

1. Java语言基础

   1. JVM

   2. io

   3. 集合

   4. 多线程异步、并发有深入理解

      

2. 分布式系统原理

   1. 分布式系统的设计和应用，熟悉分布式、缓存、消息等机制

   2. java主流中间件，至少精通1-2类

   3. Dubbo或类似框架、Zookeeper、Elasticsearch/Solr、Redis、RocketMQ、kafka、分布式调度等开源框架及产品

   4. 分布式系统原理：CAP、最终一致性、幂等操作等；大型网络应用架构：消息中间件、缓存、负载均衡、集群技术、数据同步；高可用、可容灾分布式系统设计能力

   5. Microservice、FaaS、Serverless等微服务或无服务架构及实践经验者优先，熟悉分布式框架、中间件、数据库等机制

   6. NoSQL、MQ、Cache等原理，能够设计复杂业务、高并发、大数据量的系统

      

      

3. 常见的个性化要求

   1. 常见的架构设计方法和模式

   2. DDD/敏捷开发体系

   3. CI/CD、DevOps

   4. 虚拟化技术、虚拟化安全者优先

   5. 可信体系TPM、SGX

   6. Velocity

   7. 全栈研发，BOSS系统

   8. Flink、ES、Hive、Spark、HBase、图数据库

      

      

4. 算法基础

   1. 链表，二叉树，trie，栈，队列，向量/数组列表，散列表
   2. 广度优先搜索，深度优先搜索，二分查找，归并排序，快速排序，树的插入和查找
   3. 位操作，内存（堆与栈）
