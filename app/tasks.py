class StateProcess(object):
    boolProcess = False
    listProcess = []

    @staticmethod
    def add(item):
        StateProcess.listProcess.append(item)
        print("\n LISTA")
        print(StateProcess.listProcess)

    @staticmethod
    def getList():
        return StateProcess.listProcess
