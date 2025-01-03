class Player:
    def __init__(self, health=4, x=0, y=0):
        self.health = health
        self.position = (x, y)

    def walk_left(self,distance):
        self.position = (max(0, self.position[0] - distance), self.position[1])

    def walk_right(self,distance):
        self.position = (min(1000, self.position[0] + distance), self.position[1])

    def jump(self,height):
        self.position = (self.position[0], min(100, self.position[1] + height))

    def __str__(self):
        return f"Health: {self.health}, Position: ({self.position[0]}, {self.position[1]})"

# # Вот как можно протестировать:
player = Player()
player.walk_right(100)
player.walk_left(50)
player.jump(20)
print(player)
