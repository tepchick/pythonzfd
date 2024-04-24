from django.urls import path
from django_app import views
from django_app import consumers

urlpatterns = [
    path("", views.home, name="home"),
    path("rooms", views.rooms, name="rooms"),
    path("room", views.room, name="room"),
    path("chat/<id>", views.chat, name="chat"),
    path("sing-up", views.sign_up, name="sign-up"),
    path("sing-in", views.sign_in, name="sign-in"),
    path("sing-out", views.sign_out, name="sign-out"),
    path("search/", views.search, name="search"),
    path("form", views.form, name="form"),
    path("products/p<id>", views.product, name="product"),
    path("profile/profile<id>", views.profile, name="profile"),
    path("products/qr-code/p<id>", views.qr_code, name="qr-code"),
]

websocket_urlpatterns = [
    path("ws/chat/<room_name>", consumers.ChatConsumer.as_asgi()),
]
