from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .models import User, AuctionListings, Bids, WatchList


def index(request):
    if request.method == 'GET':
        data = AuctionListings.objects.all()
        print(type(data))
        return render(request, "auctions/index.html", { "data" : data })



# Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create-listing.html")    
    
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["bid"]
        if request.POST["image-url"]:
            image_url = request.POST["image-url"]
        else:
            image_url = None
        
        new_listing = AuctionListings.objects.create(title=title, description=description, starting_bid=starting_bid, url=image_url)
        new_listing.save()
        
        return HttpResponse((title, description, starting_bid, image_url, new_listing))


def listing_page(request, listing_id):
    if request.method == "GET":
        listing = AuctionListings.objects.get(id=listing_id)
        print("Fetched Listing: ", listing)
        total_bids = len(Bids.objects.filter(listing_id=listing.id))
        print("Fetched total_bids: ", total_bids)
        max_bid = Bids.objects.filter(listing_id=listing_id).aggregate(Max('bid'))['bid__max']
        if (not max_bid):
            max_bid = AuctionListings.objects.get(id=listing.id).starting_bid
            print(max_bid)
        in_watchlist = WatchList.objects.filter(user=request.user, listing=listing_id).exists()
        return render(request, "auctions/listing.html", 
                      {'listing': listing, 'total_bids': total_bids, 'max_bid' : max_bid, 'in_watchlist': in_watchlist})
    
    
    elif request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing_object = AuctionListings.objects.get(id=listing_id)
        max_bid = float(Bids.objects.filter(listing_id=listing_id).aggregate(Max('bid'))['bid__max'])

        bid_price = float(request.POST.get('new_bid'))
        user = request.user
        if bid_price > max_bid:
            new_bid = Bids.objects.create(user_id=user, listing_id=listing_object, bid=bid_price)
            new_bid.save()
            return HttpResponseRedirect((listing_id))

        else: 
            return HttpResponse("Bid must be higher than" + str(max_bid))


def add_to_watchlist(request, listing_id):
    if request.method=="POST":
        print("in add to watchlist function")
        # if watchlist contains a row with the current user id ad the current listing id then 
        existing = WatchList.objects.filter(user=request.user, listing=listing_id)
        if existing:
            # delete that
            print('inside if')
            existing.delete()
            print("Row deleted!")
        else:
            print('inside else')
            listing_object = AuctionListings.objects.get(id=listing_id)
            watchlist = WatchList.objects.create(user=request.user, listing=listing_object)
            watchlist.save()
            print("row added ")
            
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
