# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class AmazonsqlPipeline:
    def process_item(self, item, spider):
        return item


# class RpiFilterPipeline:
#     def process_item(self, item, spider):
#         # Get the product name from the item
#         product_name = item.get("name", "").lower()  # Fetching the name field

#         # Check if both "raspberry pi" and "single board" are in the product name
#         if "raspberry pi" in product_name and "single board" in product_name:
#             return item  # If it matches, return the item
#         else:
#             raise DropItem("Filtered out item: does not contain 'Raspberry Pi' and 'single board'")
        



import mysql.connector



class SavingToMySQLPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()  # Create the table when the connection is initialized

    def create_connection(self):
        try:
            # Connect to MySQL server (without specifying a database at first)
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='rheyrabusa200116;',
                database = "amazon_scraping"
            )
            self.curr = self.conn.cursor()
            
                
            # Reconnect to the specific database
            self.conn.database = 'amazon_scraping'
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise

    def create_table(self):
        # Create the table if it doesn't already exist
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS amazon_products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price VARCHAR(50),
                ratings VARCHAR(50),
                stars VARCHAR(50)
                
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_in_db(item)
        return item

    def store_in_db(self, item):
        try:
            self.curr.execute("""
                INSERT INTO amazon_products (name, price, ratings, stars) 
                VALUES (%s, %s, %s, %s)
            """, (
                item["name"],
                item["price"],
                item["ratings"],
                item["stars"]
            ))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting item: {err}")

    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()

















    # def __init__(self):
    #     self.create_connection()
    #     self.create_table()  # Create the table when the connection is initialized

    # def create_connection(self):
    #         # Connect to MySQL server (without specifying a database at first)
    #         self.conn = mysql.connector.connect(
    #             host='localhost',
    #             user='root',
    #             password='rheyrabusa200116;',
    #             database = 'scrapedata'
    #         )
    #         self.curr = self.conn.cursor()
            
    #         # Create the database if it doesn't exist
    #         self.curr.execute("CREATE DATABASE IF NOT EXISTS amazon_scraping")
            
    #         # Reconnect to the specific database
    #         self.conn.database = 'amazon_scraping'
            

    # def create_table(self):
    #     # Create the table if it doesn't already exist
    #     self.curr.execute("""DROP TABLE IF EXISTS amazon_products""")
    #     self.curr.execute("""create table amazon_products(
    #                       name text,
    #                       price text,
    #                       ratings text,
    #                       stars text
    #                       )""")
    #     self.conn.commit()

    # def process_item(self, item, spider):
    #     self.store_in_db(item)
    #     return item

    # def store_in_db(self, item):
    #         self.curr.execute("""
    #             INSERT INTO amazon_products (name, price, ratings, stars) 
    #             VALUES (%s, %s, %s, %s)
    #         """, (
    #             item["name"][0],
    #             item["price"][0],
    #             item["ratings"][0],
    #             item["stars"][0]
    #         ))
    #         self.conn.commit()
        
    # def close_spider(self, spider):
    #     self.curr.close()
    #     self.conn.close()
