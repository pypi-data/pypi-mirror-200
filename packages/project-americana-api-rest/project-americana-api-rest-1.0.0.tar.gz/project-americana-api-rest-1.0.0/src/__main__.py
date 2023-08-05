from app import application
import os

if __name__ == "__main__":
    if os.getenv("ENV") == "DEVELOPMENT":
        application.run(host="0.0.0.0")
    application.run()
