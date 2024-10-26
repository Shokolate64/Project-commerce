from django.contrib.auth.models import AbstractUser, User
from django.db import models

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title= models.CharField(max_length=64)
    description= models.TextField()
    starting_bid= models.DecimalField(max_digits=10, decimal_places=2)
    image_url= models.URLField(blank=True, null=True)
    category= models.CharField(max_length=64, blank=True, null=True)
    active= models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at=models.DateTimeField(auto_now_add=True)
    watchlist= models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="won_auctions")
    def __str__(self):
        return f"{self.title} - {self.starting_bid}"

class Bid(models.Model):
    auction=models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bidder= models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_amount= models.DecimalField(max_digits=10, decimal_places=2)
    bid_time= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.bidder.username} bid {self.bid_amount} on {self.auction.title}"

class Comment(models.Model):
    auction= models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    commenter= models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_text= models.TextField()
    comment_time= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.auction.title}"