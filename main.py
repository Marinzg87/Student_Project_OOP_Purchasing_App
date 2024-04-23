import pandas as pd
from fpdf import FPDF

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
        pdf = FPDF (orientation="P", unit="mm", format="A4")
        pdf.add_page ()

        pdf.set_font (family="Times", size=16, style="B")
        pdf.cell (w=50, h=8, txt=f"Receipt nr.1", ln=1)

        pdf.set_font (family="Times", size=16, style="B")
        pdf.cell (w=50, h=8, txt=f"Article: {self.item_name}", ln=1)

        pdf.set_font (family="Times", size=16, style="B")
        pdf.cell (w=50, h=8, txt=f"Price: {self.item_price}", ln=1)

        pdf.output ("receipt.pdf")
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
