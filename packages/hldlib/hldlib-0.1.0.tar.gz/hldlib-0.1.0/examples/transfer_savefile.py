from hldlib import HLDSaveFile

def main():
    # old_savefile is the savefile we want to transfer to a new machine
    # new_savefile is a savefile from the new machine
    old_savefile = HLDSaveFile.load("C://SavefileFrom.sav")
    new_savefile = HLDSaveFile.load("C://SavefileTo.sav")

    # In HLD savefiles are machine specific 
    # So we transplant the new header to the old savefile
    old_savefile.header = new_savefile.header

    # And we dump the new ready-to-use savefile
    old_savefile.dump("C://SavefileDone.sav")


if __name__ == "__main__":
    main()
