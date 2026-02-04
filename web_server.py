"""Web server entry point for Tech Investment Crawler"""

import logging
from tech_crawler.web.app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Starting Tech Investment Crawler Web Server")
    app = create_app()
    logger.info("Web server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
