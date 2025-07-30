#!/usr/bin/env python3
"""
Test script for the Insurance Telegram Bot
Run this to test basic functionality before deploying
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-telegram-bot: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Config: {e}")
        return False
    
    try:
        from utils import QuoteCalculator
        print("✅ Utils module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Utils: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration setup"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import Config
        
        # Check if .env file exists
        if os.path.exists('.env'):
            print("✅ .env file exists")
        else:
            print("⚠️  .env file not found - create one with your bot token")
        
        # Test token presence (without revealing it)
        if Config.TELEGRAM_BOT_TOKEN:
            if Config.TELEGRAM_BOT_TOKEN == 'your_bot_token_here':
                print("⚠️  Please update your bot token in .env file")
            else:
                print("✅ Bot token is configured")
        else:
            print("❌ Bot token not found in environment variables")
            return False
        
        print(f"✅ Debug mode: {Config.DEBUG}")
        print(f"✅ Log level: {Config.LOG_LEVEL}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_quote_calculator():
    """Test quote calculation functionality"""
    print("\n💰 Testing quote calculator...")
    
    try:
        from utils import QuoteCalculator
        
        # Test data
        test_user_data = {
            'name': 'Test User',
            'age': 30,
            'location': 'Test City, TS'
        }
        
        # Test each insurance type
        for insurance_type in ['auto', 'home', 'health', 'travel', 'business']:
            quote = QuoteCalculator.calculate_quote(insurance_type, test_user_data)
            
            if quote and 'monthly_premium' in quote and 'annual_premium' in quote:
                print(f"✅ {insurance_type.capitalize()} insurance quote: ${quote['monthly_premium']}/month")
            else:
                print(f"❌ Failed to calculate {insurance_type} insurance quote")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Quote calculator test failed: {e}")
        return False

def test_utilities():
    """Test utility functions"""
    print("\n🛠️  Testing utilities...")
    
    try:
        from utils import (
            validate_email, validate_phone, format_currency,
            calculate_age_factor, parse_location, get_insurance_emoji
        )
        
        # Test email validation
        if validate_email('test@example.com') and not validate_email('invalid-email'):
            print("✅ Email validation working")
        else:
            print("❌ Email validation failed")
            return False
        
        # Test phone validation
        if validate_phone('555-123-4567') and not validate_phone('invalid'):
            print("✅ Phone validation working")
        else:
            print("❌ Phone validation failed")
            return False
        
        # Test currency formatting
        formatted = format_currency(1234.56)
        if formatted == '$1,234.56':
            print("✅ Currency formatting working")
        else:
            print(f"❌ Currency formatting failed: {formatted}")
            return False
        
        # Test age factor calculation
        factor = calculate_age_factor(30)
        if isinstance(factor, float) and factor > 0:
            print("✅ Age factor calculation working")
        else:
            print("❌ Age factor calculation failed")
            return False
        
        # Test location parsing
        location = parse_location('New York, NY')
        if location['city'] == 'New York' and location['state'] == 'NY':
            print("✅ Location parsing working")
        else:
            print("❌ Location parsing failed")
            return False
        
        # Test insurance emoji
        emoji = get_insurance_emoji('auto')
        if emoji == '🚗':
            print("✅ Insurance emoji working")
        else:
            print("❌ Insurance emoji failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Utilities test failed: {e}")
        return False

def test_bot_initialization():
    """Test bot initialization without starting it"""
    print("\n🤖 Testing bot initialization...")
    
    try:
        from bot import InsuranceBot
        
        # This will test if the bot can be initialized
        # but won't start the actual polling
        bot = InsuranceBot()
        
        if bot.application and bot.token:
            print("✅ Bot initialized successfully")
            return True
        else:
            print("❌ Bot initialization failed")
            return False
            
    except ValueError as e:
        print(f"❌ Bot initialization failed: {e}")
        print("💡 Make sure your TELEGRAM_BOT_TOKEN is set in .env file")
        return False
    except Exception as e:
        print(f"❌ Bot initialization failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Insurance Bot Tests\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Configuration Tests", test_configuration),
        ("Quote Calculator Tests", test_quote_calculator),
        ("Utility Tests", test_utilities),
        ("Bot Initialization Tests", test_bot_initialization)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running {test_name}")
        print('='*50)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n{'='*50}")
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("💡 Run 'python bot.py' to start your bot")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the bot.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
