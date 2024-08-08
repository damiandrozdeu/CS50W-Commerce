from django.contrib import admin
from .models import Bid, Comment, Auction, User, Category
from django.contrib.auth.admin import UserAdmin


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "title", "image","description","initial_price", "current_price", "created_date" ,"active")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "auction", "comment")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "auction", "bid")

admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Category)

