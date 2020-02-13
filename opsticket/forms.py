from django import forms
from .models import Ticket, Comment, Owner
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    title = forms.CharField(label='评论标题')
    content = forms.CharField(label='评论内容', widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = ['title', 'content']
        
# class DateInput(forms.DateInput):
#     input_type = 'date'
    
class CreateTicketForm(forms.ModelForm):
    title = forms.CharField(label='工单标题')
    # content = forms.Textarea()
    content = forms.CharField(label='工单内容',widget=forms.Textarea)
    priority = forms.ChoiceField(label='优先级',choices=((1, '低'),(2, '中'),(3, '高')))
    assign_to = forms.CharField(label='指派给谁',help_text='这里不要填字符串,填一个数字')
    expired_time = forms.DateTimeField(label='期望时间',  widget=forms.DateInput(attrs={'type':'date'},format="yyyy-MM-dd HH:mm:ss"))
    # expired_time = forms.DateTimeField(label='期望时间')
    # description = forms.Textarea()
    description = forms.CharField(label='工单描述',widget=forms.Textarea)

    class Meta:
        model = Ticket
        fields = ['title', 'content', 'priority', 'assign_to', 'expired_time', 'description']
        # widgets = {
        #     'expired_time' : DateInput()
        # }

class UpdateForm(forms.ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['title', 'content', 'priority', 'expired_time', 'description']


class RecieveTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['priority','status', 'expired_time']
        
class  CreateUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Owner
        fields = UserCreationForm.Meta.fields + ('group',)
        

        