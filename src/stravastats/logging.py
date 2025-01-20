from loguru import logger

class Logging:
    
    def reqest_error(self, message: str, request: dict):
        logger.error(message,
                     method=request.method,
                     path=request.path,
                     ip=request.remote_addr,
                     user_agent=request.user_agent.string)
        
    def request_info(self, message: str, request: dict):
        logger.info(message,
                    method=request.method,
                    path=request.path,
                    ip=request.remote_addr,
                    user_agent=request.user_agent.string)
   
    def log_debug(self, message: str):
        logger.debug(message)
        
    def log_info(self, message: str):
        logger.info(message)
    
    def log_warning(self, message: str):
        logger.warning(message)