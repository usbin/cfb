import time
import binascii
import json
from pn532pi import Pn532
from pn532pi import Pn532Hsu
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi

# Set the desired interface to True
SPI = False
I2C = True
HSU = False

if SPI:
    PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
    nfc = Pn532(PN532_SPI)
# When the number after #elif set as 1, it will be switch to HSU Mode
elif HSU:
    PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
    nfc = Pn532(PN532_HSU)

# When the number after #if & #elif set as 0, it will be switch to I2C Mode
elif I2C:
    PN532_I2C = Pn532I2c(1)
    nfc = Pn532(PN532_I2C)

g_user_id = ""
g_door_opened = False

def open_door():
   global g_door_opened
   print("┌────────────────────────────────────┐")
   print("│            DOOR OPENED!            │")
   print("└────────────────────────────────────┘")
   g_door_opened = True
   return True
def close_door():
   global g_door_opened
   if g_door_opened:
    print("┌────────────────────────────────────┐")
    print("│            DOOR CLOSED!            │")
    print("└────────────────────────────────────┘")
    g_door_opened = False
   return True
def determine_weight():
    print("┌────────────────────────────────────┐")
    print("│       Determining weight...        │")
    print("└────────────────────────────────────┘")
    time.sleep(1)
    weight = 230.0

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
  global g_user_id, g_determined_weight, g_door_opened
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
      command_get_userid = bytes("{\"method\":\"GET\", \"param\":\"user_id\"}", "utf-8")# bytearray(b)
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
            if(success):
              # 5. 아이디, 무게 정보 휴대폰으로 전송
              command_get_userid = bytes(
              '''{
                "method" : "PUT",
                "param" : {
                  "user_id" : {g_user_id},
                  "weight" : {weight}
                }
              }
              ''', "utf-8")
              success, str = nfc.inDataExchange(command_get_userid)
              if(success):
                # 6. 처음으로
                point = weight*2
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







if __name__ == '__main__':
    setup()
    while True:
      loop()