from app import create_app
import os

app = create_app(os.getenv("FLASK_ENV", "development"))

if __name__ == '__main__':
    # env = os.getenv('FLASK_ENV', 'development')
    # app = create_app(env)
    # app.run(port=5001)
    app.run(host='0.0.0.0', port=5001)

