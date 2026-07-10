# Testing
# python - <<EOF
# from dealer_intelligence.services.business_listing_service import empty_listing_report
#
# report = empty_listing_report()
#
# print(len(report))
#
# for k,v in list(report.items())[:5]:
#     print(v)
# EOF

BUSINESS_LISTINGS = {

    # Search & Maps
    "google_business_profile": {
        "label": "Google Business Profile",
        "weight": 10
    },
    "bing_places": {
        "label": "Bing Places",
        "weight": 6
    },
    "apple_business_connect": {
        "label": "Apple Business Connect",
        "weight": 6
    },
    "mapquest": {
        "label": "MapQuest",
        "weight": 2
    },

    # Reviews
    "yelp": {
        "label": "Yelp",
        "weight": 8
    },
    "bbb": {
        "label": "Better Business Bureau",
        "weight": 6
    },

    # Citations
    "yellow_pages": {
        "label": "Yellow Pages",
        "weight": 3
    },
    "foursquare": {
        "label": "Foursquare",
        "weight": 3
    },
    "hotfrog": {
        "label": "Hotfrog",
        "weight": 2
    },
    "manta": {
        "label": "Manta",
        "weight": 3
    },
    "merchant_circle": {
        "label": "MerchantCircle",
        "weight": 2
    },
    "ezlocal": {
        "label": "EZlocal",
        "weight": 2
    },
    "brownbook": {
        "label": "Brownbook",
        "weight": 2
    },
    "local_com": {
        "label": "Local.com",
        "weight": 2
    },
    "citysearch": {
        "label": "Citysearch",
        "weight": 2
    },
    "chamber": {
        "label": "Chamber of Commerce",
        "weight": 3
    },
    "showmelocal": {
        "label": "ShowMeLocal",
        "weight": 2
    },
    "elocal": {
        "label": "eLocal",
        "weight": 2
    },
    "cylex": {
        "label": "Cylex",
        "weight": 2
    },
    "alignable": {
        "label": "Alignable",
        "weight": 2
    }
}