from django import template
from django.contrib.auth.models import User
from django_app import models

register = template.Library()


@register.simple_tag(takes_context=True)
def check_access(context, action_slug=""):
    try:
        user = context["request"].user
        action = models.Action.objects.get(slug=action_slug)
        intersections = models.GroupExtend.objects.filter(users=user, actions=action)
        if len(intersections) > 0:
            return True
        return False
    except Exception:
        return False
