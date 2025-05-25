import socket, screeninfo, json, math
import pygame as  pg

pg.init()

def new_socket():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)\

win_width = screeninfo.get_monitors()[0].width / 2
win_height = screeninfo.get_monitors()[0].height / 2

connection = False
sock = None
fps = 60
tick = 0
old_vector = ""
old_radius = 0
vector = {"x": 0}
data = {}
errors = 0
nick = input("Nickname: ")
while len(nick) > 8:
    print("max 8 symbols")
    nick = input("Nickname: ")
screen = pg.display.set_mode((win_width, win_height))
nicknames = {}
pg.display.set_caption("bacteria_client")
new_socket()
running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if tick < 60:
        tick += 1
    else:
        tick = 0

    screen.fill("black")

    if connection == False and tick == 1:
        try:
            sock.connect(("localhost", 10000))
            vector["w_vision"], vector["h_vision"], vector["name"] = win_width, win_height, nick
            vector["x"], vector["y"], vector["dist"] = 0, 0, 0
            vector = json.dumps(vector)
            connection = True
            tick = 0
            print("successfully connected")
        except:
            pass
            
    if connection == True:
        vector = json.loads(vector)
        if pg.mouse.get_focused():
            if len(data) != 0 and data["radius"] >= ((pg.mouse.get_pos()[0] - win_width // 2) ** 2 + (pg.mouse.get_pos()[1] - win_height // 2) ** 2) ** 0.5:
                vector["x"], vector["y"], vector["dist"] = 0, 0, 0
            else:
                vector["x"] = pg.mouse.get_pos()[0] - win_width / 2
                vector["y"] = pg.mouse.get_pos()[1] - win_height / 2

        vector = json.dumps(vector)

        if vector != old_vector and len(vector) != 0:
            old_vector = vector
            try:
                sock.send(vector.encode())
            except:
                pass

        try:
            data = json.loads(sock.recv(32768).decode())
            errors = 0
        except:
            errors += 1

        if errors >= 100:
            errors = 0
            connection = False
            sock.close()
            new_socket()
            vector = json.loads(vector)
            print("connection is lost")
            
        
        screen.fill("gray25")

        try:
            if data["radius"] > 0:
                pg.draw.circle(screen, "black", (win_width // 2, win_height // 2), data["radius"] + 2)
                pg.draw.circle(screen, data["colour"], (win_width // 2, win_height // 2), data["radius"])
                if data["radius"] != old_radius:
                    name = pg.font.Font(None, int(data["radius"] * 0.6)).render(nick, False, "black")
                    old_radius = data["radius"]
                screen.blit(name, (win_width // 2 - name.get_width() // 2, win_height // 2 - name.get_height() // 2))
        except:
            pass

        for i in data["visible"]:
            try:
                pg.draw.circle(screen, "black", (win_width // 2 + data["visible"][i]["dist_x"], win_height // 2 + data["visible"][i]["dist_y"]), data["visible"][i]["radius"] + 2)
                pg.draw.circle(screen, data["visible"][i]["colour"], (win_width // 2 + data["visible"][i]["dist_x"], win_height // 2 + data["visible"][i]["dist_y"]), data["visible"][i]["radius"])
                if data["visible"][i].get("name") != None and nicknames.get(i) == None:
                    if nicknames.get(i) == None:
                        nicknames[i] = {"old_r": 0}
                    if nicknames[i]["old_r"] != data["visible"][i]["radius"]:
                        n = pg.font.Font(None, int(round(data["visible"][i]["radius"] * 0.6))).render(data["visible"][i]["name"], False, "black")
                        nicknames[i]["nick"] = n
                        nicknames[i]["old_r"] = data["visible"][i]["radius"]
                if nicknames[i]["nick"] != None:
                    screen.blit(nicknames[i]["nick"], (win_width // 2 + data["visible"][i]["dist_x"] - nicknames[i]["nick"].get_width() // 2, win_height // 2 + data["visible"][i]["dist_y"] - nicknames[i]["nick"].get_height() // 2))
            except:
                pass
    
    clock.tick(fps)
    pg.display.update()
pg.quit()