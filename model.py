
class Product:
    def __init__(self, id,  name, price, description, quantity, category):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity
        self.category = category


    def __repr__(self):
        return f"| {self.id} \t | {self.name} \t | {self.price} grn. \t | {self.description} \t | {self.category} \t | {self.quantity} pcs |"

class ShopModel:
    def __init__(self, con, products=None):
        self._con = con
        if products is None:
            pass
        elif isinstance(products, list):
            self._products = products
        else:
            raise TypeError("products must be a list")
    def get_all(self):
        rows = list(self._con.cursor().execute("SELECT * FROM products").fetchall())
        products = []

        for row in rows:
            product = Product(
                id=row[0],
                name=row[1],
                price=row[2],
                description=row[3],
                quantity=row[4],
                category=row[5]
            )
            products.append(product)

        return products

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("products must be a Product")
        else:
            self._con.cursor().execute("INSERT INTO products (name, price, description, quantity, category) VALUES (?, ?, ?, ?, ?)", (product.name, product.price, product.description, product.quantity, product.category))
            self._con.commit()

    def get_categories(self):
        rows = self._con.cursor().execute("SELECT category FROM products").fetchall()
        categories = []
        for row in rows:
            if row[0] not in categories:
                categories.append(row[0])

        return categories

    def get_count_categories(self, categories):
        count = []
        for category in categories:
            rows = self._con.cursor().execute("SELECT * FROM products WHERE category = ?", (category, )).fetchall()
            count.append(len(rows))
        return count

    def search(self, name=None, id=None):
        if name is not None:
            rows = self._con.cursor().execute("SELECT * FROM products WHERE name = ?", (name, )).fetchall()
        elif id is not None:
            rows = self._con.cursor().execute("SELECT * FROM products WHERE id = ?", (id, )).fetchall()
        products = []

        for row in rows:
            product = Product(
                id=row[0],
                name=row[1],
                price=row[2],
                description=row[3],
                quantity=row[4],
                category=row[5]
            )
            products.append(product)

        return products

    def remove(self, product: Product):
        if not isinstance(product, Product):
            print(type(product))
            raise TypeError("products must be a Product")
        self._con.cursor().execute("DELETE FROM products WHERE id = ?", (product.id,))
        self._con.commit()