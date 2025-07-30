"""
Utility functions for the Insurance Telegram Bot
"""

import re
from datetime import datetime
from typing import Dict, Any, Optional

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    # Check if it's a valid US phone number (10 or 11 digits)
    return len(digits_only) in [10, 11]

def format_currency(amount: float, currency: str = 'USD') -> str:
    """Format currency amount"""
    if currency == 'USD':
        return f"${amount:,.2f}"
    return f"{amount:,.2f} {currency}"

def calculate_age_factor(age: int) -> float:
    """Calculate age factor for insurance pricing"""
    if age < 25:
        return 1.3  # Higher risk
    elif age < 35:
        return 1.0  # Standard
    elif age < 55:
        return 0.9  # Lower risk
    else:
        return 1.1  # Slightly higher risk

def parse_location(location: str) -> Dict[str, str]:
    """Parse location string into city and state"""
    parts = [part.strip() for part in location.split(',')]
    if len(parts) >= 2:
        return {'city': parts[0], 'state': parts[1]}
    return {'city': location, 'state': ''}

def get_insurance_emoji(insurance_type: str) -> str:
    """Get emoji for insurance type"""
    emojis = {
        'auto': '🚗',
        'home': '🏠',
        'health': '❤️',
        'travel': '✈️',
        'business': '💼'
    }
    return emojis.get(insurance_type, '📋')

def format_business_hours(hours_dict: Dict[str, str]) -> str:
    """Format business hours for display"""
    return f"""
🕘 Monday-Friday: {hours_dict.get('monday_friday', 'N/A')}
🕘 Saturday: {hours_dict.get('saturday', 'N/A')}
🕘 Sunday: {hours_dict.get('sunday', 'N/A')}
    """.strip()

def log_user_interaction(user_id: int, action: str, data: Optional[Dict[str, Any]] = None):
    """Log user interactions for analytics"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'user_id': user_id,
        'action': action,
        'data': data or {}
    }
    # In a production app, this would write to a database or log file
    print(f"[USER_INTERACTION] {log_entry}")

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\';]', '', text)
    return sanitized.strip()

def generate_quote_id() -> str:
    """Generate a unique quote ID"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"QT{timestamp}"

class QuoteCalculator:
    """Class for calculating insurance quotes"""
    
    BASE_RATES = {
        'auto': 800,
        'home': 1200,
        'health': 300,
        'travel': 150,
        'business': 2000
    }
    
    @classmethod
    def calculate_quote(cls, insurance_type: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate insurance quote based on user data"""
        base_rate = cls.BASE_RATES.get(insurance_type, 500)
        age = user_data.get('age', 30)
        
        # Apply age factor
        age_factor = calculate_age_factor(age)
        annual_premium = int(base_rate * age_factor)
        monthly_premium = int(annual_premium / 12)
        
        return {
            'quote_id': generate_quote_id(),
            'insurance_type': insurance_type,
            'annual_premium': annual_premium,
            'monthly_premium': monthly_premium,
            'currency': 'USD',
            'valid_until': cls._get_validity_date(),
            'factors_applied': ['age_factor']
        }
    
    @staticmethod
    def _get_validity_date() -> str:
        """Get quote validity date (30 days from now)"""
        from datetime import datetime, timedelta
        validity_date = datetime.now() + timedelta(days=30)
        return validity_date.strftime("%Y-%m-%d")

def format_quote_display(quote_data: Dict[str, Any], user_data: Dict[str, Any]) -> str:
    """Format quote data for display"""
    name = user_data.get('name', 'Customer')
    age = user_data.get('age', 'N/A')
    location = user_data.get('location', 'N/A')
    
    insurance_emoji = get_insurance_emoji(quote_data['insurance_type'])
    
    return f"""
{insurance_emoji} Insurance Quote - {quote_data['quote_id']}

👤 Customer: {name}
🎂 Age: {age}
📍 Location: {location}

💰 Estimated Premiums:
• Monthly: {format_currency(quote_data['monthly_premium'])}
• Annual: {format_currency(quote_data['annual_premium'])}

📅 Quote valid until: {quote_data['valid_until']}

⚠️ This is an estimate. Final rates may vary based on detailed underwriting.
    """.strip()
