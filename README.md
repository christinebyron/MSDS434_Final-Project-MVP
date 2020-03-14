# MSDS434_Final-Project-MVP

![citi bike](https://github.com/christinebyron/MSDS434_Final-Project-MVP/blob/master/Images/citi%20bike.jpg)

This final project consists of a cloud-native analytics application that is hosted on the Google Cloud Platform (GCP). The goal of this project is to demonstrate the ability to create realistic, working solution that is created with modern techniques.

## Product Overview
Using the agile methodology, our project team developed a real-time recommendation application to increase the user interaction and enrich shopping potential for our Customer user type. In this 10 week MVP, we utilized demographic data from customers, as well as information from previous purchases and user behavior to predict which pass our daily rider should select. 

## Data Understanding 
Our product utilizes the Citi Bike daily ridership and membership data hosted in Google BigQuery. This dataset consists of the trips collected since its launch in September 2013, and is updated daily. It is important to note that the data has been processed by Citi Bike to remove all trips that are taken by staff to service and inspect the system, as well as any trips below 60 seconds in length, which are considered false starts.

The data includes:
   *	Trip Duration (seconds)
•	Start Time and Date
•	Stop Time and Date
•	Start Station Name
•	End Station Name
•	Station ID
•	Station Lat/Long
•	Bike ID
•	User Type (Customer = 24-hour pass or 3-day pass user; Subscriber = Annual Member)
•	Gender (Zero = unknown; 1 = male; 2 = female)
•	Year of Birth
