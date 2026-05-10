import json

from django.core.management.base import BaseCommand, CommandError

from user.email import send_plain_email, send_template_email


class Command(BaseCommand):
    help = "Send an email via plain text or HTML template"

    def add_arguments(self, parser):
        parser.add_argument("--to", nargs="+", required=True, metavar="EMAIL", help="Recipient email address(es)")
        parser.add_argument("--subject", required=True, help="Email subject")
        parser.add_argument("--body", default="", help="Plain text body (used when --template is not provided)")
        parser.add_argument("--template", default="", metavar="TEMPLATE_NAME", help="Template path relative to templates dir (e.g. emails/welcome.html)")
        parser.add_argument("--context", default="{}", help="JSON string of template context variables")

    def handle(self, *args, **options):
        to = options["to"]
        subject = options["subject"]
        body = options["body"]
        template_name = options["template"]

        try:
            context = json.loads(options["context"])
        except json.JSONDecodeError as e:
            raise CommandError(f"Invalid JSON in --context: {e}")

        if not body and not template_name:
            raise CommandError("Provide either --body or --template.")

        try:
            if template_name:
                send_template_email(to=to, subject=subject, template_name=template_name, context={**context, "body": body})
            else:
                send_plain_email(to=to, subject=subject, body=body)
        except Exception as e:
            raise CommandError(f"Failed to send email: {e}")

        self.stdout.write(self.style.SUCCESS(f"Email sent to: {', '.join(to)}"))
