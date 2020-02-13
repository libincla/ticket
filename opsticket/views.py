from django.http  import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from .models import Ticket, Owner, Comment

# Create your views here.

class TicketList(ListView):
    # model = Ticket
    template_name = 'tickets/ticketlist.html'
    context_object_name = 'ticket_list'
    queryset = Ticket.objects.filter(status=0)


class TicketDetail(SingleObjectMixin,ListView):
# class TicketDetail(ListView):
    template_name = 'tickets/ticket.html'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            print(self.request.user)
        else:
            print('aha!')
        self.object = self.get_object(queryset=Ticket.objects.all().select_related('owner'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = self.object
        return context
    def get_queryset(self):
        # self.owner = get_object_or_404(Owner, username=self.args[0])
        # print(self.args)
        # self.ticket = get_object_or_404(Ticket, pk=self.args[0])
        # return Comment.objects.filter(ticket=self.ticket)
        return self.object.comment.all()



class AjaxableResponseMixin(object):
    '''
     Mixin将AJAX支持添加到表单。
     必须与基于对象的FormView一起使用（例如CreateView）
    '''
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class TicketCreate(AjaxableResponseMixin, CreateView):
    model = Ticket
    fields = ['title', 'content', 'priority', 'assign_to', 'owner','expired_time' ]
    template_name = 'tickets/ticket_create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
