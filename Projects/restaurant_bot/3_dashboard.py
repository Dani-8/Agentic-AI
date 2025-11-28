import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def connect_db():
    return sqlite3.connect('restaurant.db')

def get_orders():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    return df

st.title("Grok Eats Dashboard")

orders_df = get_orders()
st.write("Orders Table:")
st.dataframe(orders_df)

# Basic Chart: Orders by Status
if not orders_df.empty:
    status_counts = orders_df['orderstatus'].value_counts()
    fig, ax = plt.subplots()
    status_counts.plot(kind='bar', ax=ax)
    ax.set_title("Orders by Status")
    ax.set_xlabel("Status")
    ax.set_ylabel("Count")
    st.pyplot(fig)
else:
    st.write("No orders yet.")