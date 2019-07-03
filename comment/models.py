import threading
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
# Create your models here.

class SendEmail(threading.Thread):
    def __init__(self,subject, text,email,fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    # 执行多线程的时候会执行run中的代码
    def run(self):
        send_mail(self.subject,
                  '',
                  settings.EMAIL_HOST_USER,
                  [self.email],
                  fail_silently=self.fail_silently,
                  # 转换为html邮件
                  html_message=self.text
                  )

class Comment(models.Model):
    # models.CASCADE 联级删除，比如删除user，也会把该User评论的内容删除，但是删除comment时候也不会删除user，比较合理
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    #contentpye 对Django的数据库模型中的进行关联

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE)

    #评论下的回复的最顶级的
    root = models.ForeignKey('self',related_name="root_comment",null=True,on_delete=models.CASCADE)
    # 评论回复功能的上一级s是谁
    parent = models.ForeignKey('self',related_name="parent_comment",null=True,on_delete=models.CASCADE)
    # 回复的对象，这里设置了两个关联到User的外键，为了你能够反向解析出（用User找出该用户的所有评论），对反向解析的目标字段进行修改
    reply_to = models.ForeignKey(User,related_name="replies",null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def send_eamil(self):
        # 发送邮件通知
        if self.parent is None:
            # 如果是评论文章
            # 在model中创建的方法，得到被评论的博客的作者的email
            email = self.content_object.get_email()
            subject = "你的博客收到新的评论"
        else:
            # 如果是回复
            email = self.reply_to.email
            subject = "有人回复你的评论"
        if email != '':
            # 在model中创建的方法，得到被评论的博客的链接
            # text ="%s \n<a href='%s'>'%s'</a>"%(self.text,self.content_object.get_url(),'查看'+self.content_object.get_url())
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text =render_to_string("comment/email.html",context)
            # 执行多线程
            send_mail = SendEmail(subject,text,email)
            send_mail.start()

    #让评论时间最新的在最上面
    class Meta():
        ordering = ['comment_time']
