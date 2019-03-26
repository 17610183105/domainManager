from django.shortcuts import render,redirect,reverse
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app import models
from app.forms import domainForm,accountForm,domainsiteForm,recordForm,nameserverForm
from app.libs.site_api import GodaddyApi,DnsApi,CloudflareApi
from django.forms import modelformset_factory
import datetime
import logging
from django.db.models import Count
from django.core.paginator import Paginator
from app.filters import domainFilter


logger = logging.getLogger('django')

@login_required
def gentella_html(request):
    context = {}
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #如果验证成功,返回的是用户对象,如果不成功,返回的就是None
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect(reverse('index'))
            else:
                return render(request,'app/page_403.html')

    return render(request,'app/login.html')


def user_logout(request):
    logout(request)
    return redirect(reverse('user_login'))

################domain action
@login_required
def index(request):
    obj = models.domain.objects.all()
    filter_obj = domainFilter(request.GET,queryset=obj)
    name_search_info = request.GET.get('name__contains','')
    account_info = request.GET.get('account','')
    url_info = "&" + "name__contains=" + name_search_info + "&" + "account=" + account_info
    show_title_name = "域名列表"
    # paginator = Paginator(obj,10)
    paginator = Paginator(filter_obj.qs,10)
    page = request.GET.get('page',1)
    contacts = paginator.page(page)
    return  render(request,'app/index.html',{"contacts":contacts,"f":filter_obj,"show_title_name":show_title_name,"url_info":url_info})


@login_required
def domain_change(request,domain_id=None):
    if domain_id:
        obj = models.domain.objects.filter(pk=domain_id).first()
        form_obj = domainForm(instance=obj)
        # form_obj = modelformset_factory(models.domain,form=domainForm)
        show_title_name = "域名编辑"
    else:
        form_obj = domainForm()
        show_title_name = "域名添加"
    if request.method == 'POST':
        # 创建一个包含提交数据的form对象
        form_obj = domainForm(request.POST,instance=obj) if domain_id else  domainForm(request.POST)
        # 对提交的数据进行校验
        if form_obj.is_valid():
            # 保存数据
            form_obj.save()  # 新增
            # 跳转至展示页面
            return redirect(reverse('index'))
    return render(request, 'app/change_info.html', {'form_obj': form_obj, 'show_title_name':show_title_name})


@login_required
def domain_del(request,domain_id):
    models.domain.objects.get(pk=domain_id).delete()
    return redirect(reverse('index'))


#################account action
@login_required
def account_list(request):
    obj = models.account.objects.all()
    show_title_name = "帐号列表"
    return  render(request,'app/account_list.html',{"all_obj":obj,"show_title_name":show_title_name})


@login_required
def account_change(request,account_id=None):
    if account_id:
        obj = models.account.objects.filter(pk=account_id).first()
        form_obj = accountForm(instance=obj)
        show_title_name = "帐号编辑"
    else:
        form_obj = accountForm()
        show_title_name = "帐号添加"
    if request.method == 'POST':
        # 创建一个包含提交数据的form对象
        form_obj = accountForm(request.POST,instance=obj) if account_id else  accountForm(request.POST)
        # 对提交的数据进行校验
        if form_obj.is_valid():
            # 保存数据
            form_obj.save()  # 新增
            # 跳转至展示页面
            return redirect(reverse('account_list'))
    return render(request, 'app/change_info.html', {'form_obj': form_obj, 'show_title_name':show_title_name})


@login_required
def account_del(request,account_id):
    models.account.objects.get(pk=account_id).delete()
    return redirect(reverse('account_list'))


#################domainsite action
@login_required
def domainsite_list(request):
    obj = models.domainsite.objects.all()
    show_title_name = "域名商列表"
    return  render(request,'app/domainsite_list.html',{"all_obj":obj,"show_title_name":show_title_name})


@login_required
def domainsite_change(request,domainsite_id=None):
    if domainsite_id:
        obj = models.domainsite.objects.filter(pk=domainsite_id).first()
        form_obj = domainsiteForm(instance=obj)
        show_title_name = "域名商编辑"
    else:
        form_obj = domainsiteForm()
        show_title_name = "域名商添加"
    if request.method == 'POST':
        # 创建一个包含提交数据的form对象
        form_obj = domainsiteForm(request.POST,instance=obj) if domainsite_id else  domainsiteForm(request.POST)
        # 对提交的数据进行校验
        if form_obj.is_valid():
            # 保存数据
            form_obj.save()  # 新增
            # 跳转至展示页面
            return redirect(reverse('domainsite_list'))
    return render(request, 'app/change_info.html', {'form_obj': form_obj, 'show_title_name':show_title_name})


@login_required
def domainsite_del(request,domainsite_id):
    models.domainsite.objects.get(pk=domainsite_id).delete()
    return redirect(reverse('domainsite_list'))


#################record action
@login_required
def record_list(request,domain_id):
    domain_obj = models.domain.objects.get(pk=domain_id)
    obj = models.record.objects.filter(main_domain_id=domain_id)
    show_title_name = "域名商:" + domain_obj.account.domainsite.name + "--> " "所属帐号:" + domain_obj.account.account  + "--> " + "域名:" + domain_obj.name + " 记录列表"
    return  render(request,'app/record_list.html',{"all_obj":obj,"show_title_name":show_title_name,"domain_id":domain_id})


@login_required
def record_change(request,domain_id,record_id=None):
    domain_obj = models.domain.objects.filter(pk=domain_id).first()
    if record_id:
        obj = models.record.objects.filter(pk=record_id).first()
        form_obj = recordForm(instance=obj)
        show_title_name = "记录编辑"
    else:
        form_obj = recordForm()
        show_title_name = "记录添加"
    if request.method == 'POST':
        # 创建一个包含提交数据的form对象
        form_obj = recordForm(request.POST,instance=obj) if record_id else  recordForm(request.POST)
        # 对提交的数据进行校验
        if form_obj.is_valid():
            result = form_obj.save(commit=False)  # 新增,在这里设置主域名
            result.main_domain = domain_obj
            result.save()
            # form_obj.save()  # 新增
            # 跳转至展示页面
            return redirect(reverse('record_list',args=(domain_id,)))
    return render(request, 'app/change_info.html', {'form_obj': form_obj, 'show_title_name':show_title_name})


@login_required
def record_del(request,domain_id,record_id):
    models.record.objects.get(pk=record_id).delete()
    return redirect(reverse('record_list',args=(domain_id,)))


##################nameserver
@login_required
def nameserver_list(request,domainsite_id):
    domainsite_obj = models.domainsite.objects.get(pk=domainsite_id)
    obj = models.nameserver.objects.filter(domainsite_id=domainsite_id)
    show_title_name = "域名商" + domainsite_obj.name + " nameserver列表"
    return  render(request,'app/nameserver_list.html',{"all_obj":obj,"show_title_name":show_title_name,"domainsite_id":domainsite_id})


@login_required
def nameserver_change(request,domainsite_id,nameserver_id=None):
    domainsite_obj = models.domainsite.objects.filter(pk=domainsite_id).first()
    if nameserver_id:
        obj = models.nameserver.objects.filter(pk=nameserver_id).first()
        form_obj = nameserverForm(instance=obj)
        show_title_name = "nameserver编辑"
    else:
        form_obj = nameserverForm()
        show_title_name = "nameserver添加"
    if request.method == 'POST':
        # 创建一个包含提交数据的form对象
        form_obj = nameserverForm(request.POST,instance=obj) if nameserver_id else  nameserverForm(request.POST)
        # 对提交的数据进行校验
        if form_obj.is_valid():
            result = form_obj.save(commit=False)  # 新增,在这里设置主域名
            result.main_domain = domainsite_obj
            result.save()
            # form_obj.save()  # 新增
            # 跳转至展示页面
            return redirect(reverse('nameserver_list',args=(domainsite_id,)))
    return render(request, 'app/change_info.html', {'form_obj': form_obj, 'show_title_name':show_title_name})


@login_required
def nameserver_del(request,domainsite_id,nameserver_id):
    models.nameserver.objects.get(pk=nameserver_id).delete()
    return redirect(reverse('record_list',args=(domainsite_id,)))



###################sync
#同步指定帐号的域名到本地
def sync_to_local(request,account_id):
    account_obj = models.account.objects.filter(pk=account_id).first()
    site_name = account_obj.domainsite.name
    account_name = account_obj.account
    account_token = account_obj.token
    account_secret = account_obj.secret
    log_show_info = "add domain by  {} {}-->".format(site_name,account_name)
    if site_name == "godaddy":
        godaddy_api = GodaddyApi(account_token, account_secret)
        all_domain = godaddy_api.domain_list()
        for domain in all_domain:
            godaddy_api = GodaddyApi(account_token, account_secret)
            # ret = godaddy_api.domain_info(domain)
            # time.sleep(0.5)
            # nameserver_list = ret['nameServers']    #获取nameserver
            if models.domain.objects.filter(name=domain, account=account_obj): continue
            # models.domain.objects.create(name=domain,account=account_obj,ns1=nameserver_list[0],ns2=nameserver_list[1])
            models.domain.objects.create(name=domain,account=account_obj)
            logger.info(log_show_info  + domain)

    if site_name == "dns":
        dns_api = DnsApi(account_token,account_secret)
        all_domain_dict = dns_api.domain_list()
        all_domain = []
        for dic in all_domain_dict['data']:
            all_domain.append(dic['domains'])
        for domain in all_domain:
            if models.domain.objects.filter(name=domain, account=account_obj): continue
            models.domain.objects.create(name=domain, account=account_obj)
            logger.info(log_show_info +  domain)

    if site_name == "cloudflare":
        cloudflare_api = CloudflareApi(account_token,account_secret)
        result = cloudflare_api.get_zones()
        all_domain = []
        for el in result['result']:
            all_domain.append(el['name'])
        for domain in all_domain:
            if models.domain.objects.filter(name=domain, account=account_obj): continue
            models.domain.objects.create(name=domain, account=account_obj)
            logger.info(log_show_info + domain)

    return HttpResponse('初始化成功')


################ log show and count chart
def get_domain_count(request):
    show_title_name = "日志统计"
    today = datetime.date.today()   #int day
    day15_ago = today - datetime.timedelta(days=15)
    time_list = []
    data = {'key':[],'value':[]}
    for i in range(15):
        day_time = today-datetime.timedelta(days=i)
        time_list.append(day_time.today())
    domain_objs = models.domain.objects.filter(ctime__range=(day15_ago,today))
    ret = domain_objs.values_list('ctime').annotate(Count('id')).order_by('ctime')
    for k,v in ret:
        data['key'].append(str(k))
        data['value'].append(v)
    return render(request,'app/echarts.html',{"data":data,"show_title_name":show_title_name})


def log_show(request):
    pass
###################search
def search(request):
    show_title_name = '搜索域名所在帐号'
    if request.method == 'POST':
        show_title_name = '搜索结果'
        domain = request.POST.get('domain')
        all_account = models.account.objects.all()
        account_info = []
        def search_func(current_account, domain):
            name = current_account.domainsite.name
            account = current_account.account
            token = current_account.token
            secret = current_account.secret

            if name == "godaddy":
                godaddy_api = GodaddyApi(token, secret)
                if domain in godaddy_api.domain_list():
                    print('this is godaddy search result', domain)
                    return {'account': current_account,'domain':domain,'id':0}


            if name == "dns":
                dns_api = DnsApi(apiKey=token, Secret=secret)
                result = dns_api.domain_search(domain)

                if result['data']['data']:
                    print('this is dns search result', result)
                    return {'account':current_account,'domain':domain,'id':result['data']['data'][0]['domainsID']}

            if name == "cloudflare":
                cloudflare_api = CloudflareApi(token, secret)
                result = cloudflare_api.get_zones()
                all_domain = []
                for el in result['result']:
                    all_domain.append(el['name'])
                if domain in all_domain:
                    return {'account':current_account,'domain':domain,'id':0}




        for account in all_account:
            if search_func(account,domain):
                account_info.append(search_func(account,domain))
            else:
                continue

        if not account_info:
            account = {"pk":0,"account":"未匹配到域名"}
            account_info.append({"account":account,'domain':None,'id':0})
        return render(request,'app/show_result.html',{'account_infos':account_info,"show_title_name":show_title_name,"domain":domain})
    return render(request,'app/show_search.html',{"show_title_name":show_title_name})


#################sync ns to domainsite
def sync_ns(request,domain_id):
    domain = models.domain.objects.get(pk=domain_id)
    domain_name = domain.name
    account_token = domain.account.token
    account_secret = domain.account.secret
    all_ns = models.domain.objects.get(id=domain_id).nsrecord.all()
    record_list = []
    for ns in all_ns:
        record_list.append(ns.name)
    if  not record_list: return HttpResponse("请先为域名添加ns记录")
    godaddy_api = GodaddyApi(account_token,account_secret)
    godaddy_api.edit_ns(domain_name,record_list)
    return HttpResponse('同步ns记录成功')


###################sync record from domainsite to local
def sync_record_local(request,domain_id):
    domain = models.domain.objects.get(pk=domain_id)
    domain_name = domain.name
    account = domain.account
    name = account.domainsite.name
    token = account.token
    secret = account.secret
    type_dict = {
        'A':0,
        'CNAME':1,
        'MX':2,
        'TXT':3,
        'NS':4,
        'AAAAA':5,
        'SRV':6,
        'CAA':7,
        'NOTYPE':8,
    }
    if name == "godaddy":
        godaddy_api = GodaddyApi(token, secret)
        try:
            record_info = godaddy_api.record_list(domain_name)
        except Exception as e:
            record_info = []
        for info in record_info:
            if models.record.objects.filter(hostrecord=info['name'],recordvalue=info['data']): continue
            models.record.objects.create(hostrecord=info['name'],type=type_dict[info['type']],recordvalue=info['data'],main_domain=domain)

    if name == "dns":
        dns_api = DnsApi(token, secret)
        record_info = dns_api.record_list(domain_name)
        for info in record_info['data']['data']:
            if models.record.objects.filter(hostrecord=info['record'], recordvalue=info['value']): continue
            models.record.objects.create(hostrecord=info['record'], type=type_dict[info['type']],
                                         recordvalue=info['value'], main_domain=domain)
    if name == "cloudflare":
        cloudflare_api = CloudflareApi(token, secret)
        domain_search_id = cloudflare_api.get_domain_id(domain_name)
        record_info = cloudflare_api.record_list(domain_search_id)
        for info in record_info['result']:
            name = info['name'].replace("." + domain_name, '')
            if models.record.objects.filter(hostrecord=name, recordvalue=info['content']): continue
            models.record.objects.create(hostrecord=name, type=type_dict[info['type']], recordvalue=info['content'],
                                         main_domain=domain)

    return redirect(reverse('record_list',args=(domain_id,)))

############ sync record to dnssite
def sync_record_dnssite(request,domain_id,record_id):
    domain = models.domain.objects.get(pk=domain_id)
    record = models.record.objects.get(pk=record_id)
    domain_name = domain.name
    account_name = domain.account.domainsite.name
    account_token = domain.account.token
    account_secret = domain.account.secret
    record_type = record.get_type_display()
    record_hostname = record.hostrecord
    record_data = str(record.recordvalue)

    #处理godaddy的记录
    if account_name == "godaddy":
        godaddy_api = GodaddyApi(account_token, account_secret)
        data = godaddy_api.get_record(domain_name,record_hostname,record_type)
        if data:
            godaddy_api = GodaddyApi(account_token, account_secret)
            godaddy_api.record_edit(domain_name,record_data,record_type,record_hostname)
        else:
            godaddy_api = GodaddyApi(account_token, account_secret)
            godaddy_api.record_create(domain,record_data,record_hostname,record_type)

    #处理dns的记录
    if account_name == "dns":
        dns_api = DnsApi(apiKey=account_token, Secret=account_secret)
        domain_id = dns_api.get_domain_id(domain_name)
        print(domain_id)
        dns_api = DnsApi(apiKey=account_token, Secret=account_secret)
        result = dns_api.record_search(domain_id, record_hostname) #获取要操作的record
        print(result,'this is result')
        if result['data']['data']:
            record_id = result['data']['data'][0]['recordID']
            dns_api = DnsApi(apiKey=account_token, Secret=account_secret)
            dns_api.record_edit(domain_id,record_id,record_hostname,record_type,record_data)
        else:
            dns_api = DnsApi(apiKey=account_token, Secret=account_secret)
            dns_api.record_create(domain_id,record_type,record_hostname,record_data)

    #处理cloudflare的记录
    if account_name == "cloudflare":
        cloudflare_api = CloudflareApi(account_token,account_secret)
        domain_id = cloudflare_api.get_domain_id(domain_name)
        search_result = cloudflare_api.get_record(domain_id,domain_name,record_hostname,record_type)

        if search_result['result']:
            record_id = cloudflare_api.get_record_id(domain_id, domain_name, record_hostname, record_type)
            cloudflare_api.record_edit(domain_id,record_id,domain_name,record_hostname,record_type,record_data)
        else:
            cloudflare_api.record_create(domain_id,record_hostname,record_type,record_data)


    return HttpResponse('同步成功!')