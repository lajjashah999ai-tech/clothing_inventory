from .models import Item


def global_stats(request):
    if not request.user.is_authenticated:
        return {}
    return {
        'low_stock_count': Item.objects.filter(is_active=True, quantity__lt=5).count(),
    }
