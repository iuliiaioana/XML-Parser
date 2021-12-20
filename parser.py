import xml.etree.ElementTree as ET
from model import Activity

mytree = ET.parse('activities.xml')
myroot = mytree.getroot()
activities = []

for elem in myroot[0].findall('activity'):
    title = elem.find('title').text
    day = elem.find('day').text
    organizer = elem.find('organizer').text
    price = elem.find('price').text
    location = elem.find('location').text
    category = elem.attrib['category']
    activity = Activity(title, day, organizer, price, location, category)
    activities.append(activity)
