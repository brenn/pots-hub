import time

from machine import Pin, PWM

# Switch hook.  High if off hook, Low if on hook
SHK_PIN_NO = 23
# Ring mode. Set to High when ringing, Low elsewise
RM_PIN_NO = 22
# Forward/Revers. PWM with 25Hz to create high voltage ring signal on RING/TIP line
FR_PIN_NO = 21


shk_pin = Pin(SHK_PIN_NO, Pin.IN)
rm_pin = Pin(RM_PIN_NO, Pin.OUT)
btn_pin = Pin(0, Pin.IN)
fr_pwm = None

shk_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=lambda p: irq_hook(SHK_PIN_NO))

hook_is_off = shk_pin.value()

def irq_hook(pin):
    global hook_is_off
    hook_is_off = shk_pin.value()

def button_pressed():
    return btn_pin.value() == 0

def ring(secs=2):
    global fr_pwm

    if hook_is_off:
        print("Cannot ring when off hook")
        return

    fr_pwm = PWM(Pin(FR_PIN_NO), freq=25)
    # check for irq every 0.1 sec
    for i in range(secs * 10):
        time.sleep(0.1)
        if hook_is_off:
            fr_pwm.deinit()
            print("Ringing aborted")
            break
    fr_pwm.deinit()

while True:
    time.sleep(1)
    if button_pressed():
        print("Button pressed")
        ring()
    print("Hook is off" if hook_is_off else "Hook is on")

