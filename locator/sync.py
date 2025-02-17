import pyodbc
import requests
from datetime import datetime
from decimal import Decimal

# Function to convert Decimal and datetime values
def convert_special_types(record):
    for key, value in record.items():
        if isinstance(value, Decimal):
            record[key] = float(value)
        elif isinstance(value, datetime):  # Check if value is datetime object
            record[key] = value.strftime('%Y-%m-%d %H:%M:%S')  # Convert to desired format
    return record

def fetch_salesData():
    conn_str = 'Driver=SQL Server;Server=localhost;Database=POS2;UID=smtech;PWD=smtech1'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    try:
        # Fetch unsynced bill_suffix values
        query = "SELECT DISTINCT bill_suffix FROM tbl_sales_record WHERE bill_suffix NOT IN (SELECT bill_suffix FROM tbl_sales_sync)"
        cursor.execute(query)
        unsynced_bills = cursor.fetchall()

        for sale in unsynced_bills:
            query = "SELECT * FROM tbl_sales_record WHERE bill_suffix = ?"
            cursor.execute(query, (sale.bill_suffix,))
            sales_by_bill = cursor.fetchall()

            if sales_by_bill:
                product_data_list = []
                payment_modes = []

                for sale_item in sales_by_bill:
                    product_data_list.append({
                        'productId': int(sale_item.item_id),
                        'productCost': float(sale_item.cost),
                        'productDiscount': float(sale_item.discount_amt),
                        'productName': sale_item.item_name,
                        'productQTY': float(sale_item.quantity),
                        'productSubtotal': float(sale_item.total),
                        'productTax': float(sale_item.tax_amt),
                        'productTotal': float(sale_item.total),
                    })

                # Handle payment modes
                payment_mode = sales_by_bill[0].payment_mode
                total_amount = float(sales_by_bill[0].grand_total)

                if "/" not in payment_mode:
                    if payment_mode != "Credit":
                        payment_modes.append({
                            'amount': total_amount,
                            'mode': payment_mode
                        })
                else:
                    modes = payment_mode.split('/')
                    if len(modes) == 2:
                        cash_amount = float(sales_by_bill[0].cash_amount)
                        card_amount = float(sales_by_bill[0].card_amount)
                        payment_modes.append({'amount': cash_amount, 'mode': modes[0]})
                        payment_modes.append({'amount': card_amount, 'mode': modes[1]})

                # Create the payload
                payload = {
                    'bill_no': int(sales_by_bill[0].bill_no),
                    'cashierName': sales_by_bill[0].cashier_name,
                    'companyId': "1",
                    'bill_suffix': sales_by_bill[0].bill_suffix,
                    'customerCode': int(sales_by_bill[0].customer_id),
                    'dateOfSales': sales_by_bill[0].date_of_sale.strftime('%Y-%m-%d %H:%M:%S'),
                    'discount': float(sales_by_bill[0].discount),
                    'fiscalYear': sales_by_bill[0].fiscal_year,
                    'grandTotal': float(sales_by_bill[0].grand_total),
                    'serviceCharge': float(sales_by_bill[0].service_charge),
                    'subTotal': float(sales_by_bill[0].sub_total),
                    'taxableAmount': float(sales_by_bill[0].taxable_amount),
                    'nonTaxAmount': float(sales_by_bill[0].non_taxable_amount),
                    'taxAmount': float(sales_by_bill[0].tax_amount),
                    'paymentMode': payment_modes,
                    'productData': product_data_list
                }

                # Post to API
                response = postSalesData(payload)
                if response:
                    insert_into_sales_sync(conn, payload['bill_no'], payload['fiscalYear'], payload['bill_suffix'])

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cursor.close()
        conn.close()

def postSalesData(salesData):
    url = "http://192.168.0.83:5000/Sales/POS/api"
    try:
        response = requests.post(url, json=salesData)
        response.raise_for_status()
        print("Data posted successfully.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to post data: {e}")
        return False

def insert_into_sales_sync(conn, bill_no, fiscal_year, bill_suffix):
    cursor = conn.cursor()
    query = """
    INSERT INTO tbl_sales_sync (bill_no, fiscal_year, bill_suffix)
    VALUES (?, ?, ?)
    """
    cursor.execute(query, (bill_no, fiscal_year, bill_suffix))
    conn.commit()
    cursor.close()

# Main function
if __name__ == "__main__":
    fetch_salesData()
