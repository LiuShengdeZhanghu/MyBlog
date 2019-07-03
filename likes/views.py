from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount,LikeRecord
# Create your views here.

def ErrorResponse(code,message):
    data = {}
    data["status"] = "ERROR"
    data["code"] = code
    data["message"] = message
    return JsonResponse(data)

def SuccessResponse(like_num):
    data = {}
    data["status"] = "SUCCESS"
    data["like_num"] = like_num
    return JsonResponse(data)

def like_change(request):
    if request.method == "GET":
        user = request.user
        # 用户是否登录验证
        if not user.is_authenticated:
            return ErrorResponse(400,"您还没有登录")

        obejct_id = int(request.GET.get("obejct_id"))
        content_type = request.GET.get("content_type")
        # 获取真正的content_type对象
        # 判断点赞的对象是否存在
        try:
            content_type = ContentType.objects.get(model=content_type)
            model_class = content_type.model_class()
            model_obj = model_class.objects.get(pk=obejct_id)
        except ObjectDoesNotExist:
            return ErrorResponse(401,"点赞的对象不存在")

        is_like = request.GET.get("is_like")

        if is_like == 'true':
            # 点赞
            # 返回值两个 一个是LikeRecord的实例化对象，一个是是否创建
            like_record,created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=obejct_id,user=user)
            if created:
                # 新增，未点赞过，进行点赞
                like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obejct_id)
                like_count.liked_num += 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                # 已经点赞过，不能重复点赞
                return ErrorResponse(402,"已经点赞过，重复点赞")
        else:
            # 取消点赞
            if LikeRecord.objects.filter(content_type=content_type, object_id=obejct_id,user=user).exists():
                # 点赞过，取消该用户的点赞
                like_record = LikeRecord.objects.get(content_type=content_type, object_id=obejct_id, user=user)
                like_record.delete()
                # 点赞总数减一
                like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obejct_id)
                if not created:
                    # 表示这个类型确实被点赞过，总点赞数存在且大于0
                    like_count.liked_num -= 1
                    like_count.save()
                    return SuccessResponse(like_count.liked_num)
                else:
                    return ErrorResponse(404, "数据错误")

            else:
                # 没有点赞过，无法进行取消
                return ErrorResponse(403, "您没有赞过，不能进行取消点赞")
