from django.contrib import admin

from durin import models


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    # searchable fields
    exclude = ("token", "expiry")
    list_display = (
        "token",
        "client_name",
        "user",
        "created",
        "expires_in",
    )
    list_filter = ("client__name", "user")

    fieldsets = [
        (
            "API Auth Token",
            {
                "fields": ("user", "client"),
                "description": """
                    <h3>Token will be auto-generated on save.</h3>
                    <h3>Token will carry the same expiry as the
                     selected client's token TTL.</h3>
                """,
            },
        ),
    ]

    def client_name(self, obj):
        return obj.client.name

    def save_model(self, request, obj, form, change):
        return models.AuthToken.objects.create(obj.user, obj.client)


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "token_ttl")
