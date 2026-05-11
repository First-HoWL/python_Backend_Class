from model import Product


class ShopView:
    def show_menu(self):
        print(" - Shop - ")
        print(" 1) Show Products")
        print(" 2) Add Product")
        print(" 3) Lookup Product")
        print(" 4) Delete Product")
        print(" 5) Show Categories")
        print(" 0) Quit")

    def show_list(self, products: list, header = None, count=None):
        if not products:
            print("No products selected")
            return
        else:
            if header : print(header)
            for i, product in enumerate(products):
                print(f"{product} {"" if count is None else f"({count[i]})"}")

    def show_add_product(self):
        name = None
        price = 0
        description = None
        quantity = 0
        category = None
        while name is None or name == "":
            name = self.get_input("Enter product name")
        while True:
            price = self.get_input("Enter product price")
            if price.isnumeric():
                price = float(price)
                break
            else:
                print("Invalid price")
                pass
        while description is None or description == "":
            description = self.get_input("Enter product description")
        while True:
            quantity = self.get_input("Enter product quantity")
            if quantity.isnumeric():
                quantity = int(quantity)
                break
            else:
                print("Invalid quantity")
                pass
        while category is None or category == "":
            category = self.get_input("Enter product category")
        return Product(id=0, name=name, price=price, description=description, quantity=quantity,category=category)



    def show_message(self, message: str):
        print(f"  {message}")
    def show_error(self, message: str):
        print(f" !! {message}")
    def get_input(self, prompt: str):
        return input(f"  {prompt}:  ").strip()
