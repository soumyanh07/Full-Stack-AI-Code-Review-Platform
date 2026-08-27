def calculate_total(price, quantity):
    total = price * quantity

    if quantity > 0:
        discount = 10
        total = total - discount

    return total
