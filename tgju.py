import websockets,json,time,datetime,sys
from persiantools import jdatetime

class tgju:
    def __init__(self):
        self.res="" 
        self.is_jalai=True

    async def req(self):
        # Define initial WebSocket messages to establish connection
        messages=[
            '{"params":{"name":"js"},"id":1}',
            '{"method":1,"params":{"channel":"tgju:stream"},"id":2}'
            ]
        # connect to the websocket endpoint here 
        async with websockets.connect('wss://stream.tgju.org/connection/websocket',user_agent_header="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36") as websocket:
            # Send initialization messages
            for message in messages:
                await websocket.send(message)
                response = await websocket.recv()
           # Receive the final response from the server
            response = await websocket.recv()
            # Clean and parse the response
            self.res=json.loads(response.replace("||||","|"))
            self.res=self.res["result"]["data"]["data"]
        return self
    
    def extract_all(self):
        result={}
        # Iterate through the response data
        for item in self.res:
            # Split the item into its components
            item=item.split("|")
            # Store each item in the result dictionary
            result.update({
                    item[2]:{
                    "name":item[2],
                    "price":item[3],
                    "high":item[4],
                    "low":item[5],
                    "rate":item[8],
                    "dt":item[9],
                    "datetime":self.date_convertor(item[11],self.is_jalai)
                    } 
                })
        return result
    
    def extract_multi(self,entities:list):
        result={}
        for item in self.res:
            item=item.split("|")
             # Check if the item matches the requested entities
            if(len(item)==12 and item[2] in self.__entities):
                result.update({
                       item[2]:{
                        "name":item[2],
                        "price":item[3],
                        "high":item[4],
                        "low":item[5],
                        "rate":item[8],
                        "dt":item[9],
                        "datetime":self.date_convertor(item[11],self.is_jalai)
                       } 
                    })
                return result
            return False
    # Convert date to Jalali or keep it as Gregorian
    def date_convertor(self,date_str,jalai:bool=True):
        
        if(jalai):
            datetime_now=str(jdatetime.JalaliDateTime.
                             fromtimestamp(time.mktime(datetime.datetime.
                                                       strptime(date_str, "%Y-%m-%d %H:%M:%S").timetuple())))
            return datetime_now
        else:
            return date_str
     # Log errors with a datetime
    def logger(self,err):
        date=str(jdatetime.JalaliDateTime.now())
        with open("err.log","a+") as f:
            f.write(f"err=> {err}--{date} \n")
    
if(__name__=="__main__"):
    print("this is a module")