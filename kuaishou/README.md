第一步 确定python+鼠标 上传到 youtube和b站。
        快手名字格式 Better than tik tok: kuaishou ‘关键字’合集 “大于10个字的第一句话”
        标签 tik tok 快手 关键字
        简介 一样
        全翻译 英文
        
        b站名字格式 ‘关键字’合集 “大于10个字的第一句话”
        标签 tik tok 快手 关键字
        简介 一样
        

        
        static function OnBeforeResponse(oSession: Session) {
        if (m_Hide304s && oSession.responseCode == 304) {
            oSession["ui-hide"] = "true";
        }
        
        
        if (oSession.fullUrl.Contains("aweme/v1/search/item")) {
            oSession.utilDecodeResponse();
            var fso;
			var file;
            var filename = oSession.fullUrl.Split('/')[3]+'.json';
			MessageBox.Show(oSession.GetRequestBodyAsString())

            fso = new ActiveXObject("Scripting.FileSystemObject");
            file = fso.OpenTextFile("D:\\ae\\"+ filename, 2 ,true, 0);
            var o = oSession.GetResponseBodyAsString();

            var rJSON = Fiddler.WebFormats.JSON.JsonDecode(o);

            var d = Fiddler.WebFormats.JSON.JsonEncode(rJSON.JSONObject)

            file.writeLine (d);
            file.close();
            
        }
            
    }
            
    }
