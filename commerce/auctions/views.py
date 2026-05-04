from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .models import User, AuctionListings, Bids


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
        return render(request, "auctions/listing.html", { 'listing': listing})
    elif request.method == "POST":
        listing_id = request.POST.get('listing_id')
        listing_object = AuctionListings.objects.get(id=listing_id)
        max_bid = float(Bids.objects.filter(listing_id=listing_id).aggregate(Max('bid'))['bid__max'])

        new_bid = float(request.POST.get('new_bid'))
        user = request.user
        if new_bid > max_bid:
            return HttpResponse("New bid is set")
        else: 
            return HttpResponse("Bid must be higher than" + str(max_bid))





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
