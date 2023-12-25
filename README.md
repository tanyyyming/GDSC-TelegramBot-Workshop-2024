# GDSC Telegram Bot Workshop 2024

## Quick Start
1. Clone this repository to your local machine by running the following command in your terminal:
    ```bash
    git clone https://github.com/tanyyyming/GDSC-TelegramBot-Workshop-2024.git
    ```

2. Create a virtual environment called `venv` by running the following command at the root of the project directory:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment by running the following command:
    ```bash
    source venv/bin/activate
    ```

4. Install the required packages by running the following command:
    ```bash
    pip3 install -r requirements.txt
    ```

5. Create a `.env` file at the root of the project directory to store your telegram bot token and your image captioning API key securely:
    ```
    BOT_TOKEN = "your bot token as a string"
    API_KEY = "your api key as a string"
    ```

6. Create an empty `data/` directory at the root of the project directory to store the images that you want to caption.

7. Run the following command to start the bot:
    ```bash
    python3 bot.py
    ```