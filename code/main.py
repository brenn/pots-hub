import time
from telefon_sentral import Sentral

s = Sentral()

while True:
    if s.incoming_call():
        s.button_was_pressed = False
        for item in s.hooks:
            for key in item:
                print(f"{key} : {item[key]}")
        s.reset_hooks()

    time.sleep(0.2)
