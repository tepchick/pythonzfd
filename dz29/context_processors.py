from django_app import models


def products_count(request):
    return {"products_count": models.Product.objects.count()}


def profile(request):
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)
    else:
        profile = None

    return {"profile": profile}
