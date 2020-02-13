from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponseNotAllowed, HttpResponseNotFound
from .models import Ticket, Comment, Owner
from .forms import CreateTicketForm, UpdateForm, RecieveTicketForm, CommentForm
from django.contrib.auth.decorators import login_required, permission_required
import datetime

@login_required
def index(request):
    username = request.user.username
    return render(request, 'tickets/index.html', locals())
    # return render(request, 'demo/index.html', locals())


def ticketAssign(self, ticket_id=None, assign_id=None):
    #取得工单实例
    if ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
    else:
        ticket_id = 1
    #验证assign_id为一个合格的uid
    if assign_id:
        # owner = Owner.objects.filter(id=int(assign_id))
        # oid = Owner.objects.get(id=int(assign_id))
        oid = get_object_or_404(Owner, id=int(assign_id))
        

    ticket.owner = oid
    ticket.save()

    return HttpResponseRedirect(reverse('ticket-detail', kwargs={'pk': ticket_id}))


@login_required
@permission_required(perm='opsticket.visit_Ticket')
def display_meta(request):
    values = request.META.items()
    # values.sort
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

# def CreateTicket(request, ticket_id=None):
#     if request.method == "POST":
#         form = CreateTicketForm(request.POST)
#         if form.is_valid():
#             ticket_db = form.save(commit=False)
#             cd = form.cleaned_data
#             # oid = Owner.objects.get(username=cd['assign_to']).id
#             try:
#                 user = Owner.objects.get(username=cd['assign_to'])
#                 ticket_db.owner = user
#                 ticket_db.save()
#                 return HttpResponseRedirect(reverse('ticket-list', kwargs=''))
#             except:
                
#                 return HttpResponseServerError('user not found')

#     else:
#         if ticket_id:
#             form = CreateTicketForm(instance=Ticket.objects.get(id=ticket_id))
#         else:
#             form = CreateTicketForm()
#             # CreateTicketForm()
#     return render(request, 'tickets/create_form.html', {'form': form})
 
#增加一个工单表单 
# @permission_required(perm='opsticket.add_Ticket')
@login_required
def create_ticket(request):
    print(request.user)
    if request.method == "GET":
        form = CreateTicketForm()
    
    elif request.method == "POST":
        form = CreateTicketForm(request.POST) 
        if form.is_valid():
            ticket_db = form.save(commit=False)
            # cd = form.cleaned_data
            # oid = Owner.objects.get(username=cd['assign_to']).id
            try:
                # user = Owner.objects.get(username=cd['assign_to'])
                ticket_db.owner = request.user
                ticket_db.belong = request.user.username
                ticket_db.save()
                # return HttpResponseRedirect(reverse('ticket-list', kwargs=''))
                return HttpResponseRedirect(reverse('showlist', kwargs=''))
            except Exception as  e:
                print(e)
                return HttpResponseNotFound(content=b'user not found')
            
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'GET'])
    return render(request, 'tickets/create_form.html', {'form': form})

@login_required
def testy(request):
    print(request.user)
    print(type(request.user))
    print(request.user.username)
    print(type(request.user.username))
    t = datetime.datetime.now()
    print(t)
    print(type(t))
    return HttpResponse(content=b'beijua!')
    

#编辑一个工单表单:
def update_ticket(request, ticket_id=None):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    uid = request.user.pk
    if request.method == "GET":
        #如果是GET请求，创建一个表单，并用当前查到的实例来填充表单
        form = RecieveTicketForm(instance=ticket)
    elif request.method == "POST":
        form = RecieveTicketForm(instance=ticket, data=request.POST)
        form.save()
        # return HttpResponseRedirect(reverse('ticket-detail', kwargs={'ticket_id': ticket_id}))
        # return HttpResponseRedirect('/t/%s/?user_id=%s' % (str(ticket_id), str(uid)))
        return HttpResponseRedirect('/r/')
    else:
        #不接受其他的HTTP方法
        return HttpResponseNotAllowed(permitted_methods=['POST', 'GET'])
    return render(request, 'tickets/create_form.html', {'form': form, 'ticket': ticket})




#删除一个工单表单:
#原理上不允许


#简单的搜索功能

# def search_form(request):
#     return render(request, 'tickets/search_form.html')

# def search(request):
#     errors = []
#     if 'q' in request.GET and request.GET['q']:
#         q = request.GET['q']
#         if not q:
#             # error = True
#             errors.append('键入一个搜索项')
#         elif len(q) < 10:
#             # error = True
#             errors.append('输入小于10个字符')
#         else:
#             ticket = Ticket.objects.filter(title__icontains=q)
#             context = {'q': q, 'ticket': ticket}
#             return render(request, 'tickets/search_res.html', context=context)
#     else:
#         # return HttpResponse('请提交一个搜索的工单标题')
#         return render(request, 'tickets/search_form.html', {'errors': errors})