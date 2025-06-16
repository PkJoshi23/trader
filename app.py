from flask import Flask
import threading
from bot import main  # Import your trading bot's main loop

app = Flask(__name__)

@app.route('/')
def home():
    return "Trading bot is running!"

def run_bot():
    main()  # This should be your trading bot's main loop

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=10000) 