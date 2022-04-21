# from pyrfc3339 import generate
import frappe,random


# def before_save(self,method):
#     if not self.item_code:
#         x = generate_alphanum()
#         while frappe.db.get_value("Item",{"item_code":x}):
#             x = generate_alphanum()
#         self.item_code = x




def generate_alphanum():
    x = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
    x = "SP-"+x
    return x
