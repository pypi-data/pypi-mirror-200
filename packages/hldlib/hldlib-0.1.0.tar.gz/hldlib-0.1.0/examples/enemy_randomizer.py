from hldlib import default_load, find_path, HLDType
import random

def main():

    list_of_enemies = [
        "slime", "Birdman", "SmallCrystalSpider", "spider", "Grumpshroom",
        "Wolf", "dirk",  "SpiralBombFrog", "RifleDirk",
        "NinjaStarFrog", "TanukiGun", "CultBird", "missiledirk", "TanukiSword",
        "Melty", "GhostBeamBird", "Leaper", "Dirkommander", "BlaDirk", "CrystalBaby"
    ]

    # Here we load all levels from path/North, path/East, path/..., path/Abyss
    # find_path will search for the hlddir.txt file and read the first line there
    levels = default_load(find_path())

    for level in levels:
        for obj in level.objects:
            if obj.type == HLDType.SPAWNER:
                if obj.attrs["-1"] in list_of_enemies and obj.attrs["-1"] != "Birdman":
                    # Here we found an object that is of a type of Spawner (all enemies are from spawners for some reason)
                    # In a Spawner "-1" attribute is the type of objcect to spawn so we choose a random enemy type
                    # We are only looking for Spawners that will spawn enemies (i.e. from list_of_enemies)
                    # and that will not spawn a Birdman (having them randomized can break arenas)
                    #
                    # So we assign a random enemy to "-1"
                    # and we normalize other attributes (having them not normalized can break arenas too)
                    obj.attrs["-1"] = random.choice(list_of_enemies)
                    obj.attrs["-2"] = 0
                    obj.attrs["-4"] = 1
                    obj.attrs["-5"] = 0
                    obj.attrs["-6"] = -1
                    obj.attrs["-7"] = 0
                    obj.attrs["-8"] = 0

    # And in the end we dump all the changed levels
    # NOTE: dump_all dumps levels in directories named after their direction
    # So dump_all(path) will dump all levels with direction HLDDirection.NORTH in path/North
    levels.dump_all("out")


if __name__ == "__main__":
    main()
