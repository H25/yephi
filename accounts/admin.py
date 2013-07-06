from django.contrib import admin
from accounts.models import UserProfile, Relationship, RelationshipType

admin.site.register(UserProfile)
admin.site.register(Relationship)
admin.site.register(RelationshipType)