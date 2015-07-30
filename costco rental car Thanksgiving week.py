
# coding: utf-8

# In[99]:

from selenium import webdriver
import urllib
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time as time
import datetime as dt
from lxml import html
# import dependencies


# In[100]:

#use selenium to key in the rental car parameters
browser = webdriver.Firefox() #I only tested in firefox
browser.get('http://costcotravel.com/Rental-Cars')
browser.implicitly_wait(5)#wait for webpage download
browser.find_element_by_xpath('//div/input[@id="pickupAirportTextWidget"]').send_keys('PHX')
browser.implicitly_wait(5) #wait for the airport suggestion box to show
browser.find_element_by_xpath('//li[@class="sayt-result"]').click() 
#click the  airport suggestion box 

browser.find_element_by_xpath('//input[@id="pickupDateWidget"]').send_keys('11/21/2015')
browser.find_element_by_xpath('//input[@id="dropoffDateWidget"]').send_keys('11/29/2015',Keys.RETURN)

browser.find_element_by_xpath('//select[@id="pickupTimeWidget"]/option[@value="11:00 AM"]').click()
browser.find_element_by_xpath('//select[@id="dropoffTimeWidget"]/option[@value="05:00 PM"]').click()
browser.implicitly_wait(5) #wait for the clicks to be completed
browser.find_element_by_link_text('SEARCH').click()
#click the search box

time.sleep(8) #wait for firefox to download and render the page
n = browser.page_source #grab the html source code


# In[14]:


soup = BeautifulSoup(n) #we use bs here


# In[137]:

#grab all the tags of interest (from the main table, the cells that display the car class)

#exclude the first row about vendor and put into a list
all_tags = [i for i in soup.findAll('th',{"class":"tar"}) if i.text.startswith('Tax')==False]

masterlist = []
#go to the entir row, grab all the text of that rows, and clean it up (replace, split....) 
for i in range(len(all_tags)):
    masterlist.append(str(all_tags[i].findParent().text).replace('Not Available','$NA').replace(',','').split('$'))
#create dataframe from masterlist
df = pd.DataFrame(masterlist)
#clean up the name of the columns
df.columns= [['car class', 'Alamo','Avis', 'Budget','Enterprise']]
#calc the days away from first date of rental 11/21/2015 at 11AM
df['days away']= abs((dt.datetime.now()-dt.datetime(2015,11,21,11)).days)
#setup the index. Will do groupby later?
df = df.set_index(['days away','car class'])


# In[138]:

#save current df
df.to_csv('data/%s.csv' %dt.datetime.now().strftime("%m-%d-%H-%M%p"))


# In[144]:

#open up master df, then append it with current df
master= pd.read_csv('data/master.csv',index_col=[0,1])
master = pd.concat([master, df])
master.to_csv('data/master.csv')

