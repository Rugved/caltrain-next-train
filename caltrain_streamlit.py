import streamlit as st
import datetime
import requests
from bs4 import BeautifulSoup

# Global schedule list
train_schedule = []

# Scrape train data from Caltrain site (example only — actual scraping will depend on structure)
def fetch_schedule():
    url = "https://www.caltrain.com/schedules/weekday-southbound.html"  # example URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    global train_schedule
    train_schedule = []

    for row in soup.select('table tbody tr'):
        columns = row.find_all('td')
        if len(columns) > 0:
            sf_time = columns[1].text.strip()  # San Francisco column
            hillsdale_time = columns[8].text.strip()  # Hillsdale column
            if sf_time and hillsdale_time:
                train_schedule.append(sf_time)

# Get next train time
def get_next_train():
    now = datetime.datetime.now().time()
    for time_str in train_schedule:
        try:
            train_time = datetime.datetime.strptime(time_str, "%I:%M %p").time()
            if train_time > now:
                return f"Next train departs at: {time_str}"
        except ValueError:
            continue
    return "No more trains today."

# Streamlit UI
st.set_page_config(page_title="Next Caltrain", layout="centered")
st.title("🚆 Next Caltrain: SF ➝ Hillsdale")

if st.button("🔄 Sync Schedule"):
    fetch_schedule()
    st.success("Schedule updated!")

if not train_schedule:
    fetch_schedule()

next_train = get_next_train()
st.subheader(next_train)
