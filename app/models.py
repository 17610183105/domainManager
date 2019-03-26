from __future__ import unicode_literals
from django.db import models


class domain(models.Model):
    name = models.CharField(max_length=128,verbose_name="域名")
    account = models.ForeignKey('account',verbose_name="关联帐号")
    nsrecord = models.ManyToManyField('nameserver',verbose_name="ns记录")
    desc = models.CharField(max_length=128,verbose_name="描述",null=True)
    ctime = models.DateField(auto_now_add=True,verbose_name="创建时间")
    mtime = models.DateField(auto_now=True,verbose_name="修改时间")


    def __str__(self):
        return self.name


class nameserver(models.Model):
    name = models.CharField(max_length=128,verbose_name="域名")
    domainsite = models.ForeignKey('domainsite',verbose_name="域名商")
    desc = models.CharField(max_length=128,verbose_name="描述",null=True)
    ctime = models.DateField(auto_now_add=True,verbose_name="创建时间")
    mtime = models.DateField(auto_now=True,verbose_name="修改时间")


    def __str__(self):
        return self.name

class account(models.Model):
    domainsite = models.ForeignKey('domainsite',verbose_name='域名商')
    account = models.CharField(max_length=64,verbose_name="帐号")
    token = models.CharField(max_length=64)
    secret = models.CharField(max_length=64, null=True)
    ctime = models.DateField(auto_now_add=True,verbose_name="创建时间")
    mtime = models.DateField(auto_now=True,verbose_name="修改时间")

    def __str__(self):
        return self.account

class domainsite(models.Model):
    name = models.CharField(max_length=128,verbose_name="域名商名称")
    url = models.URLField(max_length=128,verbose_name="网站URL")
    ctime = models.DateField(auto_now_add=True,verbose_name="创建时间")
    mtime = models.DateField(auto_now=True,verbose_name="修改时间")

    def __str__(self):
        return self.name

class record(models.Model):
    hostrecord = models.CharField(max_length=256, verbose_name='主机记录')
    type = models.IntegerField(default=8, verbose_name='类型', choices=(
        (0, 'A'),
        (1, 'CNAME'),
        (2, 'MX'),
        (3, 'TXT'),
        (4, 'NS'),
        (5, 'AAAAA'),
        (6, 'SRV'),
        (7, 'CAA'),
        (8, 'NOTYPE'),
    ))
    recordvalue = models.CharField(max_length=256, verbose_name='解析值')
    status = models.BooleanField(default=True, verbose_name='状态')
    main_domain = models.ForeignKey('domain', verbose_name='关联域名')
    ctime = models.DateField(auto_now_add=True,verbose_name="创建时间")
    mtime = models.DateField(auto_now=True,verbose_name="修改时间")

    def __str__(self):
        return self.hostrecord



