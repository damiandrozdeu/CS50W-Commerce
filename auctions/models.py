from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"


class Auction(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True, upload_to="images") 
    description = models.TextField(null=True, blank=True) 
    initial_price = models.DecimalField(decimal_places=2, max_digits=10)
    watchers = models.ManyToManyField(User,  blank=True, related_name="watchlist")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")
    created_date = models.DateTimeField(auto_now_add=True)
    current_price = models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.creator.username}"

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500)
    def __str__(self):
        return f"{self.comment}"

class Bid(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField( decimal_places=2, max_digits=10)



    