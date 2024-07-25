class Config:
    def __init__(self):
        # 物理常數
        self.GRAVITY = 9.81  # m/s^2
        self.AIR_DENSITY = 1.225  # kg/m^3 (海平面)

        # 火箭參數
        self.INITIAL_FUEL = 5000  # kg
        self.BURN_RATE = 10.0  # kg/s
        self.THRUST = 1000.0  # N
        self.LANDING_THRUST = 500.0  # N
        self.EXHAUST_VELOCITY = 3000  # m/s
        self.CROSS_SECTIONAL_AREA = 0.1  # m^2
        self.INITIAL_MASS = 500.0  # kg
        self.MIN_MASS = 100.0  # kg

        # 環境參數
        self.AIR_RESISTANCE_COEFFICIENT = 10000
        self.MAX_WIND_SPEED = 500  # m/s

        # 模擬參數
        self.INITIAL_TEMPERATURE = 15.0  # °C
        self.TEMPERATURE_VARIATION_RATE = 0.01  # °C/m

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if key.isupper()}

    @classmethod
    def from_dict(cls, config_dict):
        config = cls()
        for key, value in config_dict.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return config