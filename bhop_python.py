import time
from threading import Thread

import keyboard
import pymem.process
import requests
from art import tprint

tprint('csgo bhop')
print('[] Load Hopper...')

# Connecting to game
pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
print('[] Connection established')

# Collect Offset's
print('[] receiving Offset\'s...')

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets).json()
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwForceJump = int(response["signatures"]["dwForceJump"])

m_fFlags = int(response["netvars"]["m_fFlags"])


print('[] Loading Hopper...')


# Main function
def Hopper():
    while True:
        if pm.read_int(client + dwLocalPlayer):
            player = pm.read_int(client + dwLocalPlayer)
            force_jump = client + dwForceJump
            on_ground = pm.read_int(player + m_fFlags)

            if keyboard.is_pressed("space"):
                if on_ground == 257:
                    pm.write_int(force_jump, 5)
                    time.sleep(0.17)
                    pm.write_int(force_jump, 4)


Thread(target=Hopper).start()

print('')
print('[] Hopper launched.'
      'GL!')
