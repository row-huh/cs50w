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
    user_id = models.ForeignKey(User)
    listing_id = models.ForeignKey(AuctionListings)
    bid = models.FloatField(default=0)
    
    
class Comments(models.Model):
    listing_id = models.ForeignKey(AuctionListings)
    user_id = models.ForeignKey(User)
    content = models.CharField(max_length=64)

