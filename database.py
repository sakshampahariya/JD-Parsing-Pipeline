"""Database operations module for Supabase integration"""
import logging
from typing import Dict, List, Optional, Any
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseDB:
    """Supabase database operations"""
    
    def __init__(self, url: str, key: str, table_name: str = 'job_extractions'):
        """
        Initialize Supabase client
        
        Args:
            url: Supabase project URL
            key: Supabase API key
            table_name: Name of the table for storing extractions
        """
        try:
            self.client: Client = create_client(url, key)
            self.table_name = table_name
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            raise
    
    def insert_extraction(self, data: Dict[str, Any]) -> Optional[Dict]:
        """
        Insert a job extraction record into the database
        
        Args:
            data: Dictionary containing extracted job data
                  Should include: role, skills, seniority, location, salary, raw_jd, source
        
        Returns:
            Inserted record if successful, None otherwise
        """
        try:
            response = self.client.table(self.table_name).insert(data).execute()
            logger.info(f"Successfully inserted record for role: {data.get('role')}")
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Failed to insert extraction: {str(e)}")
            return None
    
    def insert_batch(self, records: List[Dict[str, Any]]) -> int:
        """
        Insert multiple job extraction records
        
        Args:
            records: List of dictionaries containing extracted job data
        
        Returns:
            Number of successfully inserted records
        """
        if not records:
            return 0
        
        successful_inserts = 0
        for record in records:
            try:
                response = self.client.table(self.table_name).insert(record).execute()
                if response.data:
                    successful_inserts += 1
                    logger.info(f"Batch insert: Successfully inserted record for role: {record.get('role')}")
            except Exception as e:
                logger.error(f"Batch insert failed for record {record.get('role')}: {str(e)}")
                continue
        
        logger.info(f"Batch insert completed: {successful_inserts}/{len(records)} records inserted")
        return successful_inserts
    
    def get_extractions(self, limit: int = 100) -> Optional[List[Dict]]:
        """
        Retrieve recent job extractions
        
        Args:
            limit: Maximum number of records to retrieve
        
        Returns:
            List of extraction records or None if error
        """
        try:
            response = self.client.table(self.table_name).select("*").order(
                "created_at", desc=True
            ).limit(limit).execute()
            logger.info(f"Retrieved {len(response.data)} extraction records")
            return response.data
        except Exception as e:
            logger.error(f"Failed to retrieve extractions: {str(e)}")
            return None
    
    def get_extraction_by_id(self, extraction_id: int) -> Optional[Dict]:
        """
        Retrieve a specific job extraction by ID
        
        Args:
            extraction_id: ID of the extraction record
        
        Returns:
            Extraction record or None if not found
        """
        try:
            response = self.client.table(self.table_name).select("*").eq(
                "id", extraction_id
            ).single().execute()
            logger.info(f"Retrieved extraction with ID: {extraction_id}")
            return response.data
        except Exception as e:
            logger.error(f"Failed to retrieve extraction with ID {extraction_id}: {str(e)}")
            return None
    
    def table_exists(self) -> bool:
        """
        Check if the job_extractions table exists
        
        Returns:
            True if table exists, False otherwise
        """
        try:
            self.client.table(self.table_name).select("*").limit(1).execute()
            logger.info(f"Table '{self.table_name}' exists and is accessible")
            return True
        except Exception as e:
            logger.error(f"Table '{self.table_name}' does not exist or is inaccessible: {str(e)}")
            return False

class DatabaseManager:
    """Manager for database operations"""
    
    _instance = None
    
    def __new__(cls, url: str = None, key: str = None, table_name: str = 'job_extractions'):
        """Singleton pattern for database manager"""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.db = SupabaseDB(url, key, table_name)
        return cls._instance
    
    def insert(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Insert a job extraction"""
        return self.db.insert_extraction(data)
    
    def insert_many(self, records: List[Dict[str, Any]]) -> int:
        """Insert multiple job extractions"""
        return self.db.insert_batch(records)
    
    def get_all(self, limit: int = 100) -> Optional[List[Dict]]:
        """Get all extractions"""
        return self.db.get_extractions(limit)
    
    def get_one(self, extraction_id: int) -> Optional[Dict]:
        """Get a specific extraction"""
        return self.db.get_extraction_by_id(extraction_id)
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.db.table_exists()
