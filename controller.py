from model import ShopModel, Product
from view import ShopView

class ShopController:
    def __init__(self, con):
        self._con = con
        self.model = ShopModel(con)
        self.view = ShopView()

    def run (self):

        while True:
            self.view.show_menu()

            choice = self.view.get_input(">")
            if choice == "1":
                self.view.show_list(self.model.get_all(), header=" - Products - ")
            elif choice == "2":
                product = self.view.show_add_product()
                self.model.add_product(product)
                self.view.show_message("Product added")
            elif choice == "3":
                name = self.view.get_input("Enter product name")
                products = self.model.search(name)
                self.view.show_list(products, header=" - Products - ")
            elif choice == "4":
                id = self.view.get_input("Enter product id")
                products = self.model.search(id=id)
                self.view.show_list(products, header=" - Products - ")
                if self.view.get_input("Delete this products? (y/n)").lower() == "y":
                    for product in products:
                        self.model.remove(product)
                    self.view.show_message("Product removed")
                else:
                    self.view.show_message("No products were deleted")
            elif choice == "5":
                categories = self.model.get_categories()
                count = self.model.get_count_categories(categories)
                self.view.show_list(categories, count=count, header=" - Categories - ")
            elif choice == "0":
                break


