from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone

# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0,verbose_name="阅读数量")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpand():
    def read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            read_num = ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return read_num.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

    read_num.short_description = "阅读数量"

class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)  #默认为当天
    read_num = models.IntegerField(default=0,verbose_name="日常阅读数量")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')