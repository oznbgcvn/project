#!/usr/bin/env python
# coding: utf-8

# In[3]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[4]:


tesla=yf.Ticker("TSLA")


# In[5]:


tesla_data=tesla.history(period="max")


# In[6]:


tesla_data.reset_index(inplace=True)
tesla_data.head(5)


# In[7]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text


# In[8]:


soup = BeautifulSoup(html_data)


# In[9]:


data = []
for table in soup.find_all("table"):
    
    if any(["Tesla Quarterly Revenue".lower() in th.text.lower() for th in table.find_all("th")]):
        for row in table.find("tbody").find_all("tr"):
            date_col, rev_col = [col for col in row.find_all("td")]
            data.append({
                "Date": date_col.text,
                "Revenue": rev_col.text
            })

tesla_revenue = pd.DataFrame(data)


# In[ ]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")


# In[ ]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[ ]:


tesla_revenue.tail(5)


# In[16]:


gme = yf.Ticker("GME")


# In[17]:


gme_data = gme.history(period="max")


# In[18]:


gme_data.reset_index(inplace=True)
gme_data.head()


# In[19]:


url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text


# In[20]:


soup = BeautifulSoup(html_data)


# In[21]:


data = []
for table in soup.find_all("table"):
    
    if any(["GameStop Quarterly Revenue".lower() in th.text.lower() for th in table.find_all("th")]):
        for row in table.find("tbody").find_all("tr"):
            date_col, rev_col = [col for col in row.find_all("td")]
            data.append({
                "Date": date_col.text,
                "Revenue": rev_col.text.replace("$", "").replace(",", "")
            })

gme_revenue = pd.DataFrame(data)


# In[22]:


gme_revenue.tail()


# In[ ]:


make_graph(tesla_data, tesla_revenue, 'Telsa (revenue vs. price comparison)')


# In[ ]:


make_graph(gme_data, gme_revenue, 'GameStop')

