from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    if not os.path.isdir("data"):
        os.mkdir("data")
    app.run(host='0.0.0.0', port=5012)