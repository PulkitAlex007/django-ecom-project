def cart_data(request):
    cart = request.session.get("cart", {})
    return {
        "cart_count": len(cart)
    }