from django import template
from django.conf import settings
from postman.forms import EmailForm

register = template.Library()


@register.inclusion_tag('postman/tags/postman_form.html')
def render_postman_form(form=None):
    return {
        'form': form if form else EmailForm()
    }


@register.inclusion_tag('postman/tags/linkLabel.html')
def privacy_link_label(label):
    privacy_url = None
    if hasattr(settings, 'EMAIL_PRIVACY_URL'):
        privacy_url = settings.EMAIL_PRIVACY_URL

    return {
        'label': label,
        'privacy_url': privacy_url,
    }
