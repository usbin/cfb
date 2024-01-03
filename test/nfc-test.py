from pirc522 import RFID, RFIDUtil
import signal
import time

rdr = RFID()
util = rdr.util()
# Set util debug to true - it will print what's going on
util.debug = True

def GetInput() :
    while True:
        # Wait for tag

        rdr.wait_for_tag()
        # Request tag
        (error, data) = rdr.request()
        if not error:
            print("\nDetected")
            print(data)
            (error, uid) = rdr.anticoll()
            if not error:
                # Print UID
                print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

                # 태그를 선택함. 내부적으로 RFID.select_tag(uid)를 호출함.

                util.set_tag([0xF2, 0x22, 0x22, 0x22])

                # Key B로 authorization을 저장. auth 아직 호출되지 않음.
                util.auth(rdr.auth_b, [0xF2, 0x22, 0x22, 0x22])

                rdr.write(9, [0x01, 0x23, 0x45, 0x67, 0x89, 0x98, 0x76, 0x54, 0x32, 0x10, 0x69, 0x27, 0x46, 0x66, 0x66, 0x64])

                util.rewrite(9, [None, None, 0xAB, 0xCD, 0xEF])

                util.read_out(9)

                util.dump()

                util.deauth()



GetInput()