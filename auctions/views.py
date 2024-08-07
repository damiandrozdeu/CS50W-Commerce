from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Auction, Comment, Bid, Category
from django import forms


class NewBidForm(forms.Form):
    bid = forms.DecimalField()


class NewCommentForm(forms.Form):
    comment = forms.CharField(label="comment", widget=forms.Textarea(attrs={'class': 'my-content-class'}))


class NewAuctionForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, label="Description", max_length=500, widget=forms.Textarea(attrs={'class': 'form-control'}))
    initial_price = forms.DecimalField(label="Initial Price", decimal_places=2, max_digits=10, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(label="Image", required=False)
    category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))



def index(request):
    auctions = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "Auctions": auctions
    })


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

@login_required
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

@login_required
def create_listing(request):
    if request.method == "POST":
        form = NewAuctionForm(request.POST, request.FILES) 
        if form.is_valid():
            new_auction = Auction(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                initial_price=form.cleaned_data["initial_price"],
                image=form.cleaned_data["image"],
                category=form.cleaned_data["category"],
                creator=request.user,
                current_price=form.cleaned_data["initial_price"]
            )
            new_auction.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewAuctionForm()
    return render(request, "auctions/create_listing.html", {"form": form})




def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",
                  {"categories": categories}
                  )

def categories_details(request, category_id):
    category_id = Category.objects.get(id=category_id)
    auctions = Auction.objects.filter(category_id=category_id)
    return render(request, "auctions/index.html", {
        "Auctions": auctions
    })



def watchlist(request):
    user = request.user
    watchlist = Auction.objects.filter(watchers=user)
    return render(request, "auctions/watchlist.html",
                  {"watchlist": watchlist
                                        }
                  )

def auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    is_watcher = request.user in auction.watchers.all()
    is_creator = (request.user == auction.creator) and auction.active
    is_winner = False
    comments = auction.comments.all()
    if not auction.active:
        highest_bid = Bid.objects.filter(auction=auction).order_by('-bid').first()
        if highest_bid:
            winner = highest_bid.creator
            is_winner = (request.user == winner)
    form_bid = NewBidForm()
    return render(request, "auctions/auction.html",
                {"auction": auction,
                "is_watcher": is_watcher,
                "form_bid": form_bid,
                "is_creator": is_creator,
                "is_winner": is_winner,
                "comments": comments,
                "form_add": NewCommentForm()
                })



@login_required
def add_watchlist(request, auction_id):
    if request.method == "POST":
        user = request.user
        auction = Auction.objects.get(pk=auction_id)
        auction.watchers.add(user)
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))
    
@login_required
def remove_watchlist(request, auction_id):
    if request.method == "POST":
        user = request.user
        auction = Auction.objects.get(pk=auction_id)
        auction.watchers.remove(user)
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))
    
@login_required
def add_bid(request, auction_id):
    auction = Auction.objects.get(pk = auction_id)
    if request.method == "POST":
        user = request.user
        form_bid = NewBidForm(request.POST)
        if form_bid.is_valid():
            if form_bid.cleaned_data["bid"] > auction.current_price:
                new_bid = Bid (bid = form_bid.cleaned_data["bid"], creator = user , auction = auction )
                new_bid.save()
                auction.current_price = form_bid.cleaned_data["bid"]
                auction.save()
                return HttpResponseRedirect(reverse("auction", args=[auction_id]))
            else:
                form_bid = NewBidForm()
                message_bid = "Your bid is smaller then current price!"
        else:
            form_bid = NewBidForm()
    return render(request, "auctions/auction.html", {"form_bid": form_bid,
                                                     "message_bid": message_bid,
                                                     "auction": auction} )

@login_required
def close_auction(request, auction_id):
    auction = Auction.objects.get(pk = auction_id)
    if request.method == "POST":
        auction.active = False
        auction.save()
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))
    


@login_required
def add_comment(request, auction_id):
    if request.method == "POST":
        user = request.user
        auction = Auction.objects.get(pk=auction_id)
        form_add = NewCommentForm(request.POST)
        if form_add.is_valid():
            new_add = Comment(creator=user, auction=auction, comment= form_add.cleaned_data["comment"])
            new_add.save()    
        return HttpResponseRedirect(reverse("auction", args=[auction_id]))
    