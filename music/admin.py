from django.contrib import admin
from .models import Song, Album, Download, Genre
from .models import Song, PlayHistory
from .models import Advertisement

admin.site.register(Song)
admin.site.register(PlayHistory)
admin.site.register(Album)
admin.site.register(Download)
admin.site.register(Genre)
admin.site.register(Advertisement)