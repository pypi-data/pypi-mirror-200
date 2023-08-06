from pathlib import Path
from hldlib import HLDDirection, HLDLevel, HLDObj, get_id_from_name, get_name_from_id, HLDError
from os.path import join as p_join
import copy
import pytest

@pytest.fixture
def testing_level() -> HLDLevel:
    return HLDLevel(
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


def test_dump_and_load(tmp_path: Path, testing_level: HLDLevel):
    testing_level.dump(tmp_path)
    dumped_level = HLDLevel.load(p_join(tmp_path, testing_level.name), HLDDirection.ABYSS)
    assert testing_level == dumped_level

def test_load_errors(tmp_path: Path, testing_level: HLDLevel):

    level1 = copy.deepcopy(testing_level)
    level1.layer_names = {}
    level1.name = "rm_A_Test1.lvl"
    level1.dump(tmp_path)

    level2 = copy.deepcopy(testing_level)
    level2.date = '' # type: ignore
    level2.name = "rm_A_Test2.lvl"
    level2.dump(tmp_path)

    level3 = copy.deepcopy(testing_level)
    level3.room_settings = {}
    level3.name = "rm_A_Test3.lvl"

    with pytest.raises(IndexError):
        HLDLevel.load(p_join(tmp_path, level1.name), HLDDirection.ABYSS)

    with pytest.raises(ValueError):
        HLDLevel.load(p_join(tmp_path, level2.name), HLDDirection.ABYSS)
        
    with pytest.raises(KeyError):
        level3.dump(tmp_path)

def test_get_ids_and_names():
    assert get_id_from_name("rm_IN_01_brokenshallows.lvl") == 46
    assert get_name_from_id(46) == "rm_IN_01_brokenshallows.lvl"

def test_ids_and_names_errors():
    with pytest.raises(HLDError):
        get_id_from_name("rm_A_DoesntExist.lvl")
    with pytest.raises(HLDError):
        get_name_from_id(0)