# src/domain_examples.py

DOMAIN_EXAMPLES = [
    {
        "description": "Office Supplies - Paper, Pens, and Stationery",
        "supplier": "Office Depot",
        "code": "44101500",
        "confidence": 0.95,
        "explanation": "Clear office supplies category with common items"
    },
    {
        "description": "IT Hardware - Laptop Computer",
        "supplier": "Dell Technologies",
        "code": "43211500",
        "confidence": 0.98,
        "explanation": "Specific IT hardware with clear supplier context"
    },
    {
        "description": "Professional Services - Consulting",
        "supplier": "McKinsey & Company",
        "code": "80101500",
        "confidence": 0.92,
        "explanation": "Professional services with well-known consulting firm"
    },
    {
        "description": "Software License - Microsoft Office",
        "supplier": "Microsoft",
        "code": "43232500",
        "confidence": 0.97,
        "explanation": "Software license with specific product"
    },
    {
        "description": "Facility Maintenance - Cleaning Services",
        "supplier": "Jan-Pro Cleaning",
        "code": "76101500",
        "confidence": 0.94,
        "explanation": "Facility services with clear maintenance context"
    },
    {
        "description": "Travel Expenses - Hotel Accommodation",
        "supplier": "Marriott Hotels",
        "code": "72101500",
        "confidence": 0.96,
        "explanation": "Travel-related expense with specific accommodation"
    },
    {
        "description": "Marketing Services - Digital Advertising",
        "supplier": "Google Ads",
        "code": "82101500",
        "confidence": 0.93,
        "explanation": "Marketing services with digital focus"
    },
    {
        "description": "Equipment Rental - Construction Machinery",
        "supplier": "Caterpillar",
        "code": "53101500",
        "confidence": 0.95,
        "explanation": "Equipment rental with specific industry context"
    }
]

# Add validation rules for different categories
VALIDATION_RULES = {
    "IT_HARDWARE": {
        "keywords": ["computer", "laptop", "server", "hardware", "equipment"],
        "suppliers": ["dell", "hp", "lenovo", "cisco"],
        "min_confidence": 0.85
    },
    "SOFTWARE": {
        "keywords": ["software", "license", "subscription", "saas"],
        "suppliers": ["microsoft", "adobe", "oracle", "salesforce"],
        "min_confidence": 0.90
    },
    "PROFESSIONAL_SERVICES": {
        "keywords": ["consulting", "services", "professional", "advisory"],
        "suppliers": ["mckinsey", "bain", "bcg", "deloitte"],
        "min_confidence": 0.88
    }
}