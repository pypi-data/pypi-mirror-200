import mysql.connector
import logging

logger = logging.getLogger()

class Initialize_DB(object):
    def __init__(self, db_local):
        logger.debug("--inside:Initialize_DB() init--")
        self.db_local = db_local
        self.db_conn = None
        self.db_cursor = None

    def __enter__(self):
        # This ensure, whenever an object is created using "with"
        # this magic method is called, where you can create the connection.
        self.db_conn = mysql.connector.connect(**self.db_local)
        self.db_cursor = self.db_conn.cursor(dictionary=True)
        return self

    def __exit__(self, exception_type, exception_val, trace):
        # once the with block is over, the __exit__ method would be called
        # with that, you close the connnection
        try:
           self.db_cursor.close()
           self.db_conn.close()
        except AttributeError: # isn't closable
           print('Not closable.')
           return True # exception handled successfully
    
    def sync_operation(self, mappingid, log_level):  
        logger.setLevel(log_level)     
        logger.debug("inside:Initialize_DB() , sync_operation() func:")    
        self.db_cursor.execute("SELECT * FROM reconcile_sync_data WHERE mapping_id=%s"%(mappingid))
        self.result = self.db_cursor.fetchall()
        return self.result
        
    def statistics_reconcile(self, mappingid, json_data, actions, data):
        logger.debug("inside:Initialize_DB() , statistics_reconcile() func:")        
        update_query = "UPDATE reconcile_sync_data SET statistics=%s WHERE mapping_id = %s AND reconcile_data = %s AND actions = %s"
        values = (       
            data,          
            mappingid,
            json_data,
            actions
        )
        self.db_cursor.execute(update_query, values)
        self.db_conn.commit()  