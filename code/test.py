from machine import Pin
import time

shk_pin = Pin(23, Pin.IN)
shk_pin.irq(trigger=Pin.IRQ_RISING, handler=lambda p: irq_hook(23))

btn_pin = Pin(0, Pin.IN)
btn_pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda p: irq_btn(0))

DIGITS_IN_PHONE_NUMBER = 8

# Initialize
shk_value = shk_pin.value()
hook_count = 0
dialed_number = []

hook_counts = [0] * 10
count_idx = 0

def irq_btn(p):
    reset()

def reset():
    global hook_count, dialed_number
    hook_count = 0
    dialed_number = []


def irq_hook(p):
    global hook_count, shk_value
    if shk_value != shk_pin.value():
        hook_count = hook_count + 1

while True:
    hook_counts[count_idx] = hook_count
    if count_idx > 2 and hook_count != 0:

        # hvis vi ikke har hatt en switch på 3 ganger 100ms så lagrer vi ringt tall
        if hook_counts[count_idx] == hook_counts[count_idx - 1] == hook_counts[count_idx - 2]:
            dialed_number.append(hook_count if hook_count < 10 else 0)
            if len(dialed_number) == 1:
                print("Hook off, ready...")
            else:
                print("Digit: ", dialed_number[-1])
            hook_count = 0

    count_idx = count_idx + 1 if count_idx < 9 else 0
    time.sleep_ms(100)

    if len(dialed_number) == DIGITS_IN_PHONE_NUMBER + 1:
        print("Calling subscriber : ", ''.join(map(str, dialed_number[1:])))
        dialed_number = []






