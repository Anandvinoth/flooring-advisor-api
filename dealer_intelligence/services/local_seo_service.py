def analyze_local_seo(metadata: dict, site_scan: dict) -> dict:
    checks = {
        "city_in_title": {
            "passed": metadata["city"].lower() in metadata["title"].lower(),
            "points": 20,
            "recommendation": "Add the city name to the page title.",
        },
        "city_in_meta_description": {
            "passed": metadata["city"].lower()
            in metadata["meta_description"].lower(),
            "points": 15,
            "recommendation": "Add the city name to the meta description.",
        },
        "city_in_h1": {
            "passed": any(
                metadata["city"].lower() in h1.lower()
                for h1 in metadata["h1"]
            ),
            "points": 15,
            "recommendation": "Add the city name to the main H1 heading.",
        },
        "local_business_schema": {
            "passed": "LocalBusiness" in site_scan["schema_types"],
            "points": 20,
            "recommendation": "Add LocalBusiness structured data.",
        },
        "city_mentions": {
            "passed": metadata["city_mentions"] >= 3,
            "points": 15,
            "recommendation": "Add stronger local service-area content.",
        },
        "contact_signal": {
            "passed": site_scan["has_contact_text"],
            "points": 10,
            "recommendation": "Add a clear contact or showroom section.",
        },
        "state_signal": {
            "passed": site_scan["has_state_text"],
            "points": 5,
            "recommendation": "Add the state name or abbreviation to the page.",
        },
    }

    earned_points = sum(
        check["points"]
        for check in checks.values()
        if check["passed"]
    )

    recommendations = [
        check["recommendation"]
        for check in checks.values()
        if not check["passed"]
    ]

    return {
        "category": "Local SEO",
        "score": earned_points,
        "earned_points": earned_points,
        "available_points": 100,
        "checks": checks,
        "recommendations": recommendations,
    }