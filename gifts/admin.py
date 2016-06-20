from django.contrib import admin

# Register your models here.
from gifts.models import Gift, List, GiftsMember, CommentGift, ScoreGift, LikesGift, LikeGiftUser

admin.site.register(Gift)
admin.site.register(List)
admin.site.register(GiftsMember)
admin.site.register(CommentGift)
admin.site.register(ScoreGift)
admin.site.register(LikesGift)
admin.site.register(LikeGiftUser)