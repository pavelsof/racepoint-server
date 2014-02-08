from django.contrib import admin

from racepoint.models import *


admin.site.register(Race)
admin.site.register(Point)
admin.site.register(Password)
admin.site.register(Session)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(TeamAtPoint)

