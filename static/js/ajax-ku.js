var AjaxUtil={
    //基础选项
    options:{
        method:"get",  //提交的方法，默认为GET
        url:"",     //请求的路径
      //请求的参数
        type:"text", //返回内容的类型
        callback:function () {
            //回调函数
        },
        params:{}
    },

    //创建XMLHTTPRequest对象
    createRequest: function () {
        var xmlHttp;
        try{
            xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e){
            try{
                xmlHttp=new new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e){
                try{
                    xmlHttp=new XMLHttpRequest();
                if(xmlHttp.overrideMimeType){
                    xmlHttp.overrideMimeType("text/html");
                }
                }
                catch (e){
                    alert("你的浏览器不支持ajax");
                }
            }
        }
        return xmlHttp;
    },
    //设置基础选项
    setOptions : function (newOptions) {
        for(var pro in newOptions){
            this.options[pro] =newOptions[pro];
        }
    },
    //格式化请求参数
    formateParameters : function (ajaxobj) {
        var paramsArray = [];
        var params = ajaxobj.options.param;
        for(var pro in params){
            var paramValue = params[pro];
            paramsArray.push(pro+"="+paramValue);
        }

        return paramsArray.join("&");
    },
    //状态改变的处理
    readystatechange : function (xmlHttp) {
        //获取返回值
        var returnvalue;
        if(xmlHttp.readyState==4 && xmlHttp.status==200){
            switch (this.options.type){
                case 'xml':
                    returnvalue=xmlHttp.responseXML;
                    break;
                case 'json':
                    var jsonText=xmlHttp.responseText
                    if(jsonText){
                        returnvalue=eval("("+jsonText+")");
                    }
                    break;
                default:
                    returnvalue=xmlHttp.responseText;
                    break;
            }
            if(returnvalue){
                this.options.callback.call(this,returnvalue);
            }else {
                this.options.callback.call(this);
            }
        }
    },
    //发送ajax请求
    request : function (options) {
        var ajaxObj=this;
        //设置参数
        ajaxObj.setOptions.call(ajaxObj,options);
        //创建XMLHTTPRequest对象
        var xmlHttp=ajaxObj.createRequest.call(ajaxObj);

        //设置回调函数
        xmlHttp.onreadystatechange = function () {
            ajaxObj.readystatechange.call(ajaxObj,xmlHttp);
        };

        //格式化参数
        var paramsArray = [];
        var params = ajaxObj.options.params;
        for(var pro in params){
            var paramValue = params[pro];
            paramsArray.push(pro+"="+paramValue);
        }

        var formateParams = paramsArray.join("&");
        //请求的方式
        var method = ajaxObj.options.method;
        var url=ajaxObj.options.url;

        if("GET" == method.toUpperCase()){
            url+="?"+formateParams;
            // alert(formateParams);
            // url += "?"+"id=00001";
        }

        //建立连接
        xmlHttp.open(method,url,true);

        if("GET" == method.toUpperCase()){
            xmlHttp.send(null);
        }else if("POST" == method.toUpperCase()) {
            //如果是POST提交，则设置请求头
            xmlHttp.setRequestHeader("Conten-Type","application/x-www-form-urlencoded")
            xmlHttp.send(params);
        }
    }
};

function findUser() {
    var userid = $("talksub").value;

    if(userid){
        AjaxUtil.request({
            url:"http://127.0.0.1:8000/home",
            params:{word:userid},
            type:'json',
            callback:process
        });
    }
}

function process(json) {
    if(json){
        // $("id").innerHTML=json.id;
        // $("username").innerHTML=json.username;
        // $("age").innerHTML=json.age;
        alert("ll");
        var TalkWords=json.title+json.content+json.public_time;
        var Words = document.getElementById("words");
        var Who = document.getElementById("who");
        var TalkSub = document.getElementById("talksub");
        str = '<div class="atalk"><span>A说 :' + TalkWords.value +'</span></div>';
         Words.innerHTML = Words.innerHTML + str;
         Words.scrollTop = Words.scrollHeight;
    }
    else {
        $("msg").value="用户不存在";
        $("id").innerHTML="";
        $("username").innerHTML="";
        $("age").innerHTML="";
    }
}

function $(id) {
    return document.getElementById(id);
}

function checkid() {
    var uid=document.getElementById("userid").value;
    if(uid == ""){
        alert('请输入id');

    }
    else {
        AjaxUtil.request({
            url:"http://127.0.0.1:8000/blog/ajax_user",
            params:{id:uid,action:"checkname"},
            type:'text',
            callback:recheck
        });
    }
}

function recheck(text) {
    var span=document.getElementById("show")

    if(text == "1"){
        span.style.display="block";
        span.innerHTML="用户的id已经存在，请重新输入";
    }
    if(text=="0"){
        span.innerHTML="";
        span.style.display="block";
    }
}