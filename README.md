#E-commerce Data Analysis and Visualization With Flask
##Description
This project is a project to upload a specifc dataset to MySQL database, then connect to the database and recall the data using SQL queries in Python.
After that the database is connected to Power BI to visualize the data and draw insights. And finally a webapp was created using Flask to host different visualizations.

###1-Importing Data to MySQL data base
first of all we will need to to install MySQL Connector and Pandas
*pip install pandas*
*pip install mysql-connector-python*
after we install both pandas and MySQL connector we can import both libraries
<pre>
<code>
import mysql.connector
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
