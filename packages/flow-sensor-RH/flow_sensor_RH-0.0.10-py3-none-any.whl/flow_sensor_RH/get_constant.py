def getConstant():
    """
    Get constants required by the Flow Sensor Model.

    Returns:
        Ma, Mv, P0, R, Rw
        Ma - Molar mass of dry air
        Mv - Molar mass of water vapor
        P0 - Atmospheric pressure
        R  - Molar gas constant
    """
    Ma  = 28.963e-3
    Mv  = 18.02e-3
    P0  = 101325
    R   = 8.314
    #Rw  = 461.5
    return Ma, Mv, P0, R#, Rw