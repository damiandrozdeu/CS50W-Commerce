from .models import Auction

def watchlist_count(request):
    if request.user.is_authenticated:
        count = Auction.objects.filter(watchers=request.user).count()
    else:
        count = 0
    return {
        'watchlist_count': count
    }

