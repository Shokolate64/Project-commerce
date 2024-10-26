from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')

@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'starting_bid', 'active', 'created_by', 'created_at')    

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction','bidder', 'bid_amount', 'bid_time')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('auction', 'commenter', 'comment_text', 'comment_time')