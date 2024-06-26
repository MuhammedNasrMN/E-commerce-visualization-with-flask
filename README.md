# E-commerce Data Analysis and Visualization With Flask
## Description
This project is a project to upload a specifc dataset to MySQL database, then connect to the database and recall the data using SQL queries in Python.
After that the database is connected to Power BI to visualize the data and draw insights. And finally a webapp was created using Flask to host different visualizations.

### 1-Importing Data to MySQL data base
first of all we will need to to install MySQL Connector and Pandas

<pre>
  <code>
pip install pandas
pip install sqlalchemy  </code>
</pre>
after we install both pandas and SQLAlchemy we can import both libraries
<pre>
<code>
import from sqlalchemy import create_engine, types
import pandas as pd
</code>
</pre>
<pre>
  <code>
    engine = create_engine("mysql://root:password@localhost:3306/db") #connecting to the database, add your password and database name inplace of "password" and "db"
connection=engine.connect()
  </code>
</pre>
then add the files names to a list so we can loop through them and load them to the database
<pre>
  <code>
    file_names = ["customers", "categories","Geolocation", "orders", "Order Items",
             "Order Payments", "Products", "Reviews","Sellers"] #file and table names
  </code>
</pre>
looping through files names and adjusting them to SQL syntax and then loading them into the database.
<pre>
  <code>
    for file in file_names:
      csv_file = file+".csv"
      table_name = file.replace(" ","_")
      df = pd.read_csv(csv_file)
      df.to_sql(table_name,con=engine,index=False,if_exists='append')
  </code>
</pre>
### 2-Data Exploration and Visualization
after uploading the files to MySQL database we can start exploring and drawing insgihts from the data
first of all we will need to install plotly if it is not already installed
<pre>
  <code>
    pip install plotly
  </code>
</pre>
We then will import pandas,plotly to visualize the data and MySQL connector to connect and recall data from the database
<pre>
  <code>
    import pandas as pd
    import mysql.connector
    import plotly.express as px
  </code>
</pre>
We then will connect to the database
<pre>
  <code>
    connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password', #replace with your password
    database='db' #replace with your db name
)

  </code>
</pre>
We can also make sure that we are connected to the db by using 
<pre>
  <code>
    print(connection.is_connected())
  </code>
</pre>
We then will start recalling data by writing SQL queries and then saving the data to a Pandas dataframe
<pre>
  <code>
    select_query = "SELECT * FROM orders;"
    df_orders = pd.read_sql(select_query, connection)
  </code>
</pre>
### 3-Flask Webapp
To run the webapp we will need to connect to the database that contains all the tables and we will also need to install flask
<pre>
  <code>
    pip install flask
  </code>
</pre>
We then will import flask, Pandas, Plotly and MySQL connector
<pre>
  <code>
    from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import mysql.connector
  </code>
</pre>
We can do the same steps did in data exploartion to connect to the data base.
The app has mainly two main routes /dashboard and /data excluding the homepage.
/dashboard has some visualiztions and comments and insights.
While /data contains links to all the tables in the data base.
We are going to load the data to a pandas dataframe and visualize the data like we did in the exploration step.
Then we will make the visualizations into an HTML div using the tohtml() function.
<pre>
  <code>
    bar_chart_payment_method = px.bar(df_payment_method,x = 'payment_type', y='Number_of_Payments',
                                       title = 'Favourite Payment Method For Customers')
    bar_chart_payment_method.update_layout(
        xaxis_title='Payment Method',
        yaxis_title='Number of Transactions'
        , plot_bgcolor = "white")

    payment_method_div = bar_chart_payment_method.to_html(full_html=False)
  </code>
</pre>
After that we will return all the charts on the page.
<pre>
  <code>
    return render_template('dashboard.html', payment_method_div=payment_method_div, performance_div = performance_div, 
                           orders_value_div = orders_value_div, orders_by_day_div = orders_by_day_div, 
                           category_revenue_div = category_revenue_div, average_price_div = average_price_div)
  </code>
</pre>

To run the webapp make sure you are connected to the database and then type.
<pre>
  <code>
    set FLASK_APP=your_app_name.py
    flask run
  </code>
</pre>
Now the webapp is running and you can access it by going to http://127.0.0.1:5000/
## Screenshots
![Imgur](https://i.imgur.com/lTeeBbV.png)
![Imgur](https://i.imgur.com/7zPcoup.png)
![Imgur](https://i.imgur.com/YeUOuCC.png)
![Imgur](https://i.imgur.com/KtBQcK2.png)
![Imgur](https://i.imgur.com/KLAWVcE.png)
![Imgur](https://i.imgur.com/NdIl1NZ.png)

