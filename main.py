import pandas as pd

# Read the file and create a dataframe
df = pd.read_csv("articles.csv", dtype={"id": str})


# Classes
class Item:
    def __init__(self, local_item_id):
        self.item_id = local_item_id
        self.name = df.loc[df["id"] == self.item_id, "name"].squeeze()
        self.price = df.loc[df["id"] == self.item_id, "price"].squeeze()
        self.in_stock = int(df.loc[df["id"] == self.item_id,
                            "in stock"].squeeze())

    def available(self):
        """Check if the item is in the stock"""
        if self.in_stock > 1:
            availability = True
        else:
            availability = False
        return availability

    def order(self):
        """Update the stock quantity"""
        new_quantity = self.in_stock - 1
        df.loc[df["id"] == self.item_id, "in stock"] = str(new_quantity)
        df.to_csv ("articles.csv", index=False)


class Receipt:
    def __init__(self, local_item_name, local_item_price):
        self.item_name = local_item_name
        self.item_price = local_item_price

    def generate(self):
        content = f""""
        Thank you for your purchase!
        Here are your receipt info:
        Item: {self.item_name}
        Price: {self.item_price}
        """
        return content


# Main process
print(df)
item_id = input("Enter the item id: ")
item = Item(item_id)
if item.available():
    item.order()
    receipt = Receipt(local_item_name=item.name, local_item_price=item.price)
    print(receipt.generate())
else:
    print("Item out of stock!")
