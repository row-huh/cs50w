from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListings)
admin.site.register(Bids)
admin.site.register(Comments)