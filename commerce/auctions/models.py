from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# one for auction listings, one for bids, and one for comments made on auction listings.
class AuctionListings(models.Model):
    title = models.CharField(max_length=64, default='')
    description = models.TextField(default='')
    starting_bid = models.FloatField(default=0)
    url = models.URLField(max_length=200, null=True)

    
class Bids(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    bid = models.FloatField(default=0)
    
    
class Comments(models.Model):
    listing_id = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=64)
    
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)