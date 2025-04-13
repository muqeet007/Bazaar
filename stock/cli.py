# stock/cli.py
import sys
from .models import Product, StockMovement

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py [add_product|stock_in|sell|remove] <args>")
        return
    cmd = sys.argv[1]
    if cmd == "add_product":
        Product.objects.create(name=sys.argv[2])
        print(f"Added {sys.argv[2]}")
    elif cmd in ["stock_in", "sell", "remove"]:
        product = Product.objects.get(name=sys.argv[2])
        qty = int(sys.argv[3])
        movement_type = "in" if cmd == "stock_in" else cmd
        StockMovement.objects.create(product=product, movement_type=movement_type, quantity=qty)
        print(f"{cmd} {qty} of {product.name}, now at {product.current_quantity()}")

if __name__ == "__main__":
    main()