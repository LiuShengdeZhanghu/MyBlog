// $(function(){

// });

function likeChange(obj,content_type,obejct_id) {
    var like_span = $(obj);

    var is_like = like_span.hasClass("active") == false;
    console.log(is_like);
    $.ajax({
        url:"/likes/like_change",
        type:"GET",
        data:{
            "content_type":content_type,
            "obejct_id":obejct_id,
            "is_like":is_like
        },
        cache:false,
        success:function (data) {
            console.log(data);
            if(data["status"]=="SUCCESS"){
                // 更新点赞状态
                if(is_like){
                    like_span.addClass("active");
                }else {
                    like_span.removeClass("active");
                }
                // 更新点赞数量
                like_span.next().text(data["like_num"]);
            }else {
                if(data["code"] == 400){
                    var modal = $('#login_or_register_model');
                    modal.modal('show');
                    modal.css("padding-right","0px");
                }else {
                    alert(data["message"]);
                }
            }
        },
        error:function (xhr) {
            console.log(xhr);
        }
    })
}