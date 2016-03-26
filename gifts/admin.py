from django.contrib import admin

# Register your models here.
from gifts.models import Gift, GiftsCharts, List, GiftsMember, CommentGift, ScoreGift

admin.site.register(Gift)
admin.site.register(GiftsCharts)
admin.site.register(List)
admin.site.register(GiftsMember)
admin.site.register(CommentGift)
admin.site.register(ScoreGift)