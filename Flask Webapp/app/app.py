from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

#db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SECRET_KEY'] = 'thisisasecretkey'


#class User(db.Model, UserMixin):
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(20), nullable=False, unique=True)
    #password = db.Column(db.String(80), nullable=False)


connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password', #type your password here
    database='db' #enter your database name here
)

cursor = connection.cursor(buffered=True)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/dashboard')
def dashboard():

    #### First Graph ####

    select_query_payment_method="""SELECT payment_type, COUNT(payment_type) AS Number_of_Payments
                                    FROM order_payments
                                    GROUP BY payment_type"""
    
    df_payment_method = pd.read_sql(select_query_payment_method, connection)

    df_payment_method['payment_type'] = df_payment_method['payment_type'].str.replace('_', ' ')
    df_payment_method['payment_type'] = df_payment_method['payment_type'].str.title()

    bar_chart_payment_method = px.bar(df_payment_method,x = 'payment_type', y='Number_of_Payments',
                                       title = 'Favourite Payment Method For Customers')
    bar_chart_payment_method.update_layout(
        xaxis_title='Payment Method',
        yaxis_title='Number of Transactions'
        , plot_bgcolor = "white")

    payment_method_div = bar_chart_payment_method.to_html(full_html=False)


    #### Second Graph ####
    select_query_category_sales = """SELECT COUNT(order_items.product_id) AS Category_Sales, categories.product_category_name_english AS Category
                                    FROM products
                                    LEFT JOIN order_items on order_items.product_id=products.product_id
                                    LEFT JOIN categories ON categories.product_category_name=products.product_category_name
                                    GROUP BY products.product_category_name
                                    ORDER BY Category_Sales DESC;"""

    df_category_sales = pd.read_sql(select_query_category_sales, connection)

    df_category_sales['Category'] = df_category_sales['Category'].str.replace('_', ' ')
    df_category_sales['Category'] = df_category_sales['Category'].str.title()

    fig_category_performance = px.bar(df_category_sales,x = 'Category',y = 'Category_Sales',
                                      title = 'Products Sales by Category')
    fig_category_performance.update_layout(
        xaxis=dict(tickfont=dict(size=7)), 
         yaxis=dict(tickfont=dict(size=7)),
        xaxis_title='Category',
        yaxis_title='Sales'
        , plot_bgcolor = "white")
    performance_div = fig_category_performance.to_html(full_html=False)


    #### Third Graph ####

    select_query_orders_value = """SELECT order_items.order_id,SUM(order_items.price) AS order_value
                                    FROM order_items
                                    GROUP BY order_items.order_id"""

    df_orders_value = pd.read_sql(select_query_orders_value, connection)
    histogram_orders=px.histogram(df_orders_value,x = 'order_value', title = 'Orders Value Range')

    histogram_orders.update_layout(
        xaxis_title='orders value',
        yaxis_title='number of orders'
        , plot_bgcolor = "white")
    
    orders_value_div = histogram_orders.to_html(full_html=False)

    #### Fourth Graph ####

    select_query_delivery_time = """SELECT order_id AS Orders, order_purchase_timestamp AS order_placement, order_delivered_customer_date AS order_delivery
    FROM orders"""
    df_delivery_time = pd.read_sql(select_query_delivery_time, connection)

    df_delivery_time['order_placement'] = pd.to_datetime(df_delivery_time['order_placement'])
    df_delivery_time['order_delivery'] = pd.to_datetime(df_delivery_time['order_delivery'])

    df_delivery_time['order_placement'] = df_delivery_time['order_placement'].dt.date
    df_delivery_time['order_delivery'] = df_delivery_time['order_delivery'].dt.date

    df_orders_by_date = df_delivery_time.groupby('order_placement')['Orders'].count().reset_index()

    orders_line_plot = px.line(df_orders_by_date,x = 'order_placement', y = 'Orders',
                               title = 'Order Deliveries By Day')
    orders_line_plot.update_layout(
        xaxis_title='Date',
        yaxis_title='Number of Orderss'
        , plot_bgcolor = "white")

    orders_by_day_div = orders_line_plot.to_html(full_html=False)

    #### Fifth Graph ####

    select_query_revenue = """SELECT categories.product_category_name_english AS Categories, 
                        AVG(order_items.price)*COUNT(order_items.product_id) AS Category_Revenue
                        ,AVG(order_items.price) AS Average_Price
                        FROM products
                        LEFT JOIN order_items ON products.product_id=order_items.product_id
                        LEFT JOIN categories ON products.product_category_name=categories.product_category_name
                        GROUP BY Categories
                        ORDER BY Category_Revenue DESC"""
    
    df_category_revenue = pd.read_sql(select_query_revenue, connection)
    
    df_category_revenue['Categories'] = df_category_revenue['Categories'].str.replace('_', ' ')
    df_category_revenue['Categories'] = df_category_revenue['Categories'].str.title()

    fig_category_revenue = px.bar(df_category_revenue,x = 'Categories',y = 'Category_Revenue'
                                  , title = 'Products Revenue By Category')
    fig_category_revenue.update_layout(
        xaxis=dict(tickfont=dict(size=7)), 
         yaxis=dict(tickfont=dict(size=7)),
        xaxis_title='Category',
        yaxis_title='Products Revenue'
        , plot_bgcolor = "white")
    
    category_revenue_div = fig_category_revenue.to_html(full_html=False)


    #### Sixth Graph ####
    fig_category_avg_price = px.bar(df_category_revenue,x = 'Categories',y = 'Average_Price', title = 'Products Average Price By Category')
    fig_category_avg_price.update_layout(
        xaxis=dict(tickfont=dict(size=7)), 
         yaxis=dict(tickfont=dict(size=7)),
        xaxis_title='Category',
        yaxis_title='Products Revenue'
        , plot_bgcolor = "white")
    average_price_div = fig_category_avg_price.to_html(full_html=False)



    return render_template('dashboard.html', payment_method_div=payment_method_div, performance_div = performance_div, 
                           orders_value_div = orders_value_div, orders_by_day_div = orders_by_day_div, 
                           category_revenue_div = category_revenue_div, average_price_div = average_price_div)

class StringModifier:
    def __init__(self):
        self.result_string = "SELECT * FROM"
    def table_name(self, table):
        self.result_string += " " + table
        return self.result_string
    

@app.route('/data')
def data():

    return render_template('data.html')


@app.route('/data/orders')
def orders():
    select_query_orders_table = StringModifier()
    select_query_orders_table = select_query_orders_table.table_name('orders')

    orders_table = pd.read_sql(select_query_orders_table, connection)
    orders_table_div = orders_table.to_html(classes='table table-striped')

    return render_template('orders.html', orders_table_div = orders_table_div)


@app.route('/data/order_payments')
def order_payments():
    select_query_order_payments_table = StringModifier()
    select_query_order_payments_table = select_query_order_payments_table.table_name('order_payments')

    order_payments_table = pd.read_sql(select_query_order_payments_table, connection)
    order_payments_table_div = order_payments_table.to_html(classes='table table-striped')

    return render_template('order_payments.html', order_payments_table_div = order_payments_table_div)


@app.route('/data/order_items')
def order_items():
    select_query_order_items_table = StringModifier()
    select_query_order_items_table = select_query_order_items_table.table_name('order_items')

    order_items_table = pd.read_sql(select_query_order_items_table, connection)
    order_items_table_div = order_items_table.to_html(classes='table table-striped')

    return render_template('order_items.html', order_items_table_div = order_items_table_div)



@app.route('/data/customers')
def customers():
    select_query_customers_table = StringModifier()
    select_query_customers_table = select_query_customers_table.table_name('customers')

    customers_table = pd.read_sql(select_query_customers_table, connection)
    customers_table_div = customers_table.to_html(classes='table table-striped')

    return render_template('customers.html', customers_table_div = customers_table_div)



@app.route('/data/products')
def products():
    select_query_products_table = StringModifier()
    select_query_products_table = select_query_products_table.table_name('products')

    products_table = pd.read_sql(select_query_products_table, connection)
    products_table_div = products_table.to_html(classes='table table-striped')

    return render_template('products.html', products_table_div = products_table_div)



@app.route('/data/sellers')
def sellers():
    select_query_sellers_table = StringModifier()
    select_query_sellers_table = select_query_sellers_table.table_name('sellers')

    sellers_table = pd.read_sql(select_query_sellers_table, connection)
    sellers_table_div = sellers_table.to_html(classes='table table-striped')

    return render_template('sellers.html', sellers_table_div = sellers_table_div)


@app.route('/data/geolocation')
def geolocation():
    select_query_geolocation_table = StringModifier()
    select_query_geolocation_table = select_query_geolocation_table.table_name('geolocation')

    geolocation_table = pd.read_sql(select_query_geolocation_table, connection)
    geolocation_table_div = geolocation_table.to_html(classes='table table-striped')

    return render_template("geoloaction.html", geolocation_table_div = geolocation_table_div)



@app.route('/data/reviews')
def reviews():
    select_query_reviews_table = StringModifier()
    select_query_reviews_table = select_query_reviews_table.table_name('reviews')

    reviews_table = pd.read_sql(select_query_reviews_table, connection)
    reviews_table_div = reviews_table.to_html(classes='table table-striped')

    return render_template('reviews.html', reviews_table_div = reviews_table_div)



@app.route('/data/categories')
def categories():
    select_query_categories_table = StringModifier()
    select_query_categories_table = select_query_categories_table.table_name('categories')

    categories_table = pd.read_sql(select_query_categories_table, connection)
    categories_table_div = categories_table.to_html(classes='table table-striped')

    return render_template('categories.html', categories_table_div = categories_table_div)



if __name__ == '__main__':
    app.run(debug=True)


 
