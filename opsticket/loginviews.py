from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from opsticket.models import Owner
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import make_password

from .forms import CreateUserForm

import random, string

#登录
def loginview(request):
    #设置标题和另外两个URL链接
    # title = '登陆'
    # unit_2 = 'register.html'
    # unit_2_name = '立即注册'
    # unit_1 = 'setpassword.html'
    # unit_1_name = '修改密码'
    # tips = '请登录'
    title = '用户登录'
    
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if Owner.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            try:
                if user:
                    if user.is_active:
                        login(request, user)
                    return redirect('/')
                else:
                    print('用户名或者密码错误，认证没通过')
            except Exception as e:
                print('!!!')
                print(e)
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    # return render(request, 'tickets/user.html', locals())
    return render(request, 'tickets/login.html', locals())


#注册
# def registerview(request):
#     if request.method == "POST":
#         user = CreateUserForm(request.POST)

#         if user.is_valid():
#             print(user.password1)
#             print(user.password2)
#             print(user)
#             user.save()
#             tips = '注册成功'
#             user = CreateUserForm()
#         else:
#             print(user.password1)
#             print(user.password2)
#             print("!", user)
#     else:
#         user = CreateUserForm()
#     return render(request, 'tickets/register.html', locals())
def registerview(request):
    #设置标题和另外两个url链接
    title = '注册'
    # unit_2 = 'login.html'
    # unit_2_name = '立即登录'
    # unit_1 = 'setpassword.html'
    # unit_1_name = '修改密码'
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')
        
        if Owner.objects.filter(username=username):
            tips = '用户已经存在'
            # return render(request, 'tickets/user.html')
        #用户不存在
        else:            
            if Owner.objects.filter(email=email):
                tips = '您输入的邮箱已经存在,请注册其他邮箱'
                # return render(request, 'tickets/user.html')
            else:
                user = Owner.objects.create_user(username=username, password=password)
                user.save()
                #添加权限
                permission = Permission.objects.filter(codename='visit_Ticket')[0]
                user.user_permissions.add(permission)
                
                # return redirect('/login')
                return HttpResponseRedirect(reverse('login'))
            
    return render(request, 'tickets/user.html', locals())

#重置密码

def setpasswordview(request):
    #设置标题和另外两个url链接
    title = '修改密码'
    unit_2 = 'login.html'
    unit_2_name = '立即登录'
    unit_1 = 'register.html'
    unit_1_name = '立即注册'

    new_password = True
    if request.method == "POST":
        username = request.POST.get("username", "")
        old_password = request.POST.get("password", "")
        new_password = request.POST.get("new_password", "")
        if Owner.objects.filter(username=username):
            user = authenticate(username=username, password=old_password)
            user.set_password(new_password)
            user.save()
            tips = '密码修改成功'
        else:
            tips = '用户不存在'
    return render(request, 'tickets/user.html', locals())


#找回密码
def findPassword(request):
    if request.method == "POST":
        username = request.POST.get('username', 'root')
        get_mail = request.POST.get('email', '')
        database_user = Owner.objects.filter(username=username)
        
        
        #如果账号不存在，报错:
        if not database_user:
            return render(request, 'tickets/setps.html', {'user_error': "输入的用户名不存在"})
        else:
            if get_mail != database_user[0].email:
                return render(request, 'tickets/setps.html', {'email_error': "输入邮箱有误,请输入注册时的邮箱"})
            else:
                #邮箱isOk
                passwordkey = ''.join(random.sample(string.ascii_letters + string.ascii_uppercase + string.digits, 12))
                database_user[0].set_password(passwordkey)
                database_user[0].save()
                print("密码重设完成")
                
                database_user[0].email_user('密码已经重置, 新密码显示在邮件正文中', passwordkey)
                
        return  render(request, 'tickets/setps.html', {'success': "密码已经重置完成"})

    else:
        return render(request, 'tickets/setps.html')
                
            
        #否则账号存在
        
    # button = '获取验证码'
    # new_password = False
    
    # if request.method == "POST":
    #     username = request.POST.get('username', 'root')
    #     vcode = request.POST.get('vcode', '')
    #     password = request.POST.get('password', '')
    #     user = Owner.objects.filter(username=username)
    #     #如果用户不存在
    #     if not user:
    #         tips = '用户' + username + '不存在'
    #     else:
    #         if not request.session.get('vcode', ''):
    #         #ss发送验证码并将 验证码写入session
    #             button = '重置密码'
    #             tips = '验证码已经发送'
    #             new_password = True
    #             vcode = str(random.randint(10000, 99999))
    #             request.session['vcode'] = vcode
                # user[0].email_user('找回你的密码', vcode)
    #         #匹配输入的验证码是否正确
    #         elif vcode == request.session.get('vcode'):
    #             #密码加密处理并保存到数据库
    #             dj_ps = make_password(password, None, 'pbkdf2_sha256')
    #             user[0].password = dj_ps
    #             user[0].save()
    #             del  request.session['vcode']
    # return render(request, 'tickets/setps.html', locals())
                
                
            
        



#注销

def logoutview(request):
    logout(request)
    return redirect('/')
    
        
            