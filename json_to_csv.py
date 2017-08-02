
import csv
import json
from datetime import datetime

###
# Define the fields to output
# Column name : function that takes a "joined" review
##/   
convert_fields = {
        
		'business_id':lambda r:r['business_id'],
		'user_ID': lambda r:r['user_id'],
		'category': lambda r:r['business'].get('categories'),
		'Open_24hrs': lambda r:r['business'].get('attributes',{}).get('Open 24 Hours'),
		'Rest_review_count': lambda r:r['business'].get('review_count'),
		'accepts_creditCards': lambda r:r['business'].get('attributes',{}).get('Accepts Credit Cards'),
		'sunday_open': lambda r:r['business'].get('attributes',{}).get('Sunday',{}).get('open'),
		'sunday_close': lambda r:r['business'].get('attributes',{}).get('Sunday',{}).get('close'),
		'parking_garage': lambda r:r['business'].get('attributes',{}).get('Parking',{}).get('garage'),
		'parking_valet': lambda r:r['business'].get('attributes',{}).get('Parking',{}).get('valet'),
		'biz_stars': lambda r:r['business'].get('stars'),
		'amb_romantic': lambda r:r['business'].get('attributes',{}).get('Ambience',{}).get('romantic'),
		'amb_trendy': lambda r:r['business'].get('attributes',{}).get('Ambience',{}).get('trendy'),
		'amb_classy': lambda r:r['business'].get('attributes',{}).get('Ambience',{}).get('classy'),
		'amb_intimate': lambda r:r['business'].get('attributes',{}).get('Ambience',{}).get('intimate'),
		'amb_touristy': lambda r:r['business'].get('attributes',{}).get('Ambience',{}).get('touristy'),
		'amb_divey': lambda r:r['business'].get('attributes',{}).get('Ambience',{}).get('divey'),
		'good_for_kids': lambda r:r['business'].get('attributes',{}).get('Good for Kids'),
		'whlChair_access': lambda r:r['business'].get('attributes',{}).get('Wheelchair Accessible'),
		'delivery': lambda r:r['business'].get('attributes',{}).get('Delivery'),
		'dairy_free': lambda r:r['business'].get('attributes',{}).get('Dietary Restrictions',{}).get('dairy-free'),
		'gluten_free': lambda r:r['business'].get('attributes',{}).get('Dietary Restrictions',{}).get('gluten-free'),
		'vegan': lambda r:r['business'].get('attributes',{}).get('Dietary Restrictions',{}).get('vegan'),
		'kosher': lambda r:r['business'].get('attributes',{}).get('Dietary Restrictions',{}).get('kosher'),
		'halal': lambda r:r['business'].get('attributes',{}).get('Dietary Restrictions',{}).get('halal'),
		'attire': lambda r:r['business'].get('attributes',{}).get('Attire'),
		'waiter_service': lambda r:r['business'].get('attributes',{}).get('Waiter Service'),
		'good_for_dessert': lambda r:r['business'].get('attributes',{}).get('Good For',{}).get('dessert'),
		'good_for_dinner': lambda r:r['business'].get('attributes',{}).get('Good For',{}).get('dinner'),
		'good_for_lunch': lambda r:r['business'].get('attributes',{}).get('Good For',{}).get('lunch'),
		'good_for_brunch': lambda r:r['business'].get('attributes',{}).get('Good For',{}).get('brunch'),
		'good_for_latenight': lambda r:r['business'].get('attributes',{}).get('Good For',{}).get('latenight'),
		'good_for_breakfast': lambda r:r['business'].get('attributes',{}).get('Good For',{}).get('breakfast'),
		'takes_reservations': lambda r:r['business'].get('attributes',{}).get('Takes Reservations'),
		'drive_thru': lambda r:r['business'].get('attributes',{}).get('Drive-Thru'),
		'smoking': lambda r:r['business'].get('attributes',{}).get('Smoking'),
		'has_tv': lambda r:r['business'].get('attributes',{}).get('Has TV'),
		'user_review_count': lambda r:r['user'].get('review_count'),
		'user_given_ratings': lambda r:r['stars']
	}


def juxt(*fs):
    """Given a (splatted) list of functions as an argument, return a function
    which takes a single argument and returns a list of the results."""
    return lambda x: [f(x) for f in fs]

###
# main
# Load all of the data, join it, write out in CSV format
##/
print "loading reviews"
with open('review.json', 'rb') as rev_file:
    reviews = map(json.loads, rev_file)

	
print "loading users"
with open('user.json', 'rb') as rev_file:
    users = map(json.loads, rev_file)
user_by_id = dict((u['user_id'], u) for u in users)


print "loading businesses"
with open('business.json', 'rb') as rev_file:
    businesses = map(json.loads, rev_file)
business_by_id = dict((b['business_id'], b) for b in businesses)

print "joining"
full = (dict(r.items()
             + {'user': user_by_id.get(r['user_id'], {})}.items()
             + {'business': business_by_id.get(r['business_id'], {})}.items())
        for r in reviews)

print "writing result"
with open('yelp_academic_dataset_final.txt', 'wb') as full_file:
    writer = csv.writer(full_file)
    writer.writerow(convert_fields.keys())
    converter = juxt(*convert_fields.values())
    writer.writerows(converter(r) for r in full)