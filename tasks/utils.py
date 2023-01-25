from django.core.mail import EmailMultiAlternatives
from django.template import loader


def send_email(name, title, message, email):
    template = loader.get_template('email_template.txt')
    html = loader.get_template('email_template.html')
    context = {'title': title, 'message': message, "name": name}
    text_content = template.render(context)
    email = EmailMultiAlternatives("Task assigned", text_content, to=[email])
    email.attach_alternative(html.render(context), "text/html")
    email.send()