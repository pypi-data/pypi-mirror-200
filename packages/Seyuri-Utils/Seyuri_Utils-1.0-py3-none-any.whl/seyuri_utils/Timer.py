import time, math
from .Logger import Logger
from .utils import randomString

class TimerIDS:
    def __init__(self, message: str, function: any):
        self.message = message
        self.function = function

    def update(self, message: str, function: any):
        self.message = message
        self.function = function

class Timer:
    idList = {}

    def __init__(self):
        self.startTime = self.stopTime = time.perf_counter_ns()
    def __str__(self) -> str:
        return str(self.nsToms(self.stop() - self.startTime))
    
    def start(self) -> int:
        self.startTime = time.perf_counter_ns()
        return self.startTime
    def stop(self) -> int:
        self.stopTime = time.perf_counter_ns()
        return self.stopTime
    def reset(self) -> int:
        self.stop()
        self.start()
        return self.startTime

    @classmethod
    def nsToms(cls, time: str|int, specFunc=math.floor) -> int:
        rawCalc = int(time) / 1_000_000
        return specFunc(rawCalc) if specFunc != None else rawCalc


    @classmethod
    def addID(cls, timerid: TimerIDS, lenghtID: tuple = (2, 2, 2, 2)) -> str:
        newId = randomString(*lenghtID)
        cls.idList[newId] = timerid
        return newId

    @classmethod
    def removeID(cls, id: str) -> bool:
        if id in cls.idList:
            del cls.idList[id]
            return True
        return False

    @classmethod
    def timefunction(cls, message: str='', function: any=Logger.debug, createID: bool=False) -> any:
        preTimerid = TimerIDS(message, function)
        def decorationFunction(passFunction):
            def wrapperFunction(*args, **kwargs):
                timer = Timer()

                if createID == True:
                    kwargs['timerID'] = cls.addID(preTimerid)
                    idxList: TimerIDS = cls.idList[kwargs['timerID']]

                result = passFunction(*args, **kwargs)
                
                if createID == True: idxList.function(idxList.message, { 'end': '' })
                else: function(message, { 'end': '' })
                print(f' {timer}ms')

                cls.removeID(kwargs.get('timerID', ''))

                return result
            return wrapperFunction
        return decorationFunction