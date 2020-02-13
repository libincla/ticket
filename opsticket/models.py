from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Owner(AbstractUser):
    group = models.CharField(max_length=256,null=True, verbose_name='用户组')


class Ticket(models.Model):
    PRIO_LOW = 1
    PRIO_MED = 2
    PRIO_HIGH = 3
    PRIO_ITEMS  = (
        (PRIO_LOW, '低'),
        (PRIO_MED, '中'),
        (PRIO_HIGH, '高'),

    )
    STATUS_FIN = 0
    STATUS_RUN = 1
    STATUS_BROKER = 2
    STATUS_ITEMS = (
        (STATUS_FIN, '已完成'),
        (STATUS_RUN, '正在做'),
        (STATUS_BROKER, '中断的'),
    )
     
    title = models.CharField(max_length=128, verbose_name='工单标题')
    content = models.TextField(verbose_name='工单正文')
    priority = models.PositiveIntegerField(default=PRIO_LOW, choices=PRIO_ITEMS, verbose_name='优先级')
    # assign_to = models.IntegerField(verbose_name='指派给谁')
    belong = models.CharField(max_length=256, verbose_name='工单的提交者', null=True)
    assign_to = models.CharField(max_length=128, verbose_name='指派对象')
    status =  models.PositiveIntegerField(default=STATUS_FIN, choices=STATUS_ITEMS, verbose_name='工单状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='工单创建时间')
    expired_time = models.DateTimeField(auto_now=False, verbose_name='工单销毁时间', blank=True)
    description = models.TextField(verbose_name='工单描述', null=True,)
    #开始定义关系
    owner = models.ForeignKey(Owner, verbose_name='工单所属')

    # @property
    # def all_comments(self):
    #     return c
    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '工单'
        ordering = ['-id'] #按照id进行降序排列
        permissions = (
            ('visit_Ticket', 'Can visit Ticket'),
        )


class Comment(models.Model):
    title = models.CharField(max_length=256, verbose_name='评论标题')
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField(auto_now=True, verbose_name='评论时间')
    owner = models.ForeignKey(Owner, verbose_name='评论者')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comment', verbose_name='所属工单')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '评论'
        ordering = ['-id']







