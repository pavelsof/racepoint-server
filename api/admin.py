from django.contrib import admin

from api.models import *


admin.site.register(Race)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Point)
admin.site.register(LogEvent)
admin.site.register(AuthToken)

