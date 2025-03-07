from machine import Pin, PWM, Timer
import time

class Sentral:
    def __init__(self, SHK_PIN_NO=23, RM_PIN_NO=22, FR_PIN_NO=21) -> None:

        self.hook_count = 0
        self.shk_pin = Pin(SHK_PIN_NO, Pin.IN)
#        self.shk_pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda p: self.irq_hook(SHK_PIN_NO))
        self.shk_pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda p: self.irq_hook_tmp(SHK_PIN_NO))
        self.btn_pin = Pin(0, Pin.IN)
        self.btn_pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda p: self.irq_btn(0))

        self.rm_pin = Pin(RM_PIN_NO, Pin.OUT)
        self.fr_pin_no = FR_PIN_NO

        self.shk_value = self.shk_pin.value()
        self.button_was_pressed = False

        self.last_tick = 0
        self.hooks = [] * 10

#        self.tim = Timer(-1)
#        self.tim.init(mode=Timer.PERIODIC, period=2000, callback=lambda t: self.reset_hook_count())

    def irq_hook(self, pin):
        pass

    def irq_btn(self, pin):
        self.button_was_pressed = True

    def set_ring_mode(self, mode):
        self.rm_pin.value(mode)

    def hook_is_off(self):
        return True if self.shk_value else False

    def incoming_call(self):
        # simulert ved knappetrykk for øyeblikket
        return self.button_was_pressed

    def reset_hooks(self):
        self.hooks = []

    def ring(self, secs=2):
        if self.hook_is_off():
            print("Kan ikke ringe når røret er av")
            return

        self.button_was_pressed = False
        self.set_ring_mode(True)
        fr_pwm = PWM(Pin(self.fr_pin_no), freq=25)
        for i in range(secs * 10):
            time.sleep(0.1)
            if self.hook_is_off():
                fr_pwm.deinit()
                self.set_ring_mode(False)
                print("Rør er av, ringing avbrutt")
                break

        fr_pwm.deinit()
