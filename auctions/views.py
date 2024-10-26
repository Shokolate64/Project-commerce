from django.shortcuts import render, redirect, get_object_or_404
from .models import User, AuctionListing, Bid, Comment
from .forms import CreateListingForm, RegisterForm
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request): 
    listings = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", { "listings": listings })

def listing(request, listing_id):
    listing=  get_object_or_404(AuctionListing, id=listing_id)
    bids = Bid.objects.filter(auction=listing)
    comments= Comment.objects.filter(auction=listing)

    if request.method=="POST":
        bid_amount= request.POST.get("bid_amount")
        comment_text = request.POST.get("comment_text")

        if bid_amount:
            bid_amount= float(bid_amount)
            highest_bid= bids.order_by('-bid_amount').first()

            if bid_amount > listing.starting_bid and (not highest_bid or bid_amount > highest_bid.bid_amount): 
                 Bid.objects.create(
                     auction=listing,
                     bidder=request.user,
                     bid_amount=bid_amount
                 )
            else:
                messages.error(request,"Your bid must be higher than the current highest bid.")
                return render(request, "auctions/listing.html",{
                    "listing":listing,
                    "bids": bids,
                    "comments": comments,
                    "message": "Your bid must be greater than the current bid"
                })
        if comment_text:
                Comment.objects.create(
                    auction=listing,
                    commenter=request.user,
                    comment_text=comment_text
                )
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    
    return render(request, "auctions/listing.html", {
        "listing":listing,
        "bids": bids,
        "comments": comments
    })    

@login_required
def create_listing(request):
    if request.method == "POST":
        form= CreateListingForm(request.POST)
        if form.is_valid():
            listing= form.save(commit=False) 
            listing.created_by= request.user
            listing.save()
            return redirect('index')
    else:
        form= CreateListingForm()
    return render(request, "auctions/create_listing.html",{"form":form})        

@login_required
def close_listing(request, listing_id):
    listing= get_object_or_404(AuctionListing, id=listing_id)

    if request.user != listing.created_by:
        return HttpResponseForbidden ("You are not authorized to close this listing.")
    
    listing.active= False
    highest_bid= Bid.objects.filter(auction=listing).order_by('-bid_amount').first()

    if highest_bid:
        listing.winner= highest_bid.bidder 
        listing.save()

    return HttpResponseRedirect(reverse("listing", args=[listing.id]))

def register(request):
    if request.method == "POST":
        form= RegisterForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect("index")
    else:
        form= RegisterForm()
    return render(request, "auctions/register.html",{
        "form": form
    })  

@login_required
def watchlist(request):
    user= request.user
    return render(request, "auctions/watchlist.html",{"watchlist": user.watchlist.all})

def categories(request):
    all_categories= AuctionListing.objects.values_list("category", flat=True).distinct()
    return render(request, "auctions/categories.html",{"categories": all_categories}) 

def category_listings(request, category):
    listings_in_category= AuctionListing.objects.filter(category=category, active=True)
    return render(request, "auctions/category_listings.html", {
        "category":category,
        "listings":listings_in_category
    })

def categories_processor(request):
    categories= AuctionListing.objects.exclude(category__isnull=True).exclude(category__exact='').values_list("category", flat=True).distinct()
    return {'categories':categories}


@login_required
def toggle_watchlist(request, listing_id):
    listing= get_object_or_404(AuctionListing, id=listing_id)
    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user)
    else:
        listing.watchlist.add(request.user)    
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))    