import logging

# Configure the logger in this file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ]
)

# Create a logger instance
logger = logging.getLogger("quant")
