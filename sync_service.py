import logging
from typing import List
from database import DatabaseService
from mango_client import MangoOfficeClient
from models import SyncResult, MangoLine

logger = logging.getLogger(__name__)


class SyncService:
    
    def __init__(self):
        self.db_service = DatabaseService()
        self.mango_client = MangoOfficeClient()
    
    def sync_phone_numbers(self) -> SyncResult:
        logger.info("Starting phone numbers sync")
        
        result = SyncResult(
            total_processed=0,
            created=0,
            updated=0,
            errors=0
        )
        
        try:
            api_response = self.mango_client.get_phone_numbers()
            if not api_response:
                logger.error("Failed to fetch data from API")
                result.error_details.append("API fetch error")
                return result
            
            if api_response.result != 1000:
                logger.error(f"API error code: {api_response.result}")
                result.error_details.append(f"API error: {api_response.result}")
                return result
            
            session = self.db_service.get_session()
            
            try:
                for mango_line in api_response.lines:
                    result.total_processed += 1
                    
                    try:
                        existing = self.db_service.get_phone_number_by_number(session, mango_line.number)
                        
                        if existing:
                            if self.db_service.update_phone_number(session, existing, mango_line):
                                result.updated += 1
                            else:
                                result.errors += 1
                                result.error_details.append(f"Update error {mango_line.number}")
                        else:
                            if self.db_service.create_phone_number(session, mango_line):
                                result.created += 1
                            else:
                                result.errors += 1
                                result.error_details.append(f"Create error {mango_line.number}")
                                
                    except Exception as e:
                        logger.error(f"Error processing number {mango_line.number}: {e}")
                        result.errors += 1
                        result.error_details.append(f"Process error {mango_line.number}: {str(e)}")
                
                logger.info(
                    f"Sync finished. "
                    f"Processed: {result.total_processed}, "
                    f"Created: {result.created}, "
                    f"Updated: {result.updated}, "
                    f"Errors: {result.errors}"
                )
                
            finally:
                session.close()
                
        except Exception as e:
            logger.error(f"Critical error during sync: {e}")
            result.error_details.append(f"Critical error: {str(e)}")
        
        return result
    
    def close(self):
        self.db_service.close()
