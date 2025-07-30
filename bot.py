#!/usr/bin/env python3
"""
Insurance Telegram Bot
A Telegram bot for handling insurance-related queries and services.
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
MAIN_MENU, INSURANCE_TYPE, PERSONAL_INFO, QUOTE_DETAILS = range(4)

class InsuranceBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in environment variables")
        
        # Initialize application
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up command and message handlers"""
        
        # Command handlers
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Conversation handler for insurance process
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", self.start_command),
                CommandHandler("quote", self.get_quote),
                CommandHandler("menu", self.main_menu)
            ],
            states={
                MAIN_MENU: [CallbackQueryHandler(self.main_menu_handler)],
                INSURANCE_TYPE: [CallbackQueryHandler(self.insurance_type_handler)],
                PERSONAL_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.personal_info_handler)],
                QUOTE_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.quote_details_handler)]
            },
            fallbacks=[CommandHandler("cancel", self.cancel)]
        )
        
        self.application.add_handler(conv_handler)
        
        # Default message handler
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🏦 Welcome to Insurance Bot! 🏦

I'm here to help you with:
• Get insurance quotes
• Compare different policies
• Answer insurance questions
• Guide you through the process

Use the buttons below to get started!
        """
        await update.message.reply_text(welcome_message)
        return await self.main_menu(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📋 Available Commands:

/start - Start the bot and see welcome message
/menu - Show main menu
/quote - Get an insurance quote
/help - Show this help message
/cancel - Cancel current operation

💡 Tips:
- Use the inline buttons for easier navigation
- Type your questions naturally, I'll try to help!
- All your data is handled securely
        """
        await update.message.reply_text(help_text)
    
    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main menu with options"""
        keyboard = [
            [InlineKeyboardButton("🚗 Auto Insurance", callback_data="auto")],
            [InlineKeyboardButton("🏠 Home Insurance", callback_data="home")],
            [InlineKeyboardButton("❤️ Health Insurance", callback_data="health")],
            [InlineKeyboardButton("✈️ Travel Insurance", callback_data="travel")],
            [InlineKeyboardButton("💼 Business Insurance", callback_data="business")],
            [InlineKeyboardButton("❓ General Questions", callback_data="questions")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message_text = "🎯 What type of insurance are you interested in?"
        
        if update.callback_query:
            await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(message_text, reply_markup=reply_markup)
        
        return MAIN_MENU
    
    async def main_menu_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle main menu selections"""
        query = update.callback_query
        await query.answer()
        
        insurance_types = {
            "auto": "🚗 Auto Insurance",
            "home": "🏠 Home Insurance", 
            "health": "❤️ Health Insurance",
            "travel": "✈️ Travel Insurance",
            "business": "💼 Business Insurance"
        }
        
        if query.data in insurance_types:
            context.user_data['insurance_type'] = query.data
            
            keyboard = [
                [InlineKeyboardButton("📋 Get Quote", callback_data="get_quote")],
                [InlineKeyboardButton("ℹ️ Learn More", callback_data="learn_more")],
                [InlineKeyboardButton("📞 Talk to Agent", callback_data="talk_agent")],
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"You selected: {insurance_types[query.data]}\n\nWhat would you like to do?",
                reply_markup=reply_markup
            )
            return INSURANCE_TYPE
        
        elif query.data == "questions":
            await query.edit_message_text(
                "❓ Ask me any insurance-related question!\n\nI can help with:\n"
                "• Policy explanations\n• Coverage details\n• Claim processes\n• Premium calculations\n\n"
                "Just type your question!"
            )
            return ConversationHandler.END
    
    async def insurance_type_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle insurance type specific actions"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "get_quote":
            await query.edit_message_text(
                "📋 Let's get you a quote!\n\n"
                "I'll need some basic information. Please provide your:\n"
                "1. Full Name\n"
                "2. Age\n"
                "3. Location (City, State)\n\n"
                "Please enter your full name:"
            )
            context.user_data['step'] = 'name'
            return PERSONAL_INFO
        
        elif query.data == "learn_more":
            insurance_type = context.user_data.get('insurance_type', 'insurance')
            info_text = self.get_insurance_info(insurance_type)
            
            keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="back_type")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(info_text, reply_markup=reply_markup)
        
        elif query.data == "talk_agent":
            await query.edit_message_text(
                "📞 Connect with an Agent\n\n"
                "Our agents are available:\n"
                "🕘 Monday-Friday: 8 AM - 8 PM\n"
                "🕘 Saturday: 9 AM - 5 PM\n"
                "🕘 Sunday: 10 AM - 4 PM\n\n"
                "📱 Phone: 1-800-INSURANCE\n"
                "✉️ Email: agents@insurance.com\n\n"
                "Or leave your contact info and we'll call you!"
            )
        
        elif query.data == "back_menu":
            return await self.main_menu(update, context)
        
        elif query.data == "back_type":
            return await self.main_menu_handler(update, context)
    
    def get_insurance_info(self, insurance_type):
        """Get information about specific insurance types"""
        info = {
            "auto": """
🚗 Auto Insurance Information

Coverage Types:
• Liability Coverage - Required by law
• Collision Coverage - Covers vehicle damage
• Comprehensive - Theft, vandalism, weather
• Personal Injury Protection - Medical expenses
• Uninsured Motorist - Protection from uninsured drivers

Factors Affecting Rates:
• Driving record
• Vehicle type and age
• Location
• Coverage limits
• Deductible amount
            """,
            "home": """
🏠 Home Insurance Information

Coverage Types:
• Dwelling Coverage - Structure of your home
• Personal Property - Your belongings
• Liability Protection - Injury/damage claims
• Additional Living Expenses - Temporary housing
• Medical Payments - Guest injuries

What's Typically Covered:
• Fire and smoke damage
• Weather-related damage
• Theft and vandalism
• Water damage (sudden)
            """,
            "health": """
❤️ Health Insurance Information

Plan Types:
• HMO - Health Maintenance Organization
• PPO - Preferred Provider Organization
• EPO - Exclusive Provider Organization
• POS - Point of Service

Key Features:
• Preventive care coverage
• Prescription drug coverage
• Emergency services
• Mental health services
• Maternity coverage
            """,
            "travel": """
✈️ Travel Insurance Information

Coverage Types:
• Trip Cancellation/Interruption
• Medical Emergency Coverage
• Baggage Loss/Delay
• Travel Delay Coverage
• Emergency Evacuation

When to Buy:
• Within 14 days of initial trip payment
• Before departure
• Consider annual plans for frequent travelers
            """,
            "business": """
💼 Business Insurance Information

Essential Coverage:
• General Liability - Customer injury/property damage
• Professional Liability - Errors and omissions
• Property Insurance - Business property protection
• Workers' Compensation - Employee injury coverage
• Cyber Liability - Data breach protection

Industry-Specific Options:
• Product liability
• Commercial auto
• Business interruption
            """
        }
        return info.get(insurance_type, "Information not available for this insurance type.")
    
    async def personal_info_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle personal information collection"""
        step = context.user_data.get('step')
        user_input = update.message.text
        
        if step == 'name':
            context.user_data['name'] = user_input
            context.user_data['step'] = 'age'
            await update.message.reply_text(
                f"Thanks {user_input}! 👋\n\nNow, please enter your age:"
            )
        
        elif step == 'age':
            try:
                age = int(user_input)
                if 18 <= age <= 100:
                    context.user_data['age'] = age
                    context.user_data['step'] = 'location'
                    await update.message.reply_text(
                        "Great! Now please enter your location (City, State):"
                    )
                else:
                    await update.message.reply_text(
                        "Please enter a valid age between 18 and 100:"
                    )
            except ValueError:
                await update.message.reply_text(
                    "Please enter a valid age (numbers only):"
                )
        
        elif step == 'location':
            context.user_data['location'] = user_input
            insurance_type = context.user_data.get('insurance_type', 'insurance')
            
            # Generate quote based on insurance type
            quote = self.generate_quote(context.user_data, insurance_type)
            
            await update.message.reply_text(
                f"🎉 Here's your {insurance_type} insurance quote:\n\n{quote}\n\n"
                "💬 Would you like to:\n"
                "• Adjust coverage options\n"
                "• Talk to an agent\n"
                "• Get quotes for other insurance types\n\n"
                "Just let me know!"
            )
            return ConversationHandler.END
        
        return PERSONAL_INFO
    
    def generate_quote(self, user_data, insurance_type):
        """Generate a sample quote based on user data and insurance type"""
        name = user_data.get('name', 'Customer')
        age = user_data.get('age', 30)
        location = user_data.get('location', 'Unknown')
        
        # Sample quote calculation (in real app, this would use actual pricing algorithms)
        base_rates = {
            'auto': 800,
            'home': 1200,
            'health': 300,
            'travel': 150,
            'business': 2000
        }
        
        base_rate = base_rates.get(insurance_type, 500)
        
        # Age factor
        if age < 25:
            age_factor = 1.3
        elif age < 35:
            age_factor = 1.0
        elif age < 55:
            age_factor = 0.9
        else:
            age_factor = 1.1
        
        estimated_annual = int(base_rate * age_factor)
        estimated_monthly = int(estimated_annual / 12)
        
        quote_text = f"""
👤 Customer: {name}
📍 Location: {location}
🎂 Age: {age}

💰 Estimated Rates:
• Monthly: ${estimated_monthly}
• Annual: ${estimated_annual}

📋 This quote includes:
• Basic coverage options
• Standard deductibles
• Good driver/customer discounts

⚠️ This is an estimate. Final rates may vary based on detailed information and underwriting.
        """
        
        return quote_text
    
    async def get_quote(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quote command"""
        return await self.main_menu(update, context)
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button presses"""
        return await self.main_menu_handler(update, context)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        message_text = update.message.text.lower()
        
        # Simple keyword-based responses
        if any(word in message_text for word in ['quote', 'price', 'cost', 'rate']):
            await update.message.reply_text(
                "💰 Looking for a quote? Use /quote or click the menu button below to get started!"
            )
            return await self.main_menu(update, context)
        
        elif any(word in message_text for word in ['claim', 'accident', 'damage']):
            await update.message.reply_text(
                "🚨 Need to file a claim?\n\n"
                "1. Call our 24/7 claims hotline: 1-800-CLAIMS\n"
                "2. Visit our website: www.insurance.com/claims\n"
                "3. Use our mobile app\n\n"
                "Have your policy number ready!"
            )
        
        elif any(word in message_text for word in ['help', 'support', 'question']):
            return await self.help_command(update, context)
        
        else:
            await update.message.reply_text(
                "🤔 I'm not sure how to help with that specific question.\n\n"
                "Try using /menu to see available options or /help for commands.\n\n"
                "For complex questions, you can always talk to one of our agents!"
            )
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel current operation"""
        await update.message.reply_text(
            "❌ Operation cancelled.\n\nUse /menu to start over or /help for assistance."
        )
        return ConversationHandler.END
    
    async def quote_details_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle additional quote details"""
        # This can be expanded for more detailed quote customization
        pass
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Insurance Bot...")
        
        # Start polling for updates
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function to run the bot"""
    try:
        bot = InsuranceBot()
        bot.run()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print("❌ Error: Please set your TELEGRAM_BOT_TOKEN in the .env file")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
