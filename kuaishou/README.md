android模拟器标签要在抓包软件右边，再右是chrome
chrome设置启动时最大化
        
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
