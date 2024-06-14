class Boss(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.image = game.assets['enemy/idle']
        self.vel = [0, 0]
        self.homing = False
        self.stomp = False
        self.death = 0