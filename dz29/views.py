from django.shortcuts import render, redirect
from django_app import models
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.urls import reverse
import qrcode
from io import BytesIO


def paginator(request, objs):
    selected_page = request.GET.get(key="page", default=1)
    page_objs = Paginator(object_list=objs, per_page=3)
    page_obj = page_objs.page(number=selected_page)
    return page_obj


def home(request):
    products = models.Product.objects.all().filter(status=True)
    sort = request.GET.get("sort", None)
    if sort:
        products = models.Product.objects.order_by(sort)
    return render(
        request,
        "home.html",
        {"products": paginator(request, products)},
    )


def rooms(request):
    rooms = models.Room.objects.filter(users=request.user)
    return render(request, "rooms.html", {"rooms": rooms})


def room(request):
    user = request.user
    admin = models.User.objects.get(username="admin")
    room = models.Room.objects.filter(users=user).first()
    if not room:
        room = models.Room.objects.create(name=f"Chat {user.id}", slug=f"c{user.id}")
        room.users.set([user, admin])
    return redirect("chat", id=room.id)


@login_required
def chat(request, id):
    if request.method == "GET":
        messages = models.Message.objects.filter(room=id)
        return render(request, "chat.html", {"messages": messages})
    else:
        room = models.Room.objects.get(id=id)
        content = request.POST.get("message", None)
        if content:
            message = models.Message.objects.create(
                user=request.user, room=room, content=content
            )
        return redirect("chat", id=id)


def search(request):
    if request.method == "GET":
        search = request.GET.get("search", "")
        products = models.Product.objects.all().filter(
            status=True, name__icontains=search
        )
        return render(
            request,
            "home.html",
            {"products": paginator(request, products), "search": search},
        )


def product(request, id):
    product = models.Product.objects.get(id=id)
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        price = float(request.POST["price"].replace(",", "."))
        image = request.FILES.get("image", None)
        if product.name != name:
            product.name = name
        if product.description != description:
            product.description = description
        if product.price != price:
            product.price = price
        if image:
            product.image = image
        product.save()
    return render(request, "product.html", {"product": product})


def qr_code(request, id):
    product = models.Product.objects.get(id=id)
    if not product.qr_code:
        product_url = request.build_absolute_uri(reverse("product", args=[id]))
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(product_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        filename = f"qr_code_{id}.png"
        product.qr_code.save(filename, ContentFile(img_bytes.getvalue()), save=True)
        product.save()
    return render(request, "qr-code.html", {"product": product})


def profile(request, id):
    if request.method == "GET":
        return render(request, "profile.html")
    elif request.method == "POST":
        name = request.POST["name"]
        avatar = request.FILES.get("avatar", None)
        clear_avatar = True if request.POST.get("clear_avatar", None) else False
        profile = models.Profile.objects.get(id=id)
        if profile.name != name:
            profile.name = name
        if clear_avatar:
            profile.avatar = "profile/avatar/default.png"
        if avatar:
            profile.avatar = avatar
        profile.save()
        return render(request, "profile.html")


def form(request):
    if request.method == "GET":
        return render(request, "form.html")
    else:
        name = request.POST["name"]
        description = request.POST["description"]
        price = float(request.POST["price"].replace(",", "."))
        image = request.FILES["image"]
        try:
            product = models.Product.objects.create(
                name=name, description=description, price=price, image=image
            )
            status = "success"
        except Exception:
            status = "error"
        return render(request, "form.html", {"status": status})


def sign_up(request):
    if request.method == "GET":
        return render(request, "sign-up.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if not user:
            name = request.POST["name"]
            avatar = request.FILES.get("avatar", None)
            if not avatar:
                avatar = "profile/avatars/default.png"
            user = User.objects.create(
                username=username, password=make_password(password)
            )
            profile = models.Profile.objects.get(user=user)
            profile.name = name
            profile.avatar = avatar
            profile.save()
            login(request, user)
            return redirect("home")
        else:
            return render(
                request,
                "sign-up.html",
                context={"error": True},
            )


def sign_in(request):
    if request.method == "GET":
        return render(request, "sign-in.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if not user:
            return render(
                request,
                "sign-in.html",
                context={"error": True},
            )
        login(request, user)
        return redirect("home")


def sign_out(request):
    logout(request)
    return redirect(reverse("sign-in"))
