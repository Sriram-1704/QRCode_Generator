from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from .models import QRCode
from django.contrib.auth.decorators import login_required
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def generate_qr(request):
    if request.method == 'POST':
        upi_id = request.POST['upi_id']
        name = request.POST['name']
        amount = request.POST['amount']
        purpose = request.POST.get('purpose', '')

        upi_string = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        qr_img = qrcode.make(upi_string)

        buffer = BytesIO()
        qr_img.save(buffer)
        image_file = ContentFile(buffer.getvalue(), name=f'{name}_{amount}.png')

        QRCode.objects.create(
            user=request.user,
            upi_id=upi_id,
            name=name,
            amount=amount,
            purpose=purpose,
            image=image_file
        )

        return redirect('history')

    return render(request, 'generate_qr.html')

@login_required
def history_view(request):
    qr_list = QRCode.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'qr_list': qr_list})