import socket, json, random, math
import pygame as pg

pg.init()

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(("localhost", 10000))
main_socket.setblocking(0)
main_socket.listen(5)

print("Server stated")

class Player():
    def __init__(self, addr, conn, colour, x, y, radius, errors, tick):
        self.addr = addr
        self.number = objects
        self.conn = conn
        self.colour = colour
        self.x = x
        self.y = y
        self.radius = radius
        self.rect = pg.rect.Rect(x, y, radius * 2, radius * 2)
        self.erors = errors
        self.speed = 30 / (self.radius ** 0.5)
        self.tick = tick
        self.w_vision = 0
        self.h_vision = 0
        self.scale = 1
        self.vector = [0, 0]
        self.win_width = 0
        self.win_height = 0
        self.name = None
    def draw(self):
        pg.draw.circle(screen, self.colour, (win_width * (self.rect.centerx/room_width), win_width * (self.rect.centery/room_height)), win_width * (self.radius/room_width))
    def move(self):
        if self.conn != None:
            try:
                data = json.loads(self.conn.recv(1024).decode())
                self.vector = [data["x"], data["y"]]
                if self.name == None:
                    self.name = data["name"]
            except:
                pass
        
        if self.conn == None and self.name == None:
            self.name = random.choice(nicks)

        elif tick == 2 and self.conn == None:
            self.vector = [random.randint(-100, 100), random.randint(-100, 100)]

        if self.conn != None and self.w_vision == 0:
            self.w_vision, self.h_vision = data["w_vision"], data["h_vision"]
            self.win_width, self.win_height = self.w_vision, self.h_vision

        if self.conn != None and self.radius == 0:
            if self.tick < 120:
                self.tick += 1
            if self.tick >= 120:
                self.radius = 25
                spawn = random.choice(food)
                self.rect.centerx, self.rect.centery = random.randint(0, room_width), random.randint(0, room_height)            
                spawn.rect.centerx, spawn.rect.centery = random.randint(0, room_width), random.randint(0, room_height)
                self.tick = 0

        dist = (self.vector[0] ** 2 + self.vector[1] ** 2) ** 0.5

        if dist != 0 and self.radius > 0:
            try:
                x_speed = self.vector[0] / dist * self.speed
                y_speed = self.vector[1] / dist * self.speed
            except:
                x_speed, y_speed = 0, 0
        else:
            x_speed, y_speed = 0, 0

        if self.rect.centerx - self.radius <= 0:
            if x_speed >= 0:
                self.rect.centerx += x_speed
        else:
            if self.rect.centerx + self.radius >= room_width:
                if x_speed <= 0:
                    self.rect.centerx += x_speed
            else:
                self.rect.centerx += x_speed

        if self.rect.centery - self.radius <= 0:
            if y_speed >= 0:
                self.rect.centery += y_speed
        else:
            if self.rect.centery + self.radius >= room_height:
                if y_speed <= 0:
                    self.rect.centery += y_speed
            else:
                self.rect.centery += y_speed

        if self.radius >= 100:
            self.radius -= self.radius / 20000
        
        if self.conn != None:
            if self.radius >= self.w_vision / 4 or self.radius >= self.h_vision / 4:
                if self.w_vision <= room_width or self.h_vision <= room_height:
                    self.scale *= 2
                    self.w_vision = self.win_width * self.scale
                    self.h_vision = self.win_height * self.scale
            if self.radius < self.w_vision / 8 and self.radius < self.h_vision / 8:
                if self.scale > 1:
                    self.scale = self.scale // 2
                    self.w_vision = self.win_width * self.scale
                    self.h_vision = self.win_height * self.scale
    def send_data(self):
        if self.conn != None:
            data = {"radius": int(self.radius // self.scale),
                    "colour": self.colour,
                    "visible": self.see()}
            try:
                self.conn.send(json.dumps(data).encode())
                self.erors = 0
            except:
                self.speed = 0
                self.erors += 1
                if self.erors >= 100:
                    if self.conn != None:
                        self.conn.close()
                    players.remove(self)
                    print(player.addr, "disconnected")
    def see(self):
        visible = {}
        for f in food:
            if ((f.rect.centerx - self.rect.centerx) ** 2 + (f.rect.centery - self.rect.centery) ** 2) ** 0.5 <= self.radius:
                f.rect.centerx, f.rect.centery = random.randint(0, room_width), random.randint(0, room_height)
                self.radius = (self.radius ** 2 + f.radius ** 2) ** 0.5
                self.speed = 30 / (self.radius ** 0.5)
                if self.speed < 4:
                    self.speed = 4
            if self.conn != None and abs(f.rect.centerx - self.rect.centerx) <= self.w_vision / 2 + f.radius and abs(f.rect.centery - self.rect.centery) <= self.h_vision / 2 + f.radius:
                visible[f.number] = {"dist_x": (f.rect.centerx - self.rect.centerx) // self.scale,
                                     "dist_y": (f.rect.centery - self.rect.centery) // self.scale,
                                     "radius": f.radius / self.scale,
                                     "colour": f.colour}
        for player in players:
            if player != self:
                if ((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.rect.centery) ** 2) ** 0.5 <= self.radius and self.radius > player.radius * 1.1:
                        self.radius = (self.radius ** 2 + player.radius ** 2) ** 0.5
                        self.speed = 30 / (self.radius ** 0.5)
                        if self.speed < 4:
                            self.speed = 4
                        if player.conn == None:
                            player.radius = random.randint(25, 50)
                            player.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                            player.rect.centerx, player.rect.centery = random.randint(0, room_width), random.randint(0, room_height)
                        else:
                            player.radius = 0
                
                if self.conn != None and abs(player.rect.centerx - self.rect.centerx) <= self.w_vision / 2 + player.radius and abs(player.rect.centery - self.rect.centery) <= self.h_vision / 2 + player.radius:
                    visible[player.number] = {"dist_x": (player.rect.centerx - self.rect.centerx) // self.scale,
                                              "dist_y": (player.rect.centery - self.rect.centery) // self.scale,
                                              "radius": player.radius // self.scale,
                                              "colour": player.colour,
                                              "name": player.name}
        if self.conn != None:
            return visible

class Food():
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.rect = pg.rect.Rect(x, y, radius * 2, radius * 2)
        self.number = objects

win_width, win_height = 500, 500
room_width, room_height = 4000, 4000

pg.display.set_caption("bacteria_server")
screen = pg.display.set_mode((win_width, win_height))

players = []
food = []
fps = 60
tick = 0
objects = 0
mobs_quantity = 25
food_quantity = room_width * room_height // 80000
clients = 0
nicks = ["Физмат", "Химбио", "Гений"]
for i in range(mobs_quantity):
    objects += 1
    players.append(Player(None, None, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(0, room_width), random.randint(0, room_height), random.randint(25, 50), None, None))
for i in range(food_quantity):
    objects += 1
    food.append(Food(random.randint(15, room_width - 15), random.randint(15, room_height - 15), 15, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
font = pg.font.Font(None, 20)
clock = pg.time.Clock()
server_working = True

while server_working:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            server_working = False

    if tick < 120:
        tick += 1
    else:
        tick = 0

    if tick == 1:
        try:
            new_socket, addr = main_socket.accept()
            print(addr, "successfully connected")
            objects += 1
            clients += 1
            spawn = random.choice(food)
            players.append(Player(addr, new_socket, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), spawn.rect.centerx, spawn.rect.centery, 25, 0, 0))
            spawn.rect.centerx, spawn.rect.centery = random.randint(0, room_width), random.randint(0, room_height)
            new_socket.setblocking(0)
        except:
            pass 

    screen.fill("black")
        
    for player in players:
        player.move()
        player.draw()
        player.see()
        player.send_data()   
        if player.radius >= 3000:
            for player in players:
                if player.conn == None:
                    player.radius = random.randint(25, 50)
                    player.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    player.rect.centerx, player.rect.centery = random.randint(0, room_width), random.randint(0, room_height)
                else:
                    player.radius = 0
    
    clock.tick(fps)
    pg.display.update()
pg.quit()