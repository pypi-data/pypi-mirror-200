from pathlib import Path

import pytest
from hldlib import Counter, find_path, HLDError, default_load, HLDLevel, HLDObj, HLDDirection

def test_counter(): # Why?
    a = Counter(1)
    assert a.use() == 2
    assert a.use() == 3
    assert a.use() == 4

def test_find_path(tmp_path: Path):
    with pytest.raises(HLDError):
        find_path("hlddir.txt", tmp_path)
    sub = tmp_path / "sub"; sub.mkdir()
    hlddir = sub / "hlddir.txt"
    hlddir.write_text("C://...")
    assert find_path("hlddir.txt", tmp_path) == "C://..."

def test_default_load(tmp_path: Path):

    level = HLDLevel(
        name="rm_A_Test.lvl",
        date=50000.00,
        layer_names={
            0: "Door",
            1: "Block",
            2: "Veg",
            3: "Obj",
            4: "Wall"
        },
        room_settings={
            "lb": 0,
            "bg": "<undefined>",
            "floorSpr": "bg_C_Floor_Dregs",
            "bri": 1,
            "liteOff": 0,
            "over": "bg_C_Dregs_N_Overlay",
            "overPit": 0,
            "wallsTop": 1,
            "shadows": 1,
            "flrOutline": 1,
            "flrOC": 16777215,
            "flrOSpr": "<undefined>",
            "wallO": 0,
            "w": 1024,
            "h": 1888,
            "sketchalpha": [
                0.5,
                1,
                0
            ]
        },
        objects=[
            HLDObj.from_string("obj,Spawner,5643,522,717,3,-999999,++,-1=Crate,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,"),
            HLDObj.from_string("obj,Spawner,2261,540,719,3,-999999,++,-1=CrateBig,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,"),
            HLDObj.from_string("obj,Spawner,4066,480,728,3,-999999,++,-1=Crate,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,"),
            HLDObj.from_string("obj,Spawner,7726,464,728,3,-999999,++,-1=Crate,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,"),
            HLDObj.from_string("obj,Spawner,1324,464,752,3,-999999,++,-1=MultiHitCrate,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,"),
        ],
        direction=HLDDirection.ABYSS
    )

    north = tmp_path / "North"; north.mkdir(); level.dump(north) 
    east = tmp_path / "East"; east.mkdir(); level.dump(east) 
    west = tmp_path / "West"; west.mkdir(); level.dump(west) 
    south = tmp_path / "South"; south.mkdir(); level.dump(south) 
    central = tmp_path / "Central"; central.mkdir(); level.dump(central) 
    intro = tmp_path / "Intro"; intro.mkdir(); level.dump(intro) 
    abyss = tmp_path / "Abyss"; abyss.mkdir(); level.dump(abyss) 

    loaded = default_load(tmp_path)
    assert len(loaded) == 7
    assert loaded[0].direction != loaded[1].direction