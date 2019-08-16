from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Game, GamePlatform, User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import json

def index(request):
    current_games_list = Game.objects.order_by('title')
    context = {
        'current_games_list': current_games_list
    }
    return render(request, 'mangudapp/index.html', context)

def verify_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('MangudApp:index'))
    else:
        # raise Http404("Invalid user credentials!")
        return HttpResponseRedirect(reverse('MangudApp:index')+'?message=fail')

def mylogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('MangudApp:index'))

@login_required
def members(request):
    return render(request, 'mangudapp/members.html')


@login_required
def get_wish_list(request):
    data = {'wish_list':[]}
    for game in request.user.user_wishlist.all():
        data['wish_list'].append(game.text)
    return HttpResponse('ok')

@login_required
def change_password_submission(request):
    current_password = request.POST['current_password']
    password = request.POST['new_password']
    current_user = request.user
    user = authenticate(request, username=current_user, password=current_password)
    if user is not None:
        current_user.set_password=(password)
        current_user.save()
        return HttpResponseRedirect(reverse('MangudApp:members'))
    else:
        return HttpResponseRedirect(reverse('MangudApp:members'))
    
    

def login_page(request):
    return render(request, 'mangudapp/login.html')    

def create_user(request):
    return render(request, 'mangudapp/create_user.html')


def create_user_submission(request):
    print(request.POST)
    m_username = request.POST['username']
    m_email = request.POST['member_email']
    m_birthday = request.POST['birthday']
    m_password = request.POST['password']
    
    a_member = User.objects.create_user(m_username,m_email,m_password)
    group = Group.objects.get(name='Normal')
    a_member.groups.add(group)
    a_member.save()
    login(request,a_member)
    return HttpResponseRedirect(reverse('MangudApp:members'))

def game_details(request, games_id):
    current_game = get_object_or_404(Game, pk=games_id)
    context = {
        'current_game': current_game
    }
    print(current_game)
    return render(request, 'mangudapp/a_game.html', context)


def add_to_wishlist(request):
    current_games_list = Game.objects.all()
    context = {
        'current_games_list': current_games_list
    }
    data = json.loads(request.body)
    gameid = data['gameid']
    
    for i in range(len(context['current_games_list'])):
        temp_game = context['current_games_list'][i]
        if(gameid == temp_game.id):
            print(temp_game)
            request.user.saved_games.add(temp_game)
    
    return render(request, 'mangudapp/members.html')

def remove_from_wishlist(request):
    current_user = request.user
    game_ids = request.POST.getlist('gid')
    for game_id in game_ids:
        print(f"Game id: {game_id}")
        game = Game.objects.get(id=game_id)
        current_user.saved_games.remove(game)
    current_user.save()
    return HttpResponseRedirect(reverse('MangudApp:members'))


def edit_user_submission(request):
    # u_name = request.POST['username']
    f_name = request.POST['first_name']
    l_name = request.POST['last_name']
    newsletter = request.POST['newsletter']
    
    current_user = request.user
    current_user.first_name = f_name
    current_user.last_name = l_name
    if (newsletter =="true"):
        current_user.on_newsletter = True
        current_user.save()
    else:
        current_user.on_newletter = False
        current_user.save()
    if(current_user.on_newsletter):
        send_mail(
        'Welcome to the newsletter!',
        'Thank you for signing up.',
        'mfd2970@gmail.com',
        [current_user.email],
        fail_silently=False,
    )
    return HttpResponseRedirect(reverse('MangudApp:members'))