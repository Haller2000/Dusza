from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Player
from .forms import PlayerRegistrationForm, PlayerLoginForm
from django.contrib.auth import login, authenticate, logout as auth_logout

def role_selection(request):
    """Főoldal - szerepkör kiválasztása"""
    if request.user.is_authenticated:
        # Ha már be van jelentkezve, átirányítjuk a megfelelő oldalra
        if request.user.role == 'gamemaster':
            return redirect('cards:card-list')
        else:
            return redirect('game:game-home')
    return render(request, 'users/role_selection.html')

def register(request):
    """Regisztráció"""
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Sikeres regisztráció! Üdvözöllek, {user.email}!')

            if user.role == 'gamemaster':
                return redirect('cards:card-list')
            else:
                return redirect('game:game-home')
    else:
        form = PlayerRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Bejelentkezés"""
    if request.method == 'POST':
        form = PlayerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            
            # Felhasználó hitelesítése
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                # Szerepkör ellenőrzése
                if user.role != role:
                    messages.error(request, 'Hibás szerepkör!')
                    return render(request, 'users/login.html', {'form': form})
                
                login(request, user)
                messages.success(request, f'Sikeres bejelentkezés! Üdvözöllek, {user.email}!')
                
                # Szerepkörtől függő átirányítás
                if user.role == 'gamemaster':
                    return redirect('cards:card-list')
                else:
                    return redirect('game:game-home')
            else:
                messages.error(request, 'Hibás email vagy jelszó!')
    else:
        form = PlayerLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout(request):
    """Kijelentkezés"""
    auth_logout(request)
    messages.info(request, 'Sikeresen kijelentkeztél.')
    return redirect('users:role-selection')


def player_login(request):
    if request.method == 'POST':
        print(request.POST)
        player_name = request.POST.get('player_name', '').strip()
        
        if not player_name:
            messages.error(request, 'Add meg a neved!')
            return render(request, 'users/player_login.html')
        
        # Játékos létrehozása vagy lekérése
        player, created = Player.objects.get_or_create(
            name=player_name,
            defaults={'role': 'player'}
        )
        
        # Session beállítása
        request.session['player_id'] = player.id
        request.session['player_name'] = player.name
        request.session['player_role'] = player.role
        request.session['is_authenticated'] = True
        
        messages.success(request, f'Üdvözöllek, {player_name}!')
        return redirect('users:role-selection')
    
    return render(request, 'users/player_login.html')

def gamemaster_login(request):


    if request.method == 'POST':
        print(request.POST)
        player_name = request.POST.get('player_name', '').strip()

        
        if not player_name:
            messages.error(request, 'Add meg a neved!')
            return render(request, 'users/gamemaster_login.html')

        player, created = Player.objects.get_or_create(
            name=player_name,
            defaults={'role': 'gamemaster'}
        )
        
        if not created and player.role != 'gamemaster':
            player.role = 'gamemaster'
            player.save()
        
        request.session['player_id'] = player.id
        request.session['player_name'] = player.name
        request.session['player_role'] = 'gamemaster'
        request.session['is_authenticated'] = True
        
        messages.success(request, f'Üdvözöllek, {player_name} (Játékmester)!')
        return redirect('users:role-selection')
    
    return render(request, 'users/gamemaster_login.html')
 
def logout(request):
    request.session.flush()
    messages.info(request, 'Sikeresen kijelentkeztél.')
    return redirect('users:role-selection')