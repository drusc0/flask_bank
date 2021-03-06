from scratchfi import create_app
from config import Config


if __name__ == "__main__":
    app = create_app(Config)
    app.run(debug=True, host='0.0.0.0')
