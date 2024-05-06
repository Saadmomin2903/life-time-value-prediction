# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

# Initialize Flask app
# Initialize Flask app
app = Flask(__name__, template_folder='template')



# Check if we're running in debug mode
debug_mode = True

# Import Data
tx_data = pd.read_csv("OnlineRetail.csv", encoding="cp1252")

# Check the shape (number of columns and rows) in the dataset
tx_data.shape

# Find out missing values
tx_data.isnull().sum(axis=0)

# Remove time from date
tx_data['InvoiceDate'] = pd.to_datetime(tx_data['InvoiceDate'], format="%m/%d/%Y %H:%M").dt.date

# There are 135,080 missing values in the CustomerID column, and since our analysis is based on customers,
# we will remove these missing values.
tx_data = tx_data[pd.notnull(tx_data['CustomerID'])]

# Keep records with non negative quantity
tx_data = tx_data[(tx_data['Quantity'] > 0)]

# Add a new column depicting total sales
tx_data['Total_Sales'] = tx_data['Quantity'] * tx_data['UnitPrice']
necessary_cols = ['CustomerID', 'InvoiceDate', 'Total_Sales']
tx_data = tx_data[necessary_cols]

# Built-in utility functions from lifetimes package to transform the transactional data (one row per purchase)
# into summary data (a frequency, recency, age and monetary).
from lifetimes.plotting import *
from lifetimes.utils import *

lf_tx_data = summary_data_from_transaction_data(tx_data, 'CustomerID', 'InvoiceDate', monetary_value_col='Total_Sales',
                                                observation_period_end='2011-12-9')

# Process the data as needed for your analysis

@app.route('/')
def index():
    # Your CLV analysis code here
    # For example:
    top_customers = lf_tx_data.head(10)  # Example: Top 10 customers by CLV
    return render_template('index.html', top_customers=top_customers)

if __name__ == '__main__':
    app.run(debug=debug_mode)
