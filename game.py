import random
import sys
import time
from enum import Enum
from typing import List, Dict, Tuple, Optional, Set

# ENUMS -------------------------------------------
class Direction(Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    STAY = "stay"

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3

class TerrainType(Enum):
    PLAINS = "plains"
    FOREST = "forest"
    SWAMP = "swamp"
    MOUNTAIN = "mountain"
    DESERT = "desert"

class ItemType(Enum):
    FOOD = "food"
    WATER = "water"
    GOLD = "gold"
    TRADER = "trader"
    SPECIAL = "special"

# TERRAIN CLASS -----------------------------------
class Terrain:
    def __init__(self, terrain_type: TerrainType):
        self.type = terrain_type
        # costs: (movement, water, food)
        if terrain_type == TerrainType.PLAINS:
            self.movement_cost, self.water_cost, self.food_cost = 1, 1, 1
        elif terrain_type == TerrainType.FOREST:
            self.movement_cost, self.water_cost, self.food_cost = 2, 1, 2
        elif terrain_type == TerrainType.SWAMP:
            self.movement_cost, self.water_cost, self.food_cost = 2, 1, 3
        elif terrain_type == TerrainType.MOUNTAIN:
            self.movement_cost, self.water_cost, self.food_cost = 3, 2, 2
        elif terrain_type == TerrainType.DESERT:
            self.movement_cost, self.water_cost, self.food_cost = 2, 3, 1
        else:
            raise ValueError(f"Unknown terrain type: {terrain_type}")
    def get_movement_cost(self) -> int: return self.movement_cost
    def get_water_cost(self)    -> int: return self.water_cost
    def get_food_cost(self)     -> int: return self.food_cost
    def __str__(self) -> str: return self.type.value

# ITEM CLASSES -------------------------------------
class TraderType(Enum):
    PATIENT = "patient"
    PICKY = "picky"
    SCAMMER = "scammer"
class Item:
    def __init__(self, name: str, description: str, repeating: bool=False):
        self.name = name
        self.description = description
        self.repeating = repeating
    def apply(self, player) -> None: pass
    def is_repeating(self) -> bool: return self.repeating
    def __str__(self) -> str: return self.name

class FoodBonus(Item):
    def __init__(self, amount:int, repeating:bool=False):
        super().__init__("Food Bonus", f"Provides {amount} food", repeating)
        self.amount = amount
    def apply(self, player):
        player.add_resources(0, 0, self.amount, 0)
        print(f"Collected {self.amount} food!")

class WaterBonus(Item):
    def __init__(self, amount:int, repeating:bool=False):
        super().__init__("Water Bonus", f"Provides {amount} water", repeating)
        self.amount = amount
    def apply(self, player):
        player.add_resources(0, self.amount, 0, 0)
        print(f"Collected {self.amount} water!")

class GoldBonus(Item):
    def __init__(self, amount:int, repeating:bool=False):
        super().__init__("Gold Bonus", f"Provides {amount} gold", repeating)
        self.amount = amount
    def apply(self, player):
        player.add_resources(0, 0, 0, self.amount)
        print(f"Collected {self.amount} gold!")

class Trader(Item):
    def __init__(self, trader_type: TraderType):
        self.type = trader_type
        if trader_type == TraderType.PATIENT:
            self.patience, self.greed_factor = 5, 1
            name = "Patient Trader"
            description = "A patient and fair trader."
        elif trader_type == TraderType.PICKY:
            self.patience, self.greed_factor = 3, 2
            name = "Picky Trader"
            description = "A picky trader."
        elif trader_type == TraderType.SCAMMER:
            self.patience, self.greed_factor = 2, 3
            name = "Trader"
            description = "Offers excellent deals!"
        else:
            raise ValueError(f"Unknown trader type: {trader_type}")
        super().__init__(name, description, True)
        self.current_patience = self.patience
        self.offers_made = 0

    def apply(self, player) -> None:
        print(f"Found a {self.name}!")

    def offer_trade(self, player) -> bool:
        print(f"\n--- Trading with {self.name} ---")
        print("Trade format: X food Y water Z gold FOR A food B water C gold")
        print("Type 'exit' to cancel.")
        self.current_patience, self.offers_made = self.patience, 0
        while True:
            print(f"Resources: Food={player.current_food}, Water={player.current_water}, Gold={player.gold}")
            offer = input("Your offer: ")
            if offer.lower() == 'exit': return False
            try:
                of, ow, og, rf, rw, rg = self._parse_offer(offer)
                if player.current_food < of or player.current_water < ow or player.gold < og:
                    print("Insufficient resources.")
                    continue
                resp = self._evaluate_offer(of, ow, og, rf, rw, rg, player.trader_discount)
                if resp == 'accept':
                    player.add_resources(0, -ow, -of, -og)
                    player.add_resources(0, rw, rf, rg)
                    print(f"Trade accepted. Gave {of}F,{ow}W,{og}G for {rf}F,{rw}W,{rg}G.")
                    return True
                if resp == 'reject': print("Trade rejected."); return False
                if resp == 'counter':
                    cf, cw, cg, rf2, rw2, rg2 = self._make_counter_offer(of, ow, og, rf, rw, rg)
                    print(f"Counter: {cf}F,{cw}W,{cg}G FOR {rf2}F,{rw2}W,{rg2}G")
                    if input("Accept? (yes/no)").lower() == 'yes':
                        player.add_resources(0, -cw, -cf, -cg)
                        player.add_resources(0, rw2, rf2, rg2)
                        print("Counter accepted."); return True
            except ValueError as e:
                print(f"Error: {e}")
                print("Use 'X food Y water Z gold FOR A food B water C gold'.")

    def _parse_offer(self, s:str) -> Tuple[int,int,int,int,int,int]:
        p1,p2 = s.upper().split("FOR")
        t1,t2 = p1.strip().split(), p2.strip().split()
        if len(t1)!=6 or len(t2)!=6: raise ValueError("Bad format")
        return int(t1[0]),int(t1[2]),int(t1[4]), int(t2[0]),int(t2[2]),int(t2[4])

    def _evaluate_offer(self, of, ow, og, rf, rw, rg, disc=0) -> str:
        self.offers_made += 1
        val_offer = of + ow + og*3
        val_req   = rf + rw + rg*3
        if disc: val_req *= (100-disc)/100
        if self.offers_made > self.current_patience: return 'reject'
        ratio = val_offer / max(val_req,1)
        thresh = 1.0 + 0.2*self.offers_made*self.greed_factor if self.type==TraderType.SCAMMER else 0.8*self.greed_factor
        if ratio >= thresh: return 'accept'
        if ratio >= thresh*0.7: return 'counter'
        self.current_patience -=1
        return 'reject' if self.current_patience<=0 else 'counter'

    def _make_counter_offer(self, of, ow, og, rf, rw, rg) -> Tuple[int,int,int,int,int,int]:
        if self.type==TraderType.PATIENT:    return (of+1,ow,og,rf,rw,rg)
        if self.type==TraderType.PICKY:
            f=self.offers_made%3
            if f==0: return (of*2, max(0,ow-1),og, max(1,rf-1),rw,rg)
            if f==1: return (max(0,of-1), ow*2,og, rf, max(1,rw-1),rg)
            return(of,ow,min(og+2,og*2), rf,rw, max(0,rg-1))
        if self.type==TraderType.SCAMMER:    return(of*2,ow*2,og+1, max(1,rf//2), max(1,rw//2), max(0,rg-1))
        return(of+1,ow+1,og, rf,rw,rg)

# SQUARE CLASS -------------------------------------
class Square:
    def __init__(self, x:int, y:int, terrain:Terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.items: List[Item] = []
    def get_items(self) -> List[Item]: return self.items
    def add_item(self, item:Item): self.items.append(item)
    def remove_item(self, item:Item):
        if item in self.items and not item.is_repeating(): self.items.remove(item)
    def has_item(self) -> bool: return bool(self.items)
    def has_trader(self) -> bool:
        return any(isinstance(item, Trader) for item in self.items)
    def __str__(self) -> str:
        if self.items:
            return f"{self.terrain.value.capitalize()} with {', '.join(i.name for i in self.items)}"
        return self.terrain.value.capitalize()

# MAP CLASS ----------------------------------------
class Map:
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        self.squares: List[List[Square]] = [[None]*height for _ in range(width)]
    def generate_map(self, difficulty:Difficulty) -> None:
        # terrain distribution by difficulty
        dist = {
            Difficulty.EASY:   {TerrainType.PLAINS:0.6, TerrainType.FOREST:0.2, TerrainType.SWAMP:0.1, TerrainType.MOUNTAIN:0.05, TerrainType.DESERT:0.05},
            Difficulty.MEDIUM: {TerrainType.PLAINS:0.4, TerrainType.FOREST:0.2, TerrainType.SWAMP:0.2, TerrainType.MOUNTAIN:0.1,  TerrainType.DESERT:0.1},
            Difficulty.HARD:   {TerrainType.PLAINS:0.2, TerrainType.FOREST:0.2, TerrainType.SWAMP:0.2, TerrainType.MOUNTAIN:0.2, TerrainType.DESERT:0.2}
        }[difficulty]
        types, weights = zip(*dist.items())
        for x in range(self.width):
            for y in range(self.height):
                choice = random.choices(types, weights, k=1)[0]
                self.squares[x][y] = Square(x, y, Terrain(choice))
    def populate_items(self, difficulty:Difficulty) -> None:
        # item probabilities by difficulty
        prob = {Difficulty.EASY:0.1, Difficulty.MEDIUM:0.07, Difficulty.HARD:0.05}[difficulty]
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < prob:
                    # random item type
                    itype = random.choice([FoodBonus, WaterBonus, GoldBonus, Trader])
                    if itype is Trader:
                        ttype = random.choice(list(TraderType))
                        self.squares[x][y].add_item(Trader(ttype))
                    else:
                        amount = random.randint(1,3)
                        self.squares[x][y].add_item(itype(amount))
    def get_square(self, x:int, y:int) -> Optional[Square]:
        if 0<=x<self.width and 0<=y<self.height:
            return self.squares[x][y]
        return None
    def get_starting_position(self) -> Tuple[int,int]:
        # west edge, lowest total cost
        return (0,0)
    def is_valid(self, x:int, y:int) -> bool:
        return 0<=x<self.width and 0<=y<self.height
    def __str__(self)->str:
        lines=[]
        for y in range(self.height):
            row=''
            for x in range(self.width):
                sq=self.squares[x][y]
                c=sq.terrain.type.value[0].upper()
                if sq.has_trader(): m='T'
                elif sq.has_item(): m='*'
                else: m=' '
                row+=f"[{c}{m}] "
            lines.append(row)
        return '\n'.join(lines)

# PLAYER CLASS -------------------------------------
class SimplePlayer:
    def __init__(self, x:int, y:int):
        self.x = x; self.y = y
        self.max_strength = 20; self.current_strength = 20
        self.max_food = 20;    self.current_food = 20
        self.max_water = 20;   self.current_water = 20
        self.gold = 0;   self.trader_discount = 0
    def add_resources(self, ds:int, dw:int, df:int, dg:int):
        self.current_strength = max(0, min(self.max_strength, self.current_strength + ds))
        self.current_water   = max(0, min(self.max_water,    self.current_water    + dw))
        self.current_food    = max(0, min(self.max_food,     self.current_food     + df))
        self.gold            = max(0, self.gold + dg)
    def is_alive(self) -> bool:
        return (self.current_strength>0 and self.current_water>0 and self.current_food>0)

# UTILITY FUNCTIONS -------------------------------
def get_map_size() -> Tuple[int,int]:
    while True:
        try:
            w,h = map(int, input("Enter map width and height (e.g. '10 5'): ").split())
            if w>0 and h>0:
                return w,h
        except:
            pass
        print("Invalid input. Please enter two positive integers.")

def get_difficulty() -> Difficulty:
    choices = {'easy':Difficulty.EASY, 'medium':Difficulty.MEDIUM, 'hard':Difficulty.HARD}
    while True:
        d = input("Choose difficulty [easy, medium, hard]: ").strip().lower()
        if d in choices:
            return choices[d]
        print("Invalid choice. Try again.")

def get_direction() -> Tuple[int,int]:
    dirs = {'north':(0,-1), 'south':(0,1), 'east':(1,0), 'west':(-1,0), 'stay':(0,0)}
    while True:
        d = input("Move (north, east, south, west, stay): ").strip().lower()
        if d in dirs:
            return dirs[d]
        print("Invalid direction. Try again.")

# MAIN GAME LOOP -----------------------------------
if __name__ == '__main__':
    # Setup
    width, height = get_map_size()
    difficulty = get_difficulty()
    game_map = Map(width, height)
    game_map.generate_map(difficulty)
    game_map.populate_items(difficulty)
    print("\nGenerated Map:")
    print(game_map)

    # Initialize player
    sx, sy = game_map.get_starting_position()
    player = SimplePlayer(sx, sy)
    print(f"\nStarting stats -> Strength: {player.current_strength}/{player.max_strength}, "
          f"Food: {player.current_food}/{player.max_food}, Water: {player.current_water}/{player.max_water}, Gold: {player.gold}")

    # Game loop
    while True:
        dx, dy = get_direction()
        nx, ny = player.x + dx, player.y + dy
        if not game_map.is_valid(nx, ny):
            print("Cannot move there. Try a different direction.")
            continue

        # Move player
        player.x, player.y = nx, ny
        sq = game_map.get_square(nx, ny)

        # Narrative entry
        print(f"\nPlayer enters square ({nx},{ny}) -> Terrain: {sq.terrain}")

        # Item interactions
        for item in list(sq.get_items()):
            if isinstance(item, FoodBonus):
                print("There's food here!")
            elif isinstance(item, WaterBonus):
                print("I found water!")
            elif isinstance(item, GoldBonus):
                print("I see some gold here!")
            elif isinstance(item, Trader):
                print("There is a trader here.")
                item.offer_trade(player)
            item.apply(player)
            if not item.is_repeating():
                sq.remove_item(item)

        # Deduct terrain costs
        mc = sq.terrain.get_movement_cost()
        wc = sq.terrain.get_water_cost()
        fc = sq.terrain.get_food_cost()
        player.add_resources(-mc, -wc, -fc, 0)
        print(f"Cost -> Strength: -{mc}, Food: -{fc}, Water: -{wc}")
        print(f"Stats -> Strength: {player.current_strength}/{player.max_strength}, "
              f"Food: {player.current_food}/{player.max_food}, Water: {player.current_water}/{player.max_water}, Gold: {player.gold}")

        # Check for end conditions
        if not player.is_alive():
            print("\nYou have perished in the wilderness...")
            break
        if nx == width - 1:
            print("\nCongratulations, you have reached the east edge and survived! 🎉")
            break