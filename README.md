# Snout Scheduler
## SDEV220 Group 4 - Final Project
Welcome to our repository for our pet groomer scheduling app! This app allows customers to enter their information and schedule an appointment with the pet groomer, as well as shows the upcoming appointments for the groomer. 

## Getting Started
In order to get the app running on your own machine, you first need to clone the repository to your computer.
Open up a terminal and use `cd` to navigate to the directory where you want the files to be cloned. Then run the following command:

`git clone https://github.com/js2783/SnoutScheduler.git`

Use `cd` again to navigate inside the root directory "SnoutScheduler"

## Dependencies
There is only one dependency required for our app, and that's Django.\
But first, create the virtual environment by running this command (while still in the root directory):

`python -m venv .venv`

Then activate the virtual environment by running:

`source .venv/bin/activate`

Now you are ready to install the dependencies. Run the following command:

`pip install -r requirements.txt`

## Running the Django server
Congrats! You are ready to start the server. Use one more command to get things up and running:

`python manage.py runserver`

Your server should be running. You'll see a link in the terminal after "Starting development server at", copy that link into your web browser and hit enter.

## Navigating the Interface
The first thing you will see is the bookings page. Here is the list of scheduled appointments, showing the customer name, phone number, pet name, date, time, reference ID, and actions to view or delete entry. You will also see a big green button to create new booking. Let's click that next.

![SnoutScheduler home page](<readme assets/home_page.png>)

## New Booking Page
Here you will see many fields that need to be filled with customer, pet, and time information. Go ahead and fill out the fields with the correct information, carefully selecting the time and date that works for you!\
After filling out all fields, click 'Submit Booking' at the bottom of the page to save your appointment. The newly created appointment will now appear on the home page.

![SnoutScheduler booking page](<readme assets/booking_page.png>)