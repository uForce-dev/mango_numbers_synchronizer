import logging
import sys
from datetime import datetime
from config import settings
from sync_service import SyncService

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("mango_sync.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 50)
    logger.info("Starting Mango Office numbers sync")
    logger.info(f"Started at: {datetime.now()}")
    logger.info("=" * 50)

    sync_service = None

    try:
        sync_service = SyncService()

        result = sync_service.sync_phone_numbers()

        logger.info("Sync results:")
        logger.info(f"  Processed: {result.total_processed}")
        logger.info(f"  Created: {result.created}")
        logger.info(f"  Updated: {result.updated}")
        logger.info(f"  Errors: {result.errors}")

        if result.error_details:
            logger.warning("Error details:")
            for error in result.error_details:
                logger.warning(f"  - {error}")

        if result.errors > 0:
            logger.warning(f"Sync finished with errors ({result.errors})")
            sys.exit(1)
        else:
            logger.info("Sync completed successfully")
            sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Interrupted, shutting down...")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        if sync_service:
            sync_service.close()
        logger.info("Done")


if __name__ == "__main__":
    main()
