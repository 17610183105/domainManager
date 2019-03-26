from django.conf.urls import url,include
from app import views

urlpatterns = [
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$',views.user_login,name='user_login'),
    url(r'^logout/$',views.user_logout,name='user_logout'),
    #domain action
    url(r'^domain_add/$',views.domain_change,name='domain_add'),
    url(r'^domain_edit/(\d+)/$',views.domain_change,name='domain_edit'),
    url(r'^domain_del/(\d+)/$',views.domain_del,name='domain_del'),
    #account action
    url(r'^account_list/$',views.account_list,name='account_list'),
    url(r'^account_add/$',views.account_change,name='account_add'),
    url(r'^account_edit/(\d+)/$',views.account_change,name='account_edit'),
    url(r'^account_del/(\d+)/$',views.account_del,name='account_del'),
    #domainsite action
    url(r'^domainsite_list/$',views.domainsite_list,name='domainsite_list'),
    url(r'^domainsite_add/$',views.domainsite_change,name='domainsite_add'),
    url(r'^domainsite_edit/(\d+)/$',views.domainsite_change,name='domainsite_edit'),
    url(r'^domainsite_del/(\d+)/$',views.domainsite_del,name='domainsite_del'),
    #record action
    url(r'^record_list/(\d+)/$',views.record_list,name='record_list'),
    url(r'^record_add/(\d+)/$',views.record_change,name='record_add'),
    url(r'^record_edit/(\d+)/(\d+)/$',views.record_change,name='record_edit'),
    url(r'^record_del/(\d+)/(\d+)/$',views.record_del,name='record_del'),
    # #nameserver action
    url(r'^nameserver_list/(\d+)/$',views.nameserver_list,name='nameserver_list'),
    url(r'^nameserver_add/(\d+)/$',views.nameserver_change,name='nameserver_add'),
    url(r'^nameserver_edit/(\d+)/(\d+)/$',views.nameserver_change,name='nameserver_edit'),
    url(r'^nameserver_del/(\d+)/(\d+)/$',views.nameserver_del,name='nameserver_del'),
    #sync domainsite
    url(r'^sync_to_local/(\d+)/$',views.sync_to_local,name='sync_to_local'),
    #log count chart
    url(r'^get_domain_count/$',views.get_domain_count,name='get_domain_count'),
    #log show chart
    url(r'^log_show/$',views.log_show,name='log_show'),
    #search domain  account
    url(r'^search/$',views.search,name='search'),
    #sync ns
    url(r'^sync_ns/(\d+)$',views.sync_ns,name='sync_ns'),
    #sync record to local
    url(r'^sync_record_local/(\d+)$',views.sync_record_local,name='sync_record_local'),
    #sync record to dnssite
    url(r'^sync_record_dnssite/(\d+)/(\d+)$',views.sync_record_dnssite,name='sync_record_dnssite'),

]