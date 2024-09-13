import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import seaborn as sns
from Db_connection.connection import PostgresConnection
from src.utils import *
import nbimporter
import nbimporter
from scripts.User_overview_analysis.analysis import *
from scripts.visualization.visualize_user_overview import *


# Set up the app title
st.title("Comprehensive Dashboard")
st.write("Welcome to the Telecom growth Analysis Dashboard. Explore different statistical analysis methodologies and visualize data insights.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["User Overview Analysis", "User Engagement Analysis", 
                                  "Experience Analysis", "Satisfaction Analysis"])

# Sample Data to demonstrate plots
data = pd.DataFrame({
    'User': ['A', 'B', 'C', 'D', 'E'],
    'Engagement': [100, 150, 200, 250, 300],
    'Experience': [4, 5, 3, 4, 5],
    'Satisfaction': [80, 90, 70, 85, 95]
})


# Sidebar for customization options
st.sidebar.header("Database Connection")
st.sidebar.markdown("Provide PostgreSQL database connection details below.")



# Function to fetch data from PostgreSQL

# Assuming PostgresConnection is a custom class that manages the connection
db = PostgresConnection(dbname='telecom', user='postgres', password='postgres')

# Connect to the database
db.connect()

# Try-except block to catch any errors during the query execution
try:
    # Query the table
    query = "SELECT * FROM xdr_data_cleaned"
    
    # Execute the query
    result = db.execute_query(query)
    
    # Check if the result is not empty and the cursor description exists
    if result and db.cursor.description:
        # Convert result to DataFrame using the column names from the cursor's description
        df_cleaned = pd.DataFrame(result, columns=[desc[0] for desc in db.cursor.description])
        
        # Display the DataFrame to verify
        print(df_cleaned.info())
        print(df_cleaned.head())  # Show the first few rows for quick inspection
    else:
        print("No data returned or no cursor description available.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection to the database
    db.close_connection()




# Page 1: User Overview Analysis
if page == "User Overview Analysis":
    st.header("User Overview Analysis")
    st.write("This dashboard provides an overview of the users.")

    # Example Plot - Bar chart for User Engagement
    df_user_behavior = aggregate_user_behavior(df_cleaned)
    metrics = analyze_basic_metrics(df_user_behavior)
    plot_duration_histogram(metrics, bins=100)

# Page 2: User Engagement Analysis
elif page == "User Engagement Analysis":
    st.header("User Engagement Analysis")
    st.write("This dashboard explores user engagement data.")

    # Example Plot - Line chart for Engagement
    st.subheader("Engagement Over Time")
    plt.figure(figsize=(8, 6))
    sns.lineplot(x=data['User'], y=data['Engagement'])
    plt.title('Engagement Trends')
    st.pyplot(plt)

# Page 3: Experience Analysis
elif page == "Experience Analysis":
    st.header("Experience Analysis")
    st.write("This dashboard analyzes user experience ratings.")

    # Example Plot - Scatter plot for Experience
    st.subheader("User Experience Ratings")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=data['User'], y=data['Experience'], s=100)
    plt.title('User Experience Ratings')
    st.pyplot(plt)

# Page 4: Satisfaction Analysis
elif page == "Satisfaction Analysis":
    st.header("Satisfaction Analysis")
    st.write("This dashboard provides an analysis of user satisfaction.")

    # Example Plot - Pie chart for Satisfaction
    st.subheader("User Satisfaction Levels")
    satisfaction_data = data['Satisfaction']
    labels = data['User']
    plt.figure(figsize=(8, 6))
    plt.pie(satisfaction_data, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('User Satisfaction Distribution')
    st.pyplot(plt)

# KPIs section
st.sidebar.title("Key Performance Indicators (KPIs)")
st.sidebar.write("Dashboard Usability: Ease of use, with intuitive navigation and clear labels.")
st.sidebar.write("Interactive Elements: Effective use of widgets to enhance user engagement.")
st.sidebar.write("Visual Appeal: Clean and professional design that effectively communicates data insights.")
st.sidebar.write("Deployment Success: Fully functional deployment, accessible via a public URL.")
