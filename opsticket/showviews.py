from django.shortcuts import render, reverse, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from opsticket.models import Ticket, Owner, Comment

import datetime


@login_required
def showview(request):
    print(1, request.user.username)
    user = get_object_or_404(Owner, username=request.user.username)

    ticketlist = Ticket.objects.filter(owner=user)
    # paginator = Paginator(ticketlist, 3)
    # page = request.GET.get('page')
    # try:
    #     ticket_list = paginator.page(page)
    # except PageNotAnInteger:
    #     ticket_list = paginator.page(1)
    # except (EmptyPage, InvalidPage):
    #     ticket_list = paginator.page(paginator.num_pages)
        
    context = {}
    context.update({
        'user': user,
        # 'ticketlist': ticketlist,
        'ticketlist': ticketlist,
    })
    # return render(request, 'tickets/s.html', context=context)
    return render(request, 'tickets/tables.html', context=context)

@login_required
def sendTome(request):
    
    user = get_object_or_404(Owner, username=request.user.username)
    try:
        ass_ticket = Ticket.objects.filter(assign_to=request.user.username)
    except:
        return HttpResponseNotFound(content=b'not such a user')
    
    # ticketlist = Ticket.objects.filter(owner=user)
    # paginator = Paginator(ticketlist, 3)
    # page = request.GET.get('page')
    # try:
    #     ticket_list = paginator.page(page)
    # except PageNotAnInteger:
    #     ticket_list = paginator.page(1)
    # except (EmptyPage, InvalidPage):
    #     ticket_list = paginator.page(paginator.num_pages)
    context = {}
    context.update({
        'user': user,
        # 'ticketlist': ticketlist,
        'ticketlist': ass_ticket,
    })
    # return render(request, 'tickets/s.html', context=context)
    return render(request, 'tickets/rtables.html', context=context)

@login_required
def detailview(request, ticket_id=None):
    # ticket = Ticket.objects
    #首先要在querystring中找到这个user_id
    if request.method == "GET":
        try:
            uid = int(request.GET.get('user_id'))
        except:
            return HttpResponseNotFound(content='need userid')
        #确保user_id一定要传入一个类似int的类型
        if uid == None or isinstance(uid, int) != True:
            return HttpResponseNotFound(content='need user_id')
        
        #再次判断user_id是否在数据库存在以及是否跟当前登录的用户一致
        try:
            former_user = get_object_or_404(Owner, pk=uid)
        except:
            return HttpResponseNotFound(content='user id does not exist')
        #判断user_id与当前登录用户是否一致
        if former_user.id != request.user.id:
            return HttpResponseNotAllowed(content='not same person', permitted_methods=['GET', 'POST', 'OPTIONS',])
        
        # ticket = get_object_or_404(Ticket, pk=ticket_id)
        try:
            # comment = Comment.objects.filter(Q(owner__pk=uid) & Q(ticket__pk=ticket_id))
            comment = Comment.objects.filter(ticket__pk=ticket_id)
        except:
            comment = None
        # ticket = Ticket.objects.filter(owner__pk=former_user.id)
        try:
            # ticket = Ticket.objects.filter(Q(owner__pk=former_user.id) & Q(pk=ticket_id))
            ticket = Ticket.objects.filter(pk=ticket_id)
        except:
            ticket = None
        context = {}
        context.update({
            'ticket': ticket,
            'comment' : comment,
        })
        return render(request, 'tickets/ticket.html', context=context)  
    elif request.method == "POST":
        comment_content = request.POST.get('comment')
        comment_user = request.user
        uid = request.user.pk
        if comment_content:
            c = Comment()
            t = get_object_or_404(Ticket, pk=ticket_id)
            c.ticket = t
            c.title = 'this is just a comment'
            c.content = comment_content
            c.owner = comment_user
            c.created_time = datetime.datetime.now()
            try:
                c.save()
            except Exception as e:
                print(e)
        
        # return  HttpResponseRedirect(reverse('ticket-detail', kwargs={'ticket_id': ticket_id}))
        # return  HttpResponseRedirect(reverse('ticket-detail:ticket_id', args=))
        return  HttpResponseRedirect('/t/%s/?user_id=%s' % (str(ticket_id), str(uid)))
                

@login_required
def user_detail(request):
    try:
        user = Owner.objects.filter(username=request.user.username)
        
        user = user[0]
    except Exception as e:
        print(e)
        return HttpResponseNotFound(content=b'user not found')

    return render(request, 'tickets/usertail.html', locals())
        
        
        # # if form.is_valid():
        #     comment_instance = form.save(commit=False)
        #     # cd = commentform.cleaned_data
        #     try:
        #         comment_instance.ticket__pk = int(ticket_id)
        #         comment_instance.owner = request.user
        #         comment_instance.save()
        #         # return HttpResponseRedirect(reverse('ticket-detail', kwargs={'ticket_id': ticket_id}))
        #         context.update({'form': form})
        #         return render(request, 'tickets/ticket.html', context=context)
            
        #     except:
        #         return HttpResponseNotAllowed(permitted_methods=['POST', 'GET'])
                

    