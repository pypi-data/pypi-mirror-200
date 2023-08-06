from hldlib import HLDObj, HLDType, HLDError
import pytest


@pytest.fixture
def obj_string() -> str:
    return "obj,Spawner,593,536,352,6,-999999,++,-1=dirk,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,"

def test_from_string(obj_string: str):
    obj = HLDObj.from_string(obj_string)
    assert obj.type == HLDType.SPAWNER
    assert obj.uid == 593
    assert obj.x == 536
    assert obj.y == 352
    assert obj.layer == 6
    assert obj.dependencies == "-999999"
    assert obj.attrs == \
    {
        "-1": "dirk",
        "-2": -999999,
        "-4": 1,
        "-5": 0,
        "-6": -1,
        "-7": 0,
        "-8": 0,
    }

def test_from_string_errors():
    with pytest.raises(HLDError):
        HLDObj.from_string("")
    with pytest.raises(HLDError):
        HLDObj.from_string(",obj,Spawner,593,536,352,6,-999999,++,-1=dirk,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,")
    with pytest.raises(HLDError):
        HLDObj.from_string("obj,Spawner,593,536,6,-999999,++,-1=dirk,-2=-999999,-4=1,-5=0,-6=-1,-7=0,-8=0,")

def test_to_string(obj_string: str):
    obj = HLDObj.from_string(obj_string)
    assert obj_string == obj.to_string().strip().replace("//", "") 
