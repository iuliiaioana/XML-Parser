from parser import activities
from datetime import date
import pandas as pd
import streamlit as st
import numpy as np
import pydeck as pdk


df_activities = pd.DataFrame([a.__dict__ for a in activities])


def show_map(custom=None):
    locations = {
        "Bucharest": {
            "lat": 44.439663,
            "lon": 26.096306
        },
        "Brasov": {
            "lat": 45.657974,
            "lon": 25.601198
        },
        "Cluj": {
            "lat": 46.770439,
            "lon": 23.591423
        },
        "Iasi": {
            "lat": 47.151726,
            "lon": 27.587914
        }
    }
    def find_lon(city): return locations[city]['lon']
    def find_lat(city): return locations[city]['lat']
    df_activities['lon'] = df_activities['location'].apply(find_lon)
    df_activities['lat'] = df_activities['location'].apply(find_lat)
    view_ro = pdk.ViewState(
        latitude=45.56,
        longitude=25,
        zoom=5.5
    )
    if custom:
        df = df_activities.loc[df_activities['location'] == custom]
        layer = pdk.Layer(
            type='HeatmapLayer',
            data=df,
            pickable=True,
            opacity=0.9,
            get_position=["lon", "lat"],
            get_radius=200,
        )
    else:
        layer = pdk.Layer(
            type='HeatmapLayer',
            data=df_activities,
            pickable=True,
            opacity=0.9,
            get_position=["lon", "lat"],
            get_radius=200,
        )
    r = pdk.Deck(layers=[layer], initial_view_state=view_ro,
                 height=800, tooltip=True)

    st.pydeck_chart(r)


st.set_page_config(
    page_title="XPARSER",
    page_icon="🎄",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("🎄Activities for Christmas🎄🎁")
show = pd.DataFrame({
    'options1': ['All Activities', 'Activities on a day', 'Activities based on category', 'Activities based on location', 'Activities by price', 'Activities by organizer', 'Custom Search']
})

option = st.sidebar.selectbox('Show:', show['options1'])

if option == "All Activities":
    st.table(df_activities)
elif option == "Activities on a day":
    date_selected = st.sidebar.date_input(
        'Day are you searching for:', date.today())
    st.write("Activities from date: ", date_selected)
    by_date = []
    for activity in activities:
        if activity.day == str(date_selected):
            by_date.append(activity)

    if by_date:
        st.table(pd.DataFrame([t.__dict__ for t in by_date]))
    else:
        st.subheader('No activities for this day!')
elif option == "Activities based on category":
    categories = pd.DataFrame({
        'options': ['Family', 'Children', 'Teens', 'All']})
    category_selected = st.sidebar.selectbox(
        'Select category:', categories['options'])
    if category_selected == 'All':
        st.table(df_activities)
        df_chart = df_activities.groupby(
            ['category']).size().to_frame(name='category_count')
        st.bar_chart(df_chart, height=500)
    else:
        by_category = []
        for activity in activities:
            if activity.category == category_selected.lower():
                by_category.append(activity)
        if by_category:
            st.table(pd.DataFrame([c.__dict__ for c in by_category]))
        else:
            st.subheader('No activities for this category!')
elif option == "Activities by organizer":
    organizers = pd.DataFrame({
        'options': ['All', 'CinemaCity', 'IBM', '341A3', 'Salvati Copii']})
    organizer_selected = st.sidebar.selectbox(
        'Select organizer:', organizers['options'])
    if organizer_selected == 'All':
        st.table(df_activities)
        df_chart = df_activities.groupby(
            ['organizer']).size().to_frame(name='organizer_count')
        st.bar_chart(df_chart, height=500)
    else:
        by_organizer = []
        for activity in activities:
            if activity.organizer == organizer_selected:
                by_organizer.append(activity)
        if by_organizer:
            st.table(pd.DataFrame([c.__dict__ for c in by_organizer]))
        else:
            st.subheader('No activities for this organizer!')
elif option == "Activities by price":
    price_range = st.sidebar.slider("Choose a price range:", value=[0, 100])
    st.info("The range was: " +
            str(price_range[0]) + ":" + str(price_range[1]))
    by_price = []
    for activity in activities:
        if price_range[0] < int(activity.price) < price_range[1]:
            by_price.append(activity)
    if by_price:
        st.table(pd.DataFrame([c.__dict__ for c in by_price]))
    else:
        st.subheader('No activities for this price range!')
elif option == "Activities based on location":
    locations = pd.DataFrame({
        'options': ['Bucharest', 'Brasov', 'Cluj', 'All']})
    location_selected = st.sidebar.selectbox(
        'Select city:', locations['options'])
    if location_selected == 'All':
        show_map()
    else:
        by_location = []
        for activity in activities:
            if activity.location == location_selected:
                by_location.append(activity)
        if by_location:
            st.table(pd.DataFrame([c.__dict__ for c in by_location]))
        else:
            st.subheader('No activities for this location!')
elif option == 'Custom Search':
    agree = st.sidebar.checkbox('Show Map')
    price_range = st.sidebar.slider("Choose a price range:", value=[0, 100])
    categories = pd.DataFrame({
        'options': ['Family', 'Children', 'Teens', 'All']})
    category_selected = st.sidebar.selectbox(
        'Select category:', categories['options'])
    date_selected = st.sidebar.date_input(
        'Day are you searching for:')
    locations = pd.DataFrame({
        'options': ['Bucharest', 'Brasov', 'Cluj', 'All']})
    location_selected = st.sidebar.selectbox(
        'Select city:', locations['options'])
    by_price = set()
    by_location = set()
    by_category = set()
    by_date = set()
    for activity in activities:
        if price_range[0] < int(activity.price) < price_range[1]:
            by_price.add(activity)
        if activity.location == location_selected or location_selected == 'All':
            by_location.add(activity)
        if activity.category == category_selected.lower() or category_selected == 'All':
            by_category.add(activity)
        if activity.day == str(date_selected):
            by_date.add(activity)
    custom_search = set.intersection(
        by_price, by_location, by_category, by_date)
    if agree:
        if location_selected != 'All':
            show_map(location_selected)
        else:
            show_map()
    if custom_search:
        st.table(pd.DataFrame([c.__dict__ for c in custom_search]))
    else:
        st.subheader('No activities found!')
