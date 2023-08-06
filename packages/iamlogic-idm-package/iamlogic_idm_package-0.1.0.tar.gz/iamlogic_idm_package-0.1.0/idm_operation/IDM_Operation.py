from .idm_sync import Initialize_DB
from IDMConnector import ConnectorClass
import time, json, logging
from datetime import timedelta
from cryptography.fernet import Fernet

logger = logging.getLogger()

class IDMOperationClass(object):
    
    def __init__(self, configobject):
        self.idm_operation_obj = ConnectorClass(configobject)

    def retry_attempt(self, config_param=None, max_attempt=None, delay=5):
        i = 0
        for attempt in range(1, max_attempt+1):
            i = i+1
            try:
                result = self.idm_operation_obj.testConfig(config_param)
                logger.info(f"retry_attempt() func: try attempt-{i}")
                if(result["status"]):
                    logger.info(f"retry_attempt() func: succeed-{i}")
                    logger.debug(result)
                    self.__init__(config_param)
                    return result["status"]
            except Exception as e:
                if attempt < max_attempt:
                    time.sleep(delay)
                    logger.info(f"retry_attempt() func: exception attempt-{i}")
                    logger.error(str(e))
        return None

    def sync(self, mappingid, config_data, log_level, db_config, fernet_key) -> dict:                
        logger.setLevel(log_level)
        logger.debug("inside:ConnectorClass() , sync() func:")
        # Get a Fernet instance with the key
        fernet = Fernet(fernet_key)        
        db_config["passwd"] = fernet.decrypt(db_config["passwd"]).decode()      
        start_time = time.time()
        # DB Sync operation call
        msg = "success"
        current_obj_id = 0        
        # Processed Operation records
        processed_operation = set()
        with Initialize_DB(db_config) as obj:
            response = obj.sync_operation(mappingid, log_level)
            while current_obj_id < len(response):
                obj = response[current_obj_id]
                logger.debug(f"response obj:{obj['id']}")
                logger.debug(f"Processed Operation:{processed_operation}")
                try:
                    logger.debug(f"obj{obj['id']}_currentObj{current_obj_id}")
                    if(obj['actions'] == "create"):
                        json_create_data = obj['reconcile_data']
                        logger.debug("inside:ConnectorClass() , sync() func if create try:")
                        createOp_response = self.idm_operation_obj.create(json.loads(obj['reconcile_data']))
                        with Initialize_DB(db_config) as dbObj:
                            dbObj.statistics_reconcile(mappingid, json_create_data, obj['actions'], msg)
                    elif(obj['actions'] == "update"):
                        json_update_data = obj['reconcile_data']
                        logger.debug("inside:ConnectorClass() , sync() func elif update try:")
                        updateOp_response = self.idm_operation_obj.update(json.loads(obj['reconcile_data']))
                        with Initialize_DB(db_config) as dbObj:
                            dbObj.statistics_reconcile(mappingid, json_update_data, obj['actions'], msg)
                    elif(obj['actions'] == "delete"):
                        json_delete_data = obj['reconcile_data']
                        logger.debug("inside:ConnectorClass() , sync() func elif delete try:")
                        deleteOp_response = self.idm_operation_obj.delete(json.loads(obj['reconcile_data']))
                        with Initialize_DB(db_config) as dbObj:
                            dbObj.statistics_reconcile(mappingid, json_delete_data, obj['actions'], msg)
                    processed_operation.add(obj['id'])
                    current_obj_id += 1
                except Exception as e:
                    logger.debug("inside:ConnectorClass() , sync() except Exception:")
                    logger.warning(str(e))
                    with Initialize_DB(db_config) as dbObj:
                        dbObj.statistics_reconcile(mappingid, obj['reconcile_data'], obj['actions'], str(e))
                    try:
                        # Check connection if any type of exception happening
                        conn_test_res = self.idm_operation_obj.testConfig(config_data)
                        if conn_test_res["status"]:
                            logger.debug(f"connection is available,try response_obj_operation:{obj['id']}")
                            self.idm_operation_obj.__init__(config_data)
                            current_obj_id += 1
                    except Exception as e:
                        # Re-attempt check if testConfig() return false
                        logger.info(f"Re-attempt before check, response_obj_operation:{obj['id']}")
                        conn_attempt_resp = self.retry_attempt(config_param=config_data, max_attempt=int(config_data['retry']))
                        if(conn_attempt_resp and conn_attempt_resp is not None):
                            logger.info(f"Re-attempt if conn true, response_obj_operation:{obj['id']}")
                            current_obj_id -= 1
                        else:
                            logger.info(f"Many re-attempt connectivity failed, response_obj_operation:{obj['id']}")
                            return {"error": "Please check the target application server connectivity. Many attempt could not connected!."}

        end_time = time.time()
        duration = end_time - start_time
        duration_str = str(timedelta(seconds=duration))
        return {"total_duration":duration_str, "status": "sync done!"}