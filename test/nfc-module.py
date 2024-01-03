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

                # 4번 block을 "S1B0: [숫자]" 포맷으로 읽음. RFID.card_auth() 호출됨.
                util.read_out(4)

                # 4번 block을 "S1B0: [숫자]" 포맷으로 읽음. RFID.card_auth()는 호출되지 않음.

                util.read_out(5)

                # 6번 block을 "S1B2: [숫자]" 포맷으로 읽음. 새로운 영역을 읽으므로, RFID.card_auth() 호출됨.
                util.read_out(6)

                # 다른 섹터에 대해 다른 키를 가지고 있다면 auth를 A함수로 변경할 수도 있음.
                util.auth(rdr.auth_a, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

                # 섹터2의 1번 블럭 = 9번 블럭을 읽음. 이 블럭에 대해 authorized되지 않았을 때에만 1번 더 auth가 호출됨.
                util.do_auth(util.block_addr(2, 1))

                # 이제 블럭 9에 대해 lower-level 작업을 할 수 있음.
                rdr.write(9, [0x01, 0x23, 0x45, 0x67, 0x89, 0x98, 0x76, 0x54, 0x32, 0x10, 0x69, 0x27, 0x46, 0x66, 0x66, 0x64])

                # 이 메소드로 바이트를 쓸 수 있음. None은 '이 바이트는 변경하지 마시오'라는 뜻임.
                # 이미 블럭 9에 대해 auth를 호출했으므로 authorization은 일어나지 않을 것임에 유의.
                util.rewrite(9, [None, None, 0xAB, 0xCD, 0xEF])

                # S2B1: [0x01, 0x23, 0xAB, 0xCD, 0xEF, 0x98, 0x76......] 을 write할 것임. 세번째, 네번째, 다섯번째 바이트를 재작성하기 때문.
                util.read_out(9)

                # 태그의 내용을 확인
                util.dump()

                # 작업을 종료했다면 deauth() 호출해야함.
                util.deauth()



GetInput()