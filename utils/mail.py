from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def convert_html_to_email_message(
    subject_template_name: str,
    html_email_template_name: str,
    emails_list: list | tuple,
    context: dict = None,
) -> EmailMultiAlternatives:
    """
    Converts html templates into a string, attaching them to an
    EmailMultiAlternatives object for later sending.
    """
    raw_subject = render_to_string(subject_template_name)

    subject = "".join(raw_subject.splitlines())
    message = render_to_string(html_email_template_name, context)

    return EmailMultiAlternatives(subject=subject, body=message, to=emails_list)
