from django.shortcuts import render
from django.http import HttpResponse
import qrcode
from io import BytesIO

def qr_form(request):
    if request.method == "POST":
        upi_id = request.POST.get("upi_id")
        name = request.POST.get("name")
        amount = request.POST.get("amount")

        upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        img = qrcode.make(upi_link)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return HttpResponse(buffer.getvalue(),content_type='image/png')
    return render(request,"qr_form.html")
