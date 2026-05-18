from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SendEmailSerializer(serializers.Serializer):
    to = serializers.ListField(child=serializers.EmailField(), min_length=1)
    subject = serializers.CharField()
    body = serializers.CharField()
    context = serializers.DictField(required=False, default=dict)

    def validate_to(self, value):
        found = set(User.objects.filter(email__in=value).values_list('email', flat=True))
        missing = [email for email in value if email not in found]
        if missing:
            raise serializers.ValidationError(
                f"Email(s) not registered: {', '.join(missing)}"
            )
        return value
