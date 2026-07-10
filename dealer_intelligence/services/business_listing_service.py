from dealer_intelligence.config.business_listings import BUSINESS_LISTINGS


def empty_listing_report():

    report = {}

    for key, value in BUSINESS_LISTINGS.items():

        report[key] = {
            "label": value["label"],
            "status": "UNKNOWN",
            "score": 0,
            "recommendation": ""
        }

    return report