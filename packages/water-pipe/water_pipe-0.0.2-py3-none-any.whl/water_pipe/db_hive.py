from base import Connect
from pyhive import hive

class HiveConnect(Connect):
    
    def __init__(self, config) -> None:
        """
        config = {
            
        }
        """
        
        self.connect = hive.connect(config)