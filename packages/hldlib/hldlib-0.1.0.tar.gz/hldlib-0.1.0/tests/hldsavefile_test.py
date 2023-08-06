from pathlib import Path
from hldlib import HLDSaveFile, hldsavefile
from os.path import join as p_join
import pytest


@pytest.fixture
def testing_savefile() -> HLDSaveFile:
    return HLDSaveFile.from_string("67eb87838659be77713bcdb237b0420a59d817df6eb7cd347d4b75823c138d6876d36e4eab448002eyJiYWRhc3MiOiAwLjAsICJtYXBNb2QiOiAiMTMyPTImPjE0ND0yJj4xNjE9MiY+MTgxPTImPjEwNj0yJj4xMDk9MiY+MTk0PTImPjIyNj0yJj4xODM9MiY+MTc0PTImPjE2MD0yJj4yMTg9MiY+OTU9MiY+MTA0PTImPjIyMD0yJj4yMTA9MiY+IiwgImRhdGVUaW1lIjogNDQ5ODAuNTI0MTI2LCAiaGVhbHRoVXAiOiAwLjAsICJjbCI6ICI5PTEwMTM4NyYxODUyNjcmMjA2MTM5JjI2Njc4NCY+MTM9LTE1MTg4NTEmPjc9LTI1NTEwMCYtMTg3OTA1Ji0xNjczMjYmLTUzMzkyJj42PS0xODk1NDgxJi0xMDQ3NDMwJi05MzI0NzEmLTkwMjIxMiY+OD0tNTU1Mjc5Ji0zOTg2MzUmLTM4NjQ1NyYtNjc2MzU3Jj4iLCAiZGVzdHJ1Y3QiOiAiLTM2MjI0Nj0xNjMmMzcuMjEmPjE4MjYxMj0yMTgmMzAuODQmPi0xOTc3OTEzPTIyMCYyNC42NCY+MTk1Mjk3PTIxOSYzMC40MyY+LTM2ODk5OT0xNjMmMzcuMjEmPjIwNDUwNT0yMjAmMjQuNjQmPjIwNDA1OD0yMjAmMjQuNjQmPjIwNTkwNz0yMjAmMjQuNjQmPjIwMzA3MT0yMjAmMjQuNjQmPi0xODIxODkwPTE3OCYxNS44MiY+LTY0OTEwPTE5MyYxNi4xMCY+LTE5NzkwMDE9MjA5JjMxLjg0Jj4tMTgyODY4ND0xNzEmMTkuMjkmPjE4MTM3Nj0yMTgmMzAuODQmPi0yMTU1NDE9MTc4JjE1LjgyJj4tMjE1MTIyPTE3OCYxNS44MiY+LTIxNDY5MT0xNzgmMTUuODImPi0yMTYyODI9MTc4JjE1LjgyJj4tMTgzNjE3Nj0xNjMmMzcuMjEmPi0xODI4MDIwPTE3MSYxOS4yOSY+MjAxMDk2PTIyMCYyNC42NCY+LTE3Nzk0MDg9MjIwJjI0LjY0Jj4tNDg2MTA9MTk1JjE3LjI5Jj4tMTc4MDI0MT0yMTkmMzAuNDMmPjIwNzQzNT0yMjAmMjQuNjQmPi0xOTE1ODQ1PTg0JjIuNzcmPi0zNTcwNzA9MTY0JjM4LjU1Jj4tMjEzNjY1PTE3OCYxNS44MiY+LTI1MzY3Mj0xNzQmMTguNTYmPjE4MjEwND0yMTgmMzAuODQmPjkxNTc2PTIwOSYzMS44NCY+LTIxMjE0MT0xNzgmMTUuODImPi0zNTQzNDg9MTY0JjM4LjU1Jj4xNDczNDg9MjE0JjMxLjI4Jj4tMjE3MTMzPTE3OCYxNS44MiY+OTQ1MDY9MjA5JjMxLjg0Jj4tMjEyMDI0PTE3OCYxNS44MiY+LTI1MjIwNj0xNzQmMTguNTYmPi0zNzMzOTU9MTYyJjM2Ljk4Jj4xODU1MjU9MjE4JjMwLjg0Jj4tMTk1MzYwNT00NiY4LjM1Jj4tMjcxOTUxPTE3MiYxOS4wNCY+LTI1NTc5Nz0xNzQmMTguNTYmPi0yMTI4MDM9MTc4JjE1LjgyJj4xODMyNDA9MjE4JjMwLjg0Jj4tMTgyMTYwNz0xNzgmMTUuODImPjE4NTM5Mz0yMTgmMzAuODQmPi0zNTY3MTY9MTY0JjM4LjU1Jj4tMjg3MjMyPTE3MSYxOS4yOSY+MTQ2OTcwPTIxNCYzMS4yOCY+LTE3Nzk4Mjc9MjIwJjI0LjY0Jj4yMDQ2MzY9MjIwJjI0LjY0Jj4xOTQ4NDA9MjE5JjMwLjQzJj4tMzUzMDY2PTE2NCYzOC41NSY+MTgyNDE4PTIxOCYzMC44NCY+MjA1ODYyPTIyMCYyNC42NCY+LTQyMzg3PTE5NSYxNy4yOSY+LTE3NzQyNjM9MjI1JjMwLjE1Jj4tMjE3MDUzPTE3OCYxNS44MiY+MjA0NTM1PTIyMCYyNC42NCY+LTM1MzI4Mj0xNjQmMzguNTUmPi0xNzgxNjk5PTIxOCYzMC44NCY+MTg3NTM3PTIxOCYzMC44NCY+LTE4MDUxMzg9MTk0JjE3LjQ3Jj4yMDc3NDM9MjIwJjI0LjY0Jj4tNjI0MTY9MTkzJjE2LjEwJj4tMjEzNDAyPTE3OCYxNS44MiY+LTM2MzM2Nz0xNjMmMzcuMjEmPi0yMTgwODQ9MTc4JjE1LjgyJj4tMzc1NTE0PTE2MiYzNi45OCY+LTY3NDcxPTE5MyYxNi4xMCY+LTE1MzI5NzY9NDYmOC4zNSY+MjAzOTA4PTIyMCYyNC42NCY+LTIxNTc5Mz0xNzgmMTUuODImPi0yMTIwNTM9MTc4JjE1LjgyJj4yMDM3NjM9MjIwJjI0LjY0Jj4tMzYyMzQ4PTE2MyYzNy4yMSY+MjAxNDI4PTIyMCYyNC42NCY+MTg0MTU1PTIxOCYzMC44NCY+MTgzOTM5PTIxOCYzMC44NCY+MTQ1MjUzPTIxNCYzMS4yOCY+MTQ1NzkyPTIxNCYzMS4yOCY+LTQ4NTUyPTE5NSYxNy4yOSY+LTI3NDcyMz0xNzImMTkuMDQmPiIsICJ2YWx1ZXMiOiAiVmFsdWViYWRhc3NPZmZpY2VTdGF0ZT0yPiIsICJndW5SZW1pbmRlclRpbWVzIjogMC4wLCAiZmlyZXBsYWNlU2F2ZSI6IDAuMCwgImNoZWNrSFAiOiA1LjAsICJjb21wU2hlbGwiOiAwLjAsICJjU3dvcmRzIjogIjArIiwgImNhcGUiOiAwLjAsICJoYWxsdWMiOiAwLjAsICJuZXdjb21lckhvYXJkZU1lc3NhZ2VTaG93biI6IDAuMCwgInR1dEhlYWwiOiAwLjAsICJub1NwYXduIjogIi0xMDk3OTU0Ky0xNDU1MDQrLTE4NzExNjUrIiwgImNoZWNrWSI6IDYwOC4wLCAic3BlY2lhbFVwIjogMC4wLCAiY2hlY2tCYXQiOiAxMDAuMCwgIm5vdmljZU1vZGUiOiAwLjAsICJzdWNjZXNzZnVsSGVhbFRpbWVzIjogNS4wLCAiY0NhcGVzIjogIjArIiwgIkNIIjogMC4wLCAiZ2VhciI6IDAuMCwgImNoZWNrQ0lEIjogNjI0NTMxLjAsICJyb29tcyI6ICI0Nis3OSs0Nys0OCs0OSs1MCs1Mys2MSs2Mis4NCs4NSs4OCs5MCs5Mis5Mys5NCsxMDQrOTUrMTA2KzEwNysxMDgrMTA5Kzk2Kzk3KzY0KzE3MSsxNzIrMTczKzE3NCsxNzUrMTc3KzE4MSsxODIrMTgzKzE4NCsxODUrMTc4KzE5MysxOTQrMTk1KzE5Nis2NSsyMDkrMjEwKzIxMSsyMTQrMjE4KzIxOSsyMjArMjI1KzIyNisyMzgrMjQ4KzI0NysyNDYrNjMrMTI4KzEzMCsxNDQrMTUyKzE2MCsxNjErMTYyKzE2MysxNjQrMTY1KzEzMisyNTYrMjU3KzI1OCsyNTkrMjYyKyIsICJwZXJtYVMiOiAiLTEwNDc5NDA9Mj4tNjkyMjMyPTI+LTEzODcwNTY9Mj4tNjk3MzYxPTI+LTE4MzM1Mz0yPjM4Mzk4OT0yPiIsICJjaGVja1Jvb20iOiAyNjIuMCwgIndlbGxNYXAiOiAiMSswKzIrMysiLCAiY1NoZWxscyI6ICIwKyIsICJ0YWJsZXQiOiAiIiwgInN1Y2Nlc3NmdWxXYXJwVGltZXMiOiAwLjAsICJza2lsbCI6ICIiLCAiYm9zc2VzIjogIjMuMjA9MzExJjIyNiY+IiwgInNjSyI6ICIxPTExPiIsICJ3YXJwIjogIjArMiszKyIsICJoYXNNYXAiOiAwLjAsICJldmVudHMiOiAiLTE1MzQyMTQrLTE1MTc2NjkrLTE0OTc2NjQrLTI1MjY5NCstMjI2OTc1Ky0xODA2NTkrLTE3NDg1NCstMTgyNDUzMystNDU2NzcrMjUzNDI2KzM4NTUwMSstMzk2MjcyKy0zNDQ5MjIrNTg2NjY2KzYyNjc3NisiLCAiZ2VhclJlbWluZGVyVGltZXMiOiAwLjAsICJlbmVtaWVzIjogIi0xODY4Mzk9MTgxJjEyLjE0Jj4tMTg2MjcxPTE4MSYxMi4xNCY+MjU1NTk4PTIyNSYzMC4xNSZzcHJfU21hbGxDcnlzdGFsU3BpZGVyRGVhZCYxJjUxNiY2OTgmLTEmPjI1MTYxOD0yMjUmMzAuMTUmc3ByX1JpZmxlRGlya0RlYWQmMSY0OTUmNzIwJi0xJj4tMjEyODI1PTE3OCYxNS44MiZzcHJfTmluamFGcm9nRGVhZCYxJjczMyYxNjImLTEmPi0xNjM0MDk9MTgzJjE0LjQ1Jj4yMDI5NTk9MjIwJjI0LjY0JnNwcl9Xb2xmRGVhZCYxJjY3MSYzNzMmMSY+LTkxNDgwMT0xMDgmNy42MyZzcHJfQ3VsdEJpcmREZWFkJjEmNTgyJjIzOSYtMSY+LTE5NTEyNzA9NDgmOS4xMCZzcHJfUmlmbGVEaXJrRGVhZCYxJjExODcmMTA5MCYxJj4yNTU4MzI9MjI1JjMwLjE1JnNwcl9TbWFsbENyeXN0YWxTcGlkZXJEZWFkJjEmNTk3JjY4NiYxJj4tMTkzNzQwNj02MiYyLjM3JnNwcl9EaXJrRGVhZCYxJjUyMiYzNzgmLTEmPi0xNjY3MTg9MTgzJjE0LjQ1JnNwcl9SaWZsZURpcmtEZWFkJjEmNjcyJjkxNyYtMSY+NDcxMDUyPTI0NyYyOS41OCY+LTE4NTc1Mj0xODEmMTIuMTQmPi02Mzc3OT0xOTMmMTYuMTAmc3ByX1JpZmxlRGlya0RlYWQmMSYxMDk3JjE0NzMmLTEmPi0xMzQ2Mjk3PTY1JjMyLjA4JnNwcl9TcGlkZXJEZWFkJjEmOTYmNDM0JjEmPjIwMjQ4Mz0yMjAmMjQuNjQmc3ByX1dvbGZEZWFkJjEmMzAzJjI0NCYxJj4yMDQyNjc9MjIwJjI0LjY0JnNwcl9Xb2xmRGVhZCYxJjUxMCYzNTImLTEmPi0xNTIzMzAwPTQ3JjguNzEmc3ByX0RpcmtEZWFkJjEmNzgxJjU0MCYtMSY+NDc3NzQ4PTI0NyYyOS41OCY+MjU1NzcyPTIyNSYzMC4xNSZzcHJfU21hbGxDcnlzdGFsU3BpZGVyRGVhZCYxJjU5NiY2OTAmLTEmPi0xNjg2ODY9MTgzJjE0LjQ1Jj4tMzk3NDQ3PTE2MCYzNi4xNiZzcHJfTWlzc2lsZURpcmtEZWFkJjEmMjcyJjg5MyYtMSY+LTkzODU3Mz0xMDYmNy4wNiZzcHJfUmlmbGVEaXJrRGVhZCYxJjM2OSY0MTcmMSY+MjU2ODk3PTIyNSYzMC4xNSZzcHJfU21hbGxDcnlzdGFsU3BpZGVyRGVhZCYxJjgxNCY2ODMmMSY+LTE1MTgzODE9NDgmOS4xMCZzcHJfRGlya0RlYWQmMSYxMjAyJjExMTMmLTEmPjIwNTYxOT0yMjAmMjQuNjQmc3ByX1dvbGZEZWFkJjEmNjE5JjMzMyYxJj4yMDEyODM9MjIwJjI0LjY0JnNwcl9Xb2xmRGVhZCYxJjY1NCYzNzYmMSY+LTM4NzczOD0xNjEmMzYuNTQmc3ByX1JpZmxlRGlya0RlYWQmMSY0MDgmMTQ2Ji0xJj4tMTgxNjUyMj0xODMmMTQuNDUmPjE4NTYzNT0yMTgmMzAuODQmc3ByX1RhbnVraURlYWQmMSYxMTk2JjEwNjImLTEmPjIwNDA4MD0yMjAmMjQuNjQmc3ByX1dvbGZEZWFkJjEmNTYyJjM0MiYxJj4tMTgxNjcxMz0xODMmMTQuNDUmPi0xMzc1ODg2PTYyJjIuMzcmc3ByX0RpcmtEZWFkJjEmNTA0JjQwNSYtMSY+LTE2NDc1Mj0xODMmMTQuNDUmc3ByX1JpZmxlRGlya0RlYWQmMSY0NTYmNzc5JjEmPi0xODE2MTM3PTE4MyYxNC40NSZzcHJfUmlmbGVEaXJrRGVhZCYxJjY0MSYxMDg4Ji0xJj4tNjI1NjY9MTkzJjE2LjEwJnNwcl9EaXJrRGVhZCYxJjEyODcmMTQ1NCYtMSY+MjAyMzE1PTIyMCYyNC42NCZzcHJfV29sZkRlYWQmMSY1MDcmMzcxJi0xJj4xNDI1Mjk9MjE0JjMxLjI4JnNwcl9EaXJrRGVhZCYxJjEyMjgmOTkzJi0xJj4tMTgyMTUxMT0xNzgmMTUuODImc3ByX05pbmphRnJvZ0RlYWQmMSY2OTEmMTk5JjEmPi0xNzc0NjAxPTIyNSYzMC4xNSZzcHJfU21hbGxDcnlzdGFsU3BpZGVyRGVhZCYxJjc2MSY2NjAmMSY+LTE2ODUzND0xODMmMTQuNDUmPi0xMzU2MjU5PTY0JjE5LjYzJnNwcl9TcGlkZXJEZWFkJjEmNDIxJjIyNSYxJj4tMjE3NTYwPTE3OCYxNS44MiZzcHJfSmFyRnJvZ0RlYWQmMSY4ODcmMzE5JjEmPi0xNjc3MTc9MTgzJjE0LjQ1JnNwcl9SaWZsZURpcmtEZWNhcEJvdHRvbSYxJjQ1NiY3NjEmLTEmPi05MzQ5MDQ9MTA2JjcuMDYmc3ByX1JpZmxlRGlya0RlYWQmMSYzNTYmNDQ5JjEmPjI1NTQ2MD0yMjUmMzAuMTUmc3ByX1JpZmxlRGlya0RlYWQmMSY2MjMmNjc2JjEmPi02MzY3OT0xOTMmMTYuMTAmc3ByX0RpcmtEZWFkJjEmMTM0NiYxNDQ2Ji0xJj4tMTgzNjc0MT0xNjMmMzcuMjEmPjIwMzg2Mj0yMjAmMjQuNjQmc3ByX1dvbGZEZWFkJjEmNjUyJjM1OCYtMSY+MjAzMDY2PTIyMCYyNC42NCZzcHJfV29sZkRlYWQmMSY1MDcmMzQwJjEmPi0yMTIzNTM9MTc4JjE1LjgyJnNwcl9KYXJGcm9nRGVhZCYxJjkyMSYyMDEmLTEmPi0xMzUzMzk4PTY0JjE5LjYzJnNwcl9TcGlkZXJEZWFkJjEmNDAzJjIxNCYxJj4yNTEyNTk9MjI1JjMwLjE1JnNwcl9TbWFsbENyeXN0YWxTcGlkZXJEZWFkJjEmODMyJjY5NCYxJj4tMTY1MzAxPTE4MyYxNC40NSZzcHJfRGlya0RlYWQmMSY2NDgmODk3Ji0xJj4tMTY1MzQ2PTE4MyYxNC40NSZzcHJfUmlmbGVEaXJrRGVhZCYxJjY3MyYxMDg4JjEmPi0xNTE0NTMyPTQ4JjkuMTAmc3ByX0RpcmtEZWFkJjEmMTI0NSYxMDk0Ji0xJj4tMTY0MzQ3PTE4MyYxNC40NSY+IiwgInNjVXAiOiAiIiwgImNoZWNrWCI6IDM0Ny4wLCAiYm9zc0dlYXJiaXRzIjogIiIsICJjdWVzIjogIi0xMDkyMDE5Ky0xMDkyNTE3Ky0xMDczMzY2Ky0xMDU1NTc2Ky0yNzYxMjYrLTE4MTQxMjcrLTE0NzU0NystMjE0MDI3Ky03MTYwOTIrIiwgInBsYXlUIjogNDEuMCwgIndlbGwiOiAiMSswKzIrMysiLCAic2MiOiAiMSsiLCAiZHJpZnRlcmtleSI6IDAuMCwgInN1Y2Nlc3NmdWxDb2xsZWN0VGltZXMiOiAwLjAsICJjaGVja0FtbW8iOiAwLjAsICJjaGVja1N0YXNoIjogMS4wLCAiY2hhckRlYXRocyI6IDEyLjAsICJlcTAwIjogMS4wLCAiaGVhbHRoS2l0cyI6ICItMTUzMzYzOSstMTUyNzIxMistMTUyNzA0MSstOTM0OTUxKy0xMzUzNDYzKy0xNjY3OTgrLTE3ODY2NCstNjM3OTErLTUzODM2KzE0NjIyNSstMTc3NDIyMistMzg3OTAzKy0zNjc2MjErLTM0MjM0NistNjczMjA3KyIsICJzd29yZCI6IDAuMCwgImdhbWVOYW1lIjogIlEifSA=")

def test_load(testing_savefile: HLDSaveFile):
    assert testing_savefile.badass == 0.
    assert testing_savefile.mapMod == {"132": ["2"], "144": ["2"], "161": ["2"], "181": ["2"], "106": ["2"], "109": ["2"], "194": ["2"], "226": ["2"], "183": ["2"], "174": ["2"], "160": ["2"], "218": ["2"], "95": ["2"], "104": ["2"], "220": ["2"], "210": ["2"]}
    assert testing_savefile.dateTime == 44980.524126
    assert testing_savefile.healthUp == 0.
    assert testing_savefile.cl == {"9": ["101387", "185267", "206139", "266784"], "13": ["-1518851"], "7": ["-255100", "-187905", "-167326", "-53392"], "6": ["-1895481", "-1047430", "-932471", "-902212"], "8": ["-555279", "-398635", "-386457", "-676357"]}
    assert testing_savefile.destruct == {"-362246": ["163", "37.21"], "182612": ["218", "30.84"], "-1977913": ["220", "24.64"], "195297": ["219", "30.43"], "-368999": ["163", "37.21"], "204505": ["220", "24.64"], "204058": ["220", "24.64"], "205907": ["220", "24.64"], "203071": ["220", "24.64"], "-1821890": ["178", "15.82"], "-64910": ["193", "16.10"], "-1979001": ["209", "31.84"], "-1828684": ["171", "19.29"], "181376": ["218", "30.84"], "-215541": ["178", "15.82"], "-215122": ["178", "15.82"], "-214691": ["178", "15.82"], "-216282": ["178", "15.82"], "-1836176": ["163", "37.21"], "-1828020": ["171", "19.29"], "201096": ["220", "24.64"], "-1779408": ["220", "24.64"], "-48610": ["195", "17.29"], "-1780241": ["219", "30.43"], "207435": ["220", "24.64"], "-1915845": ["84", "2.77"], "-357070": ["164", "38.55"], "-213665": ["178", "15.82"], "-253672": ["174", "18.56"], "182104": ["218", "30.84"], "91576": ["209", "31.84"], "-212141": ["178", "15.82"], "-354348": ["164", "38.55"], "147348": ["214", "31.28"], "-217133": ["178", "15.82"], "94506": ["209", "31.84"], "-212024": ["178", "15.82"], "-252206": ["174", "18.56"], "-373395": ["162", "36.98"], "185525": ["218", "30.84"], "-1953605": ["46", "8.35"], "-271951": ["172", "19.04"], "-255797": ["174", "18.56"], "-212803": ["178", "15.82"], "183240": ["218", "30.84"], "-1821607": ["178", "15.82"], "185393": ["218", "30.84"], "-356716": ["164", "38.55"], "-287232": ["171", "19.29"], "146970": ["214", "31.28"], "-1779827": ["220", "24.64"], "204636": ["220", "24.64"], "194840": ["219", "30.43"], "-353066": ["164", "38.55"], "182418": ["218", "30.84"], "205862": ["220", "24.64"], "-42387": ["195", "17.29"], "-1774263": ["225", "30.15"], "-217053": ["178", "15.82"], "204535": ["220", "24.64"], "-353282": ["164", "38.55"], "-1781699": ["218", "30.84"], "187537": ["218", "30.84"], "-1805138": ["194", "17.47"], "207743": ["220", "24.64"], "-62416": ["193", "16.10"], "-213402": ["178", "15.82"], "-363367": ["163", "37.21"], "-218084": ["178", "15.82"], "-375514": ["162", "36.98"], "-67471": ["193", "16.10"], "-1532976": ["46", "8.35"], "203908": ["220", "24.64"], "-215793": ["178", "15.82"], "-212053": ["178", "15.82"], "203763": ["220", "24.64"], "-362348": ["163", "37.21"], "201428": ["220", "24.64"], "184155": ["218", "30.84"], "183939": ["218", "30.84"], "145253": ["214", "31.28"], "145792": ["214", "31.28"], "-48552": ["195", "17.29"], "-274723": ["172", "19.04"]}
    assert testing_savefile.values == {'ValuebadassOfficeState': ['2']}
    assert testing_savefile.gunReminderTimes == 0.
    assert testing_savefile.fireplaceSave == 0.
    assert testing_savefile.checkHP == 5.
    assert testing_savefile.compShell == 0.
    assert testing_savefile.cSwords == ["0"]
    assert testing_savefile.cape == 0.
    assert testing_savefile.halluc == 0.
    assert testing_savefile.newcomerHoardeMessageShown == 0.
    assert testing_savefile.tutHeal == 0.
    assert testing_savefile.noSpawn == ['-1097954', '-145504', '-1871165']
    assert testing_savefile.checkY == 608.
    assert testing_savefile.specialUp == 0.
    assert testing_savefile.checkBat == 100.
    assert testing_savefile.noviceMode == 0.
    assert testing_savefile.successfulHealTimes == 5.
    assert testing_savefile.cCapes == ["0"]
    assert testing_savefile.CH == 0.
    assert testing_savefile.gear == 0.
    assert testing_savefile.checkCID == 624531.
    assert testing_savefile.rooms == ["46", "79", "47", "48", "49", "50", "53", "61", "62", "84", "85", "88", "90", "92", "93", "94", "104", "95", "106", "107", "108", "109", "96", "97", "64", "171", "172", "173", "174", "175", "177", "181", "182", "183", "184", "185", "178", "193", "194", "195", "196", "65", "209", "210", "211", "214", "218", "219", "220", "225", "226", "238", "248", "247", "246", "63", "128", "130", "144", "152", "160", "161", "162", "163", "164", "165", "132", "256", "257", "258", "259", "262"]
    assert testing_savefile.permaS == {"-1047940": ["2"], "-692232": ["2"], "-1387056": ["2"], "-697361": ["2"], "-183353": ["2"], "383989": ["2"]}
    assert testing_savefile.checkRoom == 262.
    assert testing_savefile.wellMap == ["1", "0", "2", "3"]
    assert testing_savefile.cShells == ["0"]
    assert testing_savefile.eq01 == 0.
    assert testing_savefile.tablet == []
    assert testing_savefile.successfulWarpTimes == 0.
    assert testing_savefile.skill == []
    assert testing_savefile.bosses == {'3.20': ['311', '226']}
    assert testing_savefile.scK == {'1': ['11']}
    assert testing_savefile.warp == ['0', '2', '3']
    assert testing_savefile.hasMap == 0.
    assert testing_savefile.events == ["-1534214", "-1517669", "-1497664", "-252694", "-226975", "-180659", "-174854", "-1824533", "-45677", "253426", "385501", "-396272", "-344922", "586666", "626776"]
    assert testing_savefile.gearReminderTimes == 0.
    assert testing_savefile.enemies == {"-186839": ["181", "12.14"], "-186271": ["181", "12.14"], "255598": ["225", "30.15", "spr_SmallCrystalSpiderDead", "1", "516", "698", "-1"], "251618": ["225", "30.15", "spr_RifleDirkDead", "1", "495", "720", "-1"], "-212825": ["178", "15.82", "spr_NinjaFrogDead", "1", "733", "162", "-1"], "-163409": ["183", "14.45"], "202959": ["220", "24.64", "spr_WolfDead", "1", "671", "373", "1"], "-914801": ["108", "7.63", "spr_CultBirdDead", "1", "582", "239", "-1"], "-1951270": ["48", "9.10", "spr_RifleDirkDead", "1", "1187", "1090", "1"], "255832": ["225", "30.15", "spr_SmallCrystalSpiderDead", "1", "597", "686", "1"], "-1937406": ["62", "2.37", "spr_DirkDead", "1", "522", "378", "-1"], "-166718": ["183", "14.45", "spr_RifleDirkDead", "1", "672", "917", "-1"], "471052": ["247", "29.58"], "-185752": ["181", "12.14"], "-63779": ["193", "16.10", "spr_RifleDirkDead", "1", "1097", "1473", "-1"], "-1346297": ["65", "32.08", "spr_SpiderDead", "1", "96", "434", "1"], "202483": ["220", "24.64", "spr_WolfDead", "1", "303", "244", "1"], "204267": ["220", "24.64", "spr_WolfDead", "1", "510", "352", "-1"], "-1523300": ["47", "8.71", "spr_DirkDead", "1", "781", "540", "-1"], "477748": ["247", "29.58"], "255772": ["225", "30.15", "spr_SmallCrystalSpiderDead", "1", "596", "690", "-1"], "-168686": ["183", "14.45"], "-397447": ["160", "36.16", "spr_MissileDirkDead", "1", "272", "893", "-1"], "-938573": ["106", "7.06", "spr_RifleDirkDead", "1", "369", "417", "1"], "256897": ["225", "30.15", "spr_SmallCrystalSpiderDead", "1", "814", "683", "1"], "-1518381": ["48", "9.10", "spr_DirkDead", "1", "1202", "1113", "-1"], "205619": ["220", "24.64", "spr_WolfDead", "1", "619", "333", "1"], "201283": ["220", "24.64", "spr_WolfDead", "1", "654", "376", "1"], "-387738": ["161", "36.54", "spr_RifleDirkDead", "1", "408", "146", "-1"], "-1816522": ["183", "14.45"], "185635": ["218", "30.84", "spr_TanukiDead", "1", "1196", "1062", "-1"], "204080": ["220", "24.64", "spr_WolfDead", "1", "562", "342", "1"], "-1816713": ["183", "14.45"], "-1375886": ["62", "2.37", "spr_DirkDead", "1", "504", "405", "-1"], "-164752": ["183", "14.45", "spr_RifleDirkDead", "1", "456", "779", "1"], "-1816137": ["183", "14.45", "spr_RifleDirkDead", "1", "641", "1088", "-1"], "-62566": ["193", "16.10", "spr_DirkDead", "1", "1287", "1454", "-1"], "202315": ["220", "24.64", "spr_WolfDead", "1", "507", "371", "-1"], "142529": ["214", "31.28", "spr_DirkDead", "1", "1228", "993", "-1"], "-1821511": ["178", "15.82", "spr_NinjaFrogDead", "1", "691", "199", "1"], "-1774601": ["225", "30.15", "spr_SmallCrystalSpiderDead", "1", "761", "660", "1"], "-168534": ["183", "14.45"], "-1356259": ["64", "19.63", "spr_SpiderDead", "1", "421", "225", "1"], "-217560": ["178", "15.82", "spr_JarFrogDead", "1", "887", "319", "1"], "-167717": ["183", "14.45", "spr_RifleDirkDecapBottom", "1", "456", "761", "-1"], "-934904": ["106", "7.06", "spr_RifleDirkDead", "1", "356", "449", "1"], "255460": ["225", "30.15", "spr_RifleDirkDead", "1", "623", "676", "1"], "-63679": ["193", "16.10", "spr_DirkDead", "1", "1346", "1446", "-1"], "-1836741": ["163", "37.21"], "203862": ["220", "24.64", "spr_WolfDead", "1", "652", "358", "-1"], "203066": ["220", "24.64", "spr_WolfDead", "1", "507", "340", "1"], "-212353": ["178", "15.82", "spr_JarFrogDead", "1", "921", "201", "-1"], "-1353398": ["64", "19.63", "spr_SpiderDead", "1", "403", "214", "1"], "251259": ["225", "30.15", "spr_SmallCrystalSpiderDead", "1", "832", "694", "1"], "-165301": ["183", "14.45", "spr_DirkDead", "1", "648", "897", "-1"], "-165346": ["183", "14.45", "spr_RifleDirkDead", "1", "673", "1088", "1"], "-1514532": ["48", "9.10", "spr_DirkDead", "1", "1245", "1094", "-1"], "-164347": ["183", "14.45"]}
    assert testing_savefile.scUp == []
    assert testing_savefile.checkX == 347.
    assert testing_savefile.bossGearbits == []
    assert testing_savefile.cues == ["-1092019", "-1092517", "-1073366", "-1055576", "-276126", "-1814127", "-147547", "-214027", "-716092"]
    assert testing_savefile.playT == 41.
    assert testing_savefile.well == ['1', '0', '2', '3']
    assert testing_savefile.sc == ["1"]
    assert testing_savefile.drifterkey == 0.
    assert testing_savefile.successfulCollectTimes == 0.
    assert testing_savefile.checkAmmo == 0.
    assert testing_savefile.checkStash == 1.
    assert testing_savefile.charDeaths == 12.
    assert testing_savefile.eq00 == 1.
    assert testing_savefile.healthKits == ["-1533639", "-1527212", "-1527041", "-934951", "-1353463", "-166798", "-178664", "-63791", "-53836", "146225", "-1774222", "-387903", "-367621", "-342346", "-673207"]
    assert testing_savefile.sword == 0.
    assert testing_savefile.gameName == "Q"

def test_dump_and_load(tmp_path: Path, testing_savefile: HLDSaveFile):
    testing_savefile.dump(p_join(tmp_path, "hello.sav"))
    dumped_savefile = HLDSaveFile.load(p_join(tmp_path, "hello.sav"))
    assert testing_savefile == dumped_savefile

def test_dump_and_load_error(tmp_path: Path, testing_savefile: HLDSaveFile):
    with pytest.raises(Exception):
        testing_savefile.badass = ['1', '0', '2', '3'] # type: ignore
        testing_savefile.dump(p_join(tmp_path, "hello.sav"))
        HLDSaveFile.load(p_join(tmp_path, "hello.sav"))

def test_sflist():
    testing_sflist = hldsavefile.sflist.from_string("1+2+3+4+")
    testing_sflist.append("5")
    assert testing_sflist.to_string() == "1+2+3+4+5+"

    testing_sflist = hldsavefile.sflist.from_string("1+2+3+4+")
    testing_sflist.remove("2")
    assert testing_sflist.to_string() == "1+3+4+"

    testing_sflist = hldsavefile.sflist.from_string("")
    assert testing_sflist.to_string() == ""

    testing_sflist = hldsavefile.sflist.from_string("1+")
    assert testing_sflist.to_string() == "1+"

def test_sfdict():
    testing_sflist = hldsavefile.sfdict.from_string("1=1&2&3&>2=4&5&6&>")
    assert testing_sflist["1"] == ["1", "2", "3"]

    testing_sflist["3"] = ["7", "8", "9"]
    assert testing_sflist.to_string() == "1=1&2&3&>2=4&5&6&>3=7&8&9&>"

    testing_sflist = hldsavefile.sfdict()
    assert testing_sflist.to_string() == ""

    testing_sflist = hldsavefile.sfdict({"1": ["1"]})
    assert testing_sflist.to_string() == "1=1&>"