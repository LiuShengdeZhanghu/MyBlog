from .models import Comment
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm

# Create your views here.

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    comment_form = CommentForm(request.POST, user = request.user)
    data = {}
    if comment_form.is_valid():
        # 数据检查通过，保存评论
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data["text"]
        comment.content_object = comment_form.cleaned_data["content_object"]

        # 判断是否是回复，如果是评论是否是顶级回复
        parent = comment_form.cleaned_data["parent"]
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        # 发送邮件通知，多线程，异步执行，发送邮件比较耗时
        comment.send_eamil()

        # 返回数据
        data["status"] = 'SUCCESS'
        data["username"] = comment.user.username
        data["comment_time"] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data["text"] = comment.text
        data["content_type"] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data["reply_to"] = comment.reply_to.username
        else:
            data["reply_to"] = ""

        if not comment.root is None:
            data["root_pk"] = comment.root.pk
        else:
            data["root_pk"] = ""
        data["pk"] = comment.pk
    else:
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data["status"] = "ERROR"
        data["message"] = list(comment_form.errors.values())[0][0]   #字典类型，取出值转为list，再取出第一个
    return JsonResponse(data)