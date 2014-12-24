class Pin :
    bouton = "P9_12"
    led = "P9_14"
    poto = "P9_36"
    motorAvG = "P9_15"
    motorArD = "P9_13"
    motorArG = "P9_16"
    pedaleAcc = "P9_16"
    pedaleFrein = "P9_36"
    pressionPile = "P9_10"
    tempPile = "P9_10"
    tempMotor = "P9_10"
    switchArduino = "P9_10"

    @classmethod
    def getSensors(cls) :
        return [cls.bouton, cls.poto, cls.pedaleFrein]


