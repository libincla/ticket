"""ticket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from opsticket.views import TicketList, TicketDetail, TicketCreate
from opsticket.ownerviews import OwnerView, OwnerTicketView
from opsticket.functionviews import ticketAssign,  display_meta, create_ticket, update_ticket, index, testy
from opsticket.loginviews import loginview, registerview, setpasswordview, logoutview, findPassword
from opsticket.showviews import showview, detailview, sendTome, user_detail

urlpatterns = [
    # url(r'^tlist/$', TicketList.as_view(), name='ticket-list'),
    # url(r'^t/(?P<pk>\d+)/$', TicketDetail.as_view(), name='ticket-detail'),
    url(r'^t/(?P<ticket_id>\d+)/$', detailview, name='ticket-detail'),
    # url(r'^t/add/$', TicketCreate.as_view(), name='ticket-create'),
    # url(r'^t/add/$', CreateTicket),
    url(r'^t/add/$',create_ticket, name='create-ticket'),
    url(r'^s/$',showview,name='showlist'),
    url(r'^r/$', sendTome, name='sendTome'),
    url(r'^t/(?P<ticket_id>\d+)/update/$', update_ticket, name='update-ticket'),
    url(r'^user/(?P<ownerid>\d+)/tickets', OwnerTicketView.as_view(), name='owner-ticket' ),
    # url(r'^user/(?P<pk>\d+)/assign/(?P<assignid>\d+)',OwnerTicketAssign.as_view(), name='ownerassign'),
    url(r'^t/(?P<ticket_id>\d+)/assign/(?P<assign_id>\d+)', ticketAssign),
    url(r'^e/$',testy),
    url(r'^user/(?P<pk>\d+)/$', OwnerView.as_view(), name='owner-detail' ),
    url(r'^admin/', admin.site.urls),
    url(r'^meta/', display_meta),
    url(r'^login/',loginview, name='login'),
    url(r'^logout/$', logoutview, name='logout'),
    url(r'^$', index, name='index'),
    url(r'^register/', registerview, name='register'),
    url(r'^setpassword/', setpasswordview, name='setpassword'),
    url(r'^findpassword/$', findPassword, name='findPassword'),
    url(r'^userdetail/$', user_detail, name='user_detail'),
    # url(r'^', include('django.contrib.auth.urls')),
    
    # url(r'^search-form/',search_form),
    # url(r'^search/', search),

]
