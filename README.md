# Insurance Telegram Bot 🏦🤖

A comprehensive Telegram bot for insurance services, built with Python and the python-telegram-bot library.

## Features ✨

- **Multi-Insurance Support**: Auto, Home, Health, Travel, and Business insurance
- **Interactive Menus**: Easy-to-use inline keyboards
- **Quote Generation**: Get instant insurance quotes
- **Information Hub**: Learn about different insurance types
- **Agent Connection**: Connect with human agents
- **Conversation Flow**: Guided insurance application process

## Prerequisites 📋

- Python 3.8 or higher
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- Virtual environment (recommended)

## Installation 🚀

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd insurance-bot-python
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env` (if exists) or create a `.env` file
   - Add your Telegram bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   DEBUG=True
   LOG_LEVEL=INFO
   ```

## Getting a Telegram Bot Token 🔑

1. Start a chat with [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "My Insurance Bot")
4. Choose a username for your bot (must end with 'bot', e.g., "myinsurance_bot")
5. Copy the token provided by BotFather
6. Paste it in your `.env` file

## Usage 🎯

1. **Start the bot**
   ```bash
   python bot.py
   ```

2. **Find your bot on Telegram**
   - Search for your bot username
   - Send `/start` to begin

3. **Available Commands**
   - `/start` - Welcome message and main menu
   - `/menu` - Show main menu
   - `/quote` - Get an insurance quote
   - `/help` - Show help information
   - `/cancel` - Cancel current operation

## Bot Structure 🏗️

```
insurance-bot-python/
├── bot.py          # Main bot application
├── config.py       # Configuration settings
├── utils.py        # Utility functions
├── requirements.txt # Python dependencies
├── .env           # Environment variables (create this)
└── README.md      # This file
```

## Key Features Explained 🔍

### 1. Interactive Menus
- Inline keyboards for easy navigation
- Context-aware responses
- Smooth conversation flow

### 2. Quote System
- Collects user information (name, age, location)
- Calculates estimates based on insurance type
- Provides detailed quote breakdown

### 3. Insurance Types Supported
- 🚗 **Auto Insurance**: Liability, collision, comprehensive
- 🏠 **Home Insurance**: Property, liability, personal belongings
- ❤️ **Health Insurance**: HMO, PPO, EPO plans
- ✈️ **Travel Insurance**: Trip protection, medical coverage
- 💼 **Business Insurance**: Liability, property, workers' comp

### 4. Information System
- Detailed explanations for each insurance type
- Coverage options and factors affecting rates
- Educational content for users

## Customization 🎨

### Adding New Insurance Types
1. Add the type to `SUPPORTED_INSURANCE_TYPES` in `config.py`
2. Add information in the `get_insurance_info()` method
3. Add base rate in `QuoteCalculator.BASE_RATES`
4. Add emoji in `get_insurance_emoji()` function

### Modifying Quote Calculation
- Edit the `QuoteCalculator` class in `utils.py`
- Adjust `BASE_RATES` for different pricing
- Modify `calculate_age_factor()` for age-based pricing
- Add new factors (location, coverage type, etc.)

### Styling Messages
- Update message templates in the bot handlers
- Modify emojis and formatting
- Add new inline keyboard layouts

## Security Considerations 🔒

- Never commit your `.env` file to version control
- Use environment variables for sensitive data  
- Validate and sanitize user inputs
- Implement rate limiting for production use
- Consider using webhooks instead of polling for production

## Deployment Options 🌐

### Local Development
- Run directly with `python bot.py`
- Use ngrok for webhook testing

### Production Deployment
- **Heroku**: Easy deployment with git
- **AWS EC2**: More control and scalability
- **Docker**: Containerized deployment
- **VPS**: Any Linux server with Python

### Example Heroku Deployment
1. Create a `Procfile`:
   ```
   web: python bot.py
   ```
2. Set environment variables in Heroku dashboard
3. Deploy using git or GitHub integration

## Troubleshooting 🔧

### Common Issues

1. **Bot not responding**
   - Check if token is correct
   - Verify bot is running
   - Check network connectivity

2. **Import errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Environment variable errors**
   - Check `.env` file exists and has correct format
   - Verify `TELEGRAM_BOT_TOKEN` is set

### Debug Mode
- Set `DEBUG=True` in `.env` for verbose logging
- Check console output for error messages
- Use `/cancel` command if bot gets stuck

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements 💡

- **Database Integration**: Store user data and quotes
- **Payment Processing**: Handle premium payments
- **Document Upload**: Allow policy document uploads
- **Multi-language Support**: Internationalization
- **Analytics Dashboard**: Track bot usage and metrics
- **AI Integration**: Natural language processing for queries
- **Calendar Integration**: Schedule agent appointments
- **Email Notifications**: Send quotes and updates via email

## License 📄

This project is open source and available under the [MIT License](LICENSE).

## Support 💬

- Create an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide detailed information for faster resolution

## Acknowledgments 🙏

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library
- Telegram Bot API documentation
- Python community for excellent libraries

---

**Happy Coding! 🎉**

Made with ❤️ for the insurance industry