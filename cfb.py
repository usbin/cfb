import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget
import time
import binascii
import json
from pn532pi import Pn532
from pn532pi import Pn532I2c
from module_door import Door
from module_weight import MeasureModule
from ui_manager import UiManager

PN532_I2C = Pn532I2c(1)
nfc = Pn532(PN532_I2C)
g_user_id = ""

DOOR = Door()
MEASURE_MODULE = MeasureModule()

def open_door():
    if DOOR.open():
        print("┌────────────────────────────────────┐")
        print("│            DOOR OPENED!            │")
        print("└────────────────────────────────────┘")
    return True
def close_door():
    if DOOR.close():
        print("┌────────────────────────────────────┐")
        print("│            DOOR CLOSED!            │")
        print("└────────────────────────────────────┘")
    return True
def determine_weight():

    print("┌────────────────────────────────────┐")
    print("│       Determining weight...        │")
    print("└────────────────────────────────────┘")
    weight = MEASURE_MODULE.measure()

    print('''┌────────────────────────────────────┐''')
    print('''│          Weight : %4dg            │'''%weight)
    print('''└────────────────────────────────────┘''')
    return True, weight

def something_wrong():
  print("!Something wrong...!")
  reset()

def done(point):
    global g_user_id
    print('''┌────────────────────────────────────┐''')
    print('''│         Your id: %-10s        │'''%g_user_id)
    print('''│         Your point: +%-5d         │'''%point)
    print('''└────────────────────────────────────┘''')
    reset()

def reset():
   global g_user_id
   close_door()
   g_user_id = ""
   print("!All reseted!")


def loop():
    global g_user_id
    # set shield to inListPassiveTarget
    success = nfc.inListPassiveTarget()

    if (success):
        print("Found something!")
        selectApdu = bytearray([0x00,                                     # CLA
                                0xA4,                                     # INS
                                0x04,                                     # P1
                                0x00,                                     # P2
                                0x05,                                     # Length of AID
                                0xF1, 0x23, 0x45, 0x67, 0x89,            # AID defined on Android App
                                0x00 # Le
                                ])

        success, response = nfc.inDataExchange(selectApdu)
        if (success):
            # 연결 후 데이터 송수신 루프
            # 1. userid 요청
            json_object = {
                "method" : "GET",
                "param" : "user_id"
            }
            json_str = json.dumps(json_object)
            command_get_userid = bytes(json_str, "utf-8")# bytearray(b)
            success, resp = nfc.inDataExchange(command_get_userid)
            str = resp.decode('utf-8')
            print("json: %s"%str)
            try:
                userid_dict: dict = json.loads(str)
                g_user_id = userid_dict.get("param")
                print("user id: %s"%g_user_id)
                success = len(g_user_id) == 8
            except:
                pass

            if(success):
                # 2. 투입구 개방
                if (open_door()):
                    # 버튼 입력 대기
                    input()
                    # 3. 투입구 폐쇄
                    if (close_door()):
                        # 4. 무게 측정
                        success, weight = determine_weight()
                        point = weight*2
                        if(success):
                            # 5. 아이디, 무게 정보 휴대폰으로 전송
                            inner_json_object = {
                                "user_id" : g_user_id,
                                "point" : point
                            }
                            inner_json_str = json.dumps(inner_json_object)
                            json_object = {
                                "method" : "PUT",
                                "param" : inner_json_str
                            }

                            result_str = json.dumps(json_object)
                            print(result_str)
                            command_put_result = bytes(result_str, "utf-8")

                            success, str = nfc.inDataExchange(command_put_result)
                            if(success):
                                # 6. 처음으로
                                done(point)
                                return
                                # if (success):
                                #   print("responseLength: {:d}".format(len(back)))
                                #   print(binascii.hexlify(back))
                                # else:
                                #   print("Broken connection?")

        something_wrong() # 리셋 후 처음으로
        return
    else:
        print("Waiting...")

    time.sleep(1)





def setup():
    print("-------Peer to Peer HCE--------")
    #------------------------------------------------#
    #               NFC 초기화                        #
    #------------------------------------------------#
    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if not versiondata:
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    # Got ok data, print it out!
    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))

    # Set the max number of retry attempts to read from a card
    # This prevents us from waiting forever for a card, which is
    # the default behaviour of the PN532.
    #nfc.setPassiveActivationRetries(0xFF)

    # configure board to read RFID tags
    nfc.SAMConfig()


    #------------------------------------------------#
    #               로드셀 초기화                     #
    #------------------------------------------------#



class Cfb(QWidget):
    com = None
    def __init__(self, com=None):
        super().__init__()
        self.Start()
    def Start(self):
        uiManager = UiManager()
        uiManager.Start()






if __name__ == '__main__':
    setup()
    app = QApplication(sys.argv)
    Cfb()
    sys.exit(app.exec_())
    GPIO.cleanup()