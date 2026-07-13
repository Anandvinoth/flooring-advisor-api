from urllib.parse import urlparse


PAGE_RULES = {
    "homepage": [""],
    "about": ["about"],
    "contact": ["contact"],
    "reviews": ["review", "customer-review"],
    "location": ["location"],
    "financing": ["financing"],
    "services": ["service"],
    "inspiration": ["blog", "inspiration"],
    "product_category": [
        "/p/",
        "carpet",
        "hardwood",
        "laminate",
        "luxury-vinyl",
        "waterproof",
    ],
}


def classify_page(url: str) -> str:
    path = urlparse(url).path.lower().strip("/")

    if path == "":
        return "homepage"

    for page_type, patterns in PAGE_RULES.items():
        for pattern in patterns:
            if pattern and pattern in path:
                return page_type

    return "other"