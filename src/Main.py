from model.DungeonCharacter import DungeonCharacter
from model.Hero import Hero
from model.Monster import Monster
from model.Skeleton import Skeleton
from model.Ogre import Ogre
from model.Gremlin import Gremlin
from model.Warrior import Warrior
from model.Thief import Thief
from model.Priestess import Priestess

# to test if the class can be instantiated

war = Warrior("warrior bob")
thi = Thief("thief joe")
pri = Priestess("priest alice")

ogre = Ogre("Shrek")
skeleton = Skeleton("Bones")
gremlin = Gremlin("Gizmo")

count = 0

print(f"{ogre.get_name()} health:", ogre.get_health())
while ogre.get_health() > 0:
    health = ogre.get_health()
    war.attack(ogre)
    if ogre.get_health() == health:
        print(f"{war.get_name()} missed!")
    else:
        print(f"{war.get_name()} hit {ogre.get_name()} for", health - ogre.get_health(), "damage")
        print(f"{ogre.get_name()} health:", ogre.get_health())
    count += 1
print(f"{ogre.get_name()} defeated! took {count} turns")
