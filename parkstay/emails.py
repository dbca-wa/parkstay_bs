from io import BytesIO
from django.conf import settings
from parkstay import pdf
from ledger.payments.pdf import create_invoice_pdf_bytes
from ledger.payments.models import Invoice
from ledger.emails.emails import EmailBase
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.core.mail import EmailMessage, EmailMultiAlternatives

from confy import env
import hashlib
import datetime
default_campground_email = settings.EMAIL_FROM


class TemplateEmailBase(EmailBase):
    subject = ''
    html_template = 'ps/email/base_email.html'
    # txt_template can be None, in this case a 'tag-stripped' version of the html will be sent. (see send)
    txt_template = 'ps/email/base_email.txt'


def send_booking_invoice(booking):
    email_obj = TemplateEmailBase()
    email_obj.subject = 'Your booking invoice for {}'.format(booking.campground.name)
    email_obj.html_template = 'ps/email/invoice.html'
    email_obj.txt_template = 'ps/email/invoice.txt'

    email = booking.customer.email

    context = {
        'booking': booking
    }
    filename = 'invoice-{}({}-{}).pdf'.format(booking.campground.name, booking.arrival, booking.departure)
    references = [b.invoice_reference for b in booking.invoices.all()]
    invoice = Invoice.objects.filter(reference__in=references).order_by('-created')[0]

    invoice_pdf = create_invoice_pdf_bytes(filename, invoice)

    campground_email = booking.campground.email if booking.campground.email else default_campground_email
    email_obj.send([email], from_address=default_campground_email, reply_to=campground_email, context=context, attachments=[(filename, invoice_pdf, 'application/pdf')])


def send_booking_confirmation(booking, request):
    email_obj = TemplateEmailBase()
    email_obj.subject = 'Your booking {} at {} is confirmed'.format(booking.confirmation_number, booking.campground.name)
    email_obj.html_template = 'ps/email/confirmation.html'
    email_obj.txt_template = 'ps/email/confirmation.txt'

    email = booking.customer.email

    cc = None
    bcc = [default_campground_email]

    campground_email = booking.campground.email if booking.campground.email else default_campground_email
    if campground_email != default_campground_email:
        cc = [campground_email]

    my_bookings_url = request.build_absolute_uri('/mybookings/')
    booking_availability = request.build_absolute_uri('/availability/?site_id={}'.format(booking.campground.id))
    unpaid_vehicle = False
    mobile_number = booking.customer.mobile_number
    booking_number = booking.details.get('phone', None)
    phone_number = booking.customer.phone_number
    tel = None
    if booking_number:
        tel = booking_number
    elif mobile_number:
        tel = mobile_number
    else:
        tel = phone_number
    tel = tel if tel else ''

    for v in booking.vehicle_payment_status:
        if v.get('Paid') == 'No':
            unpaid_vehicle = True
            break

    additional_info = booking.campground.additional_info if booking.campground.additional_info else ''

    context = {
        'booking': booking,
        'phone_number': tel,
        'campground_email': campground_email,
        'my_bookings': my_bookings_url,
        'availability': booking_availability,
        'unpaid_vehicle': unpaid_vehicle,
        'additional_info': additional_info
    }

    att = BytesIO()
    pdf.create_confirmation(att, booking)
    att.seek(0) 
    covidfile = None
    #with open(settings.BASE_DIR+"/parkstay/static/parkstay/pdf/parkstay-covid.pdf") as opened:
    #     covidfile = opened.read()
    #email_obj.send([email], from_address=default_campground_email, reply_to=campground_email, context=context, cc=cc, bcc=bcc, attachments=[('confirmation-PS{}.pdf'.format(booking.id), att.read(), 'application/pdf'), ('covid-PS{}.pdf'.format(booking.id), covidfile, 'application/pdf')])
    email_obj.send([email], from_address=default_campground_email, reply_to=campground_email, context=context, cc=cc, bcc=bcc, attachments=[('confirmation-PS{}.pdf'.format(booking.id), att.read(), 'application/pdf')]

    booking.confirmation_sent = True
    booking.save()


def send_booking_cancelation(booking, request):
    email_obj = TemplateEmailBase()
    email_obj.subject = 'Cancelled: your booking {} at {}'.format(booking.confirmation_number, booking.campground.name)
    email_obj.html_template = 'ps/email/cancel.html'
    email_obj.txt_template = 'ps/email/cancel.txt'

    email = booking.customer.email

    bcc = [default_campground_email]

    campground_email = booking.campground.email if booking.campground.email else default_campground_email
    my_bookings_url = '{}/mybookings/'.format(settings.PARKSTAY_EXTERNAL_URL)
    context = {
        'booking': booking,
        'my_bookings': my_bookings_url,
        'campground_email': campground_email
    }

    email_obj.send([email], from_address=default_campground_email, reply_to=campground_email, cc=[campground_email], bcc=bcc, context=context)


def send_booking_lapse(booking):
    email_obj = TemplateEmailBase()
    email_obj.subject = 'Your booking for {} has expired'.format(booking.campground.name)
    email_obj.html_template = 'ps/email/lapse.html'
    email_obj.txt_template = 'ps/email/lapse.txt'

    email = booking.customer.email
    campground_email = booking.campground.email if booking.campground.email else default_campground_email

    context = {
        'booking': booking,
        'settings': settings,
    }
    email_obj.send([email], from_address=default_campground_email, reply_to=campground_email, context=context)


def email_log(line):
     dt = datetime.datetime.now()
     f= open(settings.BASE_DIR+"/logs/email.log","a+")
     f.write(str(dt.strftime('%Y-%m-%d %H:%M:%S'))+': '+line+"\r\n")
     f.close()

def sendHtmlEmail(to,subject,context,template,cc,bcc,from_email,template_group,attachments=None):
    print ("start -- sendHtmlEmail")
    email_delivery = env('EMAIL_DELIVERY', 'off')
    override_email = env('OVERRIDE_EMAIL', None)
    context['default_url'] = env('DEFAULT_HOST', '')
    context['default_url_internal'] = env('DEFAULT_URL_INTERNAL', '')
    log_hash = int(hashlib.sha1(str(datetime.datetime.now()).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    email_log(str(log_hash)+' '+subject+":"+str(to)+":"+template_group)
    if email_delivery != 'on':
        print ("EMAIL DELIVERY IS OFF NO EMAIL SENT -- email.py ")
        return False
    if template is None:
        raise ValidationError('Invalid Template')
    if to is None:
        raise ValidationError('Invalid Email')
    if subject is None:
        raise ValidationError('Invalid Subject')

    if from_email is None:
        if settings.DEFAULT_FROM_EMAIL:
            from_email = settings.DEFAULT_FROM_EMAIL
        else:
            from_email = 'no-reply@dbca.wa.gov.au'

    context['version'] = settings.VERSION_NO
    # Custom Email Body Template
    context['body'] = get_template(template).render(Context(context))
    # Main Email Template Style ( body template is populated in the center
    if template_group == 'system-oim':
        main_template = get_template('ps/email/base_email-oim.html').render(Context(context))
    else:
        main_template = get_template('ps/email/base_email2.html').render(Context(context))

    reply_to=None

    if attachments is None:
        attachments = []
    # Convert Documents to (filename, content, mime) attachment
    _attachments = []
    for attachment in attachments:
        if isinstance(attachment, Document):
             filename = str(attachment)
             content = attachment.file.read()
             mime = mimetypes.guess_type(attachment.filename)[0]
             _attachments.append((filename, content, mime))
        else:
             _attachments.append(attachment)


    if override_email is not None:
        to = override_email.split(",")
        if cc:
            cc = override_email.split(",")
        if bcc:
            bcc = override_email.split(",")

    if len(to) > 1:
        msg = EmailMultiAlternatives(subject, "Please open with a compatible html email client.", from_email=from_email, to=to, attachments=_attachments, cc=cc, bcc=bcc, reply_to=reply_to)
        msg.attach_alternative(main_template, 'text/html')

        #msg = EmailMessage(subject, main_template, to=[to_email],cc=cc, from_email=from_email)
        #msg.content_subtype = 'html'
        #if attachment1:
        #    for a in attachment1:
        #        msg.attach(a)
        try:
             email_log(str(log_hash)+' '+subject)
             msg.send()
             email_log(str(log_hash)+' Successfully sent to mail gateway')
        except Exception as e:
                email_log(str(log_hash)+' Error Sending - '+str(e))

    else:
          msg = EmailMultiAlternatives(subject, "Please open with a compatible html email client.", from_email=from_email, to=to, attachments=_attachments, cc=cc, bcc=bcc, reply_to=reply_to)
          msg.attach_alternative(main_template, 'text/html')

          #msg = EmailMessage(subject, main_template, to=to,cc=cc, from_email=from_email)
          #msg.content_subtype = 'html'
          #if attachment1:
          #    for a in attachment1:
          #        msg.attach(a)
          try:
               email_log(str(log_hash)+' '+subject)
               msg.send()
               email_log(str(log_hash)+' Successfully sent to mail gateway')
          except Exception as e:
               email_log(str(log_hash)+' Error Sending - '+str(e))


    return True


