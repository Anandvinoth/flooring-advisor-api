#TESTING
# python -c "
# from dealer_intelligence.config.scoring_model import SCORING_MODEL
# print('Categories:', len(SCORING_MODEL))
# print('Scoring model OK')
# "

SCORING_MODEL = {
    # Website
    "website_health": {"label": "Website Health", "weight": 1.0},
    "technical_seo": {"label": "Technical SEO", "weight": 1.0},
    "crawlability": {"label": "Crawlability", "weight": 1.0},
    "indexation_health": {"label": "Indexation Health", "weight": 1.0},
    "performance": {"label": "Performance", "weight": 1.0},
    "core_web_vitals": {"label": "Core Web Vitals", "weight": 1.0},
    "mobile_experience": {"label": "Mobile Experience", "weight": 1.0},
    "accessibility": {"label": "Accessibility", "weight": 1.0},
    "security": {"label": "Security", "weight": 1.0},

    # SEO
    "seo_visibility": {"label": "SEO Visibility", "weight": 1.0},
    "local_seo": {"label": "Local SEO", "weight": 1.0},
    "structured_data": {"label": "Schema & Structured Data", "weight": 1.0},
    "internal_linking": {"label": "Internal Linking", "weight": 1.0},
    "image_seo": {"label": "Image SEO", "weight": 1.0},
    "duplicate_content": {"label": "Duplicate Content", "weight": 1.0},
    "content_quality": {"label": "Content Quality", "weight": 1.0},
    "content_freshness": {"label": "Content Freshness", "weight": 1.0},

    # AI
    "ai_readiness": {"label": "AI Readiness", "weight": 1.0},
    "ai_discoverability": {"label": "AI Discoverability", "weight": 1.0},
    "entity_optimization": {"label": "Entity Optimization", "weight": 1.0},

    # Local presence
    "business_listings": {"label": "Business Listings", "weight": 1.0},
    "reviews_reputation": {"label": "Reviews & Reputation", "weight": 1.0},
    "brand_association": {"label": "Brand Association", "weight": 1.0},
    "social_presence": {"label": "Social Presence", "weight": 1.0},

    # Business
    "dealer_profile": {"label": "Dealer Profile Completeness", "weight": 1.0},
    "competitive_position": {"label": "Competitive Position", "weight": 1.0},
}

MAX_CATEGORY_SCORE = 100