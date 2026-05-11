from controller import ShopController
import sqlite3

if __name__ == '__main__':
    con = sqlite3.connect('Shop.db')

    controller = ShopController(con)
    controller.run()
    con.close()
