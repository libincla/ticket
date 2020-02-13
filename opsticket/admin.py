from django.contrib import admin
from .models import Ticket, Comment, Owner
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'priority', 'assign_to',
    'status', 'owner', 'created_time','description', 
    )
    fields = ('title', 'content','priority', 'assign_to', 'owner', 'description')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content','created_time', 'owner', 'ticket')
    fields = ('title', 'content','owner', 'ticket')

@admin.register(Owner)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active')
