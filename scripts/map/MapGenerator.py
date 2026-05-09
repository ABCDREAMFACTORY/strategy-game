import hashlib
from math import cos, sin, radians, exp
import json
from .Map import Map, Tile

class MapGenerator:

    def __init__(self, seed: int, map_size: int,biome_size: int):

        self.coef_dif_biome = {"altitude":0.5,"humidity":0.5}
        self.biome_size =biome_size
        self.map_size = map_size
        self.seed = seed
        self.map_final = [[ {"altitude": 0, "humidity":0} for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.map = [[ {"altitude": 0, "humidity":0} for _ in range(self.map_size)] for _ in range(self.map_size)]

        with open("data/config/terrains.json", "r") as f:
            data = json.load(f)
        self.humidity_tile = {}
        self.altitude_tile = {}
        for elem in data.keys():
            self.altitude_tile[elem] = data[elem]["altitude"]
            self.humidity_tile[elem] = data[elem]["humidity"]



    def gen_matrice(self):

        for x in range(0, self.map_size, self.biome_size):
            for y in range(0, self.map_size, self.biome_size):
                vect = self.create_vec_from_seed_and_pos(x,y,self.seed)
                newpos = self.calc_new_pos(vect,x,y)
                if newpos != None:
                    self.map[newpos[0]][newpos[1]]["altitude"] = 1
                    self.lissage_map(newpos[0],newpos[1],"altitude")

                vect = self.create_vec_from_seed_and_pos(x,y,self.seed+1)
                newpos = self.calc_new_pos(vect,x,y)
                if newpos != None:
                    self.map[newpos[0]][newpos[1]]["humidity"] = 1
<<<<<<< HEAD
                    self.lissage_map(newpos[0],newpos[1],"humidity")
=======
                    self.lissage_map(x,y,"humidity")

>>>>>>> 0ba4452 (remove unused print)


        print(self.calc_moyenne("altitude"))
        print(self.calc_moyenne("humidity"))



    def create_vec_from_seed_and_pos(self, posx, posy,seed):

        valeur = f"{posx},{posy},{seed}"

        taille_vec = self.transforme_nombre(valeur)
        angle_vec = self.transform_angle(valeur)
        return (taille_vec, angle_vec)


    def transforme_nombre(self, valeur):

        h = hashlib.sha256(str(valeur).encode()).hexdigest()
        seed_hash = int(h, 16)

        return seed_hash % (self.biome_size * 1000) / 1000


    def transform_angle(self, valeur):

        h = hashlib.sha256(str(valeur).encode()).hexdigest()
        nombre = int(h, 16)
        return nombre % (360 * 1000) / 1000


    def calc_new_pos(self, vect: tuple, posx:int, posy:int):

        angle = radians(vect[1])
        nvec = (#Trigo calcule le vecteur directeur
            vect[0] * sin(angle),
            vect[0] * cos(angle)
        )

        npos = (#Calcule le nouveau point avec Vect+ancien point
            round(nvec[0] + posx),
            round(nvec[1] + posy)
        )

        if (#Verifie si le vecteur se trouve dans les coordonÃ©es de la map
            npos[0] < 0
            or npos[1] < 0
            or npos[0] >= self.map_size
            or npos[1] >= self.map_size
        ):
            return None

        return npos
    
    def distance(self,pos1,pos2):
        return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5


    def lissage_map(self,posx,posy,canal):

        wait_list = [(posx,posy)]
        already_check = set()
        cursor = 0
        while len(wait_list) != cursor:
            current_elem = wait_list[cursor]
            coef_dif_biome = self.coef_dif_biome[canal]
            dist = self.distance((posx,posy),current_elem)
            if  dist < 10:

                val_to_add = exp(dist*-1*coef_dif_biome)
                if self.map_final[current_elem[0]][current_elem[1]][canal] + val_to_add > 1:
                    self.map_final[current_elem[0]][current_elem[1]][canal] = 1
                else:
                    self.map_final[current_elem[0]][current_elem[1]][canal]+= val_to_add

                for intx,inty in ((1,0),(-1,0),(0,1),(0,-1)):
                    new_pos = (current_elem[0]+intx,current_elem[1]+inty)
                    if new_pos not in already_check and 0<new_pos[0]<self.map_size-1 and 0<new_pos[1]<self.map_size-1:
                        wait_list.append(new_pos)
                        already_check.add(new_pos)
                                
            cursor+=1

    def stats_to_tile(self,stats: dict) -> str:
        altitude, humidity = stats["altitude"], stats["humidity"]
        best_score = float("inf")
        best_tile = "grass"
        for tile in self.altitude_tile.keys():
            score = abs(self.altitude_tile[tile]-altitude)+abs(self.humidity_tile[tile]-humidity)
            if score < best_score:
                best_score = score
                best_tile = tile
        return best_tile

    def convert_map_to_tiles(self, tiles):
        for x in range(self.map_size):
            for y in range(self.map_size):
                tile_stats = self.map_final[x][y]
                tile_type = self.stats_to_tile(tile_stats)
                tiles[y][x].terrain = tile_type


    def calc_moyenne(self,canal):
        moyenne  = 0
        for i in range(self.map_size):
            for j in range(self.map_size):
                moyenne += self.map_final[i][j][canal]
        return moyenne/(self.map_size**2)

    def __str__(self):
        lines = []
        for y in range(self.map_size):
            line = []
            for x in range(self.map_size):
                a = self.map_final[x][y]["altitude"]
                h = self.map_final[x][y]["humidity"]
                line.append(f"A:{a:4.2f} H:{h:4.2f}")
            lines.append(" | ".join(line))
        return "\n".join(lines)


