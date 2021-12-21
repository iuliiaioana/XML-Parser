from parser import activities
from datetime import date
import pandas as pd
import streamlit as st
import numpy as np
import pydeck as pdk


def show_map():
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


df_activities = pd.DataFrame([a.__dict__ for a in activities])

st.set_page_config(
    page_title="XPARSER",
    page_icon="🎄",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("🎄Activities for Christmas🎄🎁")
show = pd.DataFrame({
    'options1': ['All Activities', 'Activities on a day', 'Activities based on category', 'Activities based on location', 'Activities by price', 'Custom search']
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
        'options': ['family', 'children', 'teens', 'All']})
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
            if activity.category == category_selected:
                by_category.append(activity)
        if by_category:
            st.table(pd.DataFrame([c.__dict__ for c in by_category]))
        else:
            st.subheader('No activities for this category!')
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
    categories = pd.DataFrame({
        'options': ['Bucharest', 'Brasov', 'Cluj', 'All']})
    category_selected = st.sidebar.selectbox(
        'Select city:', categories['options'])
    if category_selected == 'All':
        show_map()
    else:
        by_location = []
        for activity in activities:
            if activity.location == category_selected:
                by_location.append(activity)
        if by_location:
            st.table(pd.DataFrame([c.__dict__ for c in by_location]))
        else:
            st.subheader('No activities for this location!')
