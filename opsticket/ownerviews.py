from .models import Owner, Ticket, Comment
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from .views import TicketList



class OwnerView(DetailView):
    model = Owner
    template_name = 'tickets/owner-detail.html'
    
# class OwnerTicketView(ListView):
class OwnerTicketView(TicketList):
    template_name = 'tickets/owner-tickets.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     owner_id = self.kwargs.get('ownerid')
    #     owner = get_object_or_404(Owner, pk=owner_id)
    #     self.owner_id = owner_id
    #     context.update({
    #         'owner' : owner_id,
    #     })
    #     print(context)
    #     return context

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.kwargs)
        owner_id = self.kwargs.get('ownerid')
        return queryset.filter(owner_id=owner_id)
        #重写queryset,根据用户过滤

# class OwnerTicketAssign(DetailView):
#     #已完成或者中止的工单不予以指派
#     queryset = Ticket.objects.filter(status=1)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         assign_id = self.kwargs.get('assignid')
#         self.assgin_id = assign_id
#         context.update({
#             'assgin_id' : assign_id
#         })
#         return context

#     def get_object(self,queryset=None):
#         obj = super().get_object(queryset=queryset)
#         obj.owner.id = self.assgin_id
#         return obj
            



    # def get_queryset(self):




    # model = Owner
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object(queryset=Owner.objects.all())
    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['owner'] = self.object
    #     return context
        