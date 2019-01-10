# coding: utf-8
import json
import logging

from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.text import mark_safe
from django.utils.translation import ugettext_lazy as _

from postman.forms import EmailForm
from postman.models import Recipient, Information

logger = logging.getLogger('postman')


def __message_sent(request):
    information = Information.get_or_default(
        name='successfully_sent_message',
        default_title=_('Tank you for your message'),
        default_text=_('We will contact you as soon as possible.\n\nKind regards')
    )

    form = mark_safe(render(request, 'postman/partials/success.html', {
        'information': information,
    }).content.decode('utf-8'))

    return HttpResponse(json.dumps({
        'success': True,
        'form': form,
    }), content_type='application/json')


def __message_already_sent(request):
    information = Information.get_or_default(
        name='already_sent_message',
        default_title=_('You already sent an email right now'),
        default_text=_('We will process your request and contact you as soon as possible.\n\nKind regards')
    )

    form = mark_safe(render(request, 'postman/partials/alreadySent.html', {
        'information': information
    }).content.decode('utf-8'))

    return HttpResponse(json.dumps({
        'alreadySent': True,
        'form': form,
    }), content_type='application/json')


def __message_sent_error(request, form, subject=''):
    if form.instance.pk:
        information = Information.get_or_default(
            name='error_sending_message_but_saved',
            default_title=_('An error occurred while sending your message'),
            default_text=_('Please try again later or send us an email.')
        )
    else:
        information = Information.get_or_default(
            name='error_sending_message',
            default_title=_('An error occurred while sending your message'),
            default_text=_('Please try again later or send us an email.')
        )

    alternative_contact = Information.get_or_default(
        name='alternative_contact',
        default_title=_('Send an email'),
        default_text=_('Alternatively you can send your message directly to')
    )

    recipient = Recipient.objects.filter(is_default=True).first()
    error = mark_safe(render(request, 'postman/partials/error.html', {
        'information': information,
        'alternativeContact': alternative_contact,
        'recipient': recipient,
        'subject': subject,
        'message': form.instance.message,
    }).content.decode('utf-8'))

    return HttpResponse(json.dumps({
        'errors': True,
        'form': error,
    }), content_type='application/json')


def __form_error(request, form):
    form = mark_safe(render(request, 'postman/tags/postmanForm.html', {
        'form': form,
    }).content.decode('utf-8'))

    return HttpResponse(json.dumps({
        'formErrors': True,
        'form': form,
    }), content_type='application/json')


def send_message(request, subject, message, send_to):
    if not settings.LOCAL:
        mail_from = settings.EMAIL_FROM
        msg = EmailMessage(subject, message, mail_from, send_to)
        msg.content_subtype = "html"

        try:
            msg.send()
        except Exception as e:
            logger.error("Error sending email: %s" % str(e))
            return False

        return True

    logger.info("The message was not sent because we are on a local server.")
    return False


def process_message(request):
    logger.debug("Try send message")
    form = EmailForm()

    try:
        if request.session.get('mailSent', False):
            logger.debug("A message has already been sent")
            return __message_already_sent(request)

        if request.method == 'POST':
            subject = Information.get_or_default(
                name='email_subject',
                default_title=_('The email subject'),
                default_text=_('Request from truthordare'),
            )

            form = EmailForm(request.POST)

            if form.is_valid():
                logger.debug("Form is valid")
                send_to = [r.email for r in Recipient.objects.all()]

                company = form.cleaned_data['company']

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']

                email = form.cleaned_data['email']
                telephone = form.cleaned_data['telephone']

                user_message = form.cleaned_data['message']

                privacy_accepted = form.cleaned_data['privacy_accepted']

                message = mark_safe(render(request, 'postman/partials/mail.html', {
                    'company': company,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'telephone': telephone,
                    'subject': subject,
                    'message': user_message,
                    'privacy_accepted': privacy_accepted,
                }).content.decode('utf-8'))

                try:
                    form.save()
                    logger.info("Message was stored")
                except Exception as e:
                    logger.error("Unable to save message: %s" % str(e))

                if send_message(request, subject, message, send_to):
                    request.session.set_expiry(300)
                    request.session['mailSent'] = True

                    try:
                        form.instance.sent = True
                        form.instance.save()
                    except Exception as e:
                        logger.error("Unable to update message state to sent: %s" % str(e))

                    return __message_sent(request)

                else:
                    logger.error("Message not sent: %s" % request)
                    return __message_sent_error(request, form, subject)

            else:
                return __form_error(request, form)

    except Exception as e:
        logger.error("Error while sending message: %s" % str(e))
        return __message_sent_error(request, form)

    return render(request, 'postman/postman.html', {
        'form': EmailForm(),
    })


def contact(request):
    return render(request, 'postman/postman.html', {
        'form': EmailForm(),
    })
