from abc import ABC, abstractmethod

# --- CZĘŚĆ 1: Wzorzec Observer (Interfejsy) ---

class Subscriber(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Publisher(ABC):
    def __init__(self):
        self._subscribers = []

    def attach(self, subscriber: Subscriber):
        self._subscribers.append(subscriber)

    def notify(self, message: str):
        for subscriber in self._subscribers:
            subscriber.update(message)


# --- CZĘŚĆ 2: Wzorzec Mediator (Interfejs) ---

class Mediator(ABC):
    @abstractmethod
    def notify_event(self, sender: object, event: str):
        pass


# --- CZĘŚĆ 3: Komponenty Systemu ---

class SmartDevice(Subscriber):
    """Bazowa klasa dla urządzeń, będąca jednocześnie subskrybentem i współpracownikiem Mediatora."""
    def __init__(self, name: str, mediator: Mediator = None):
        self.name = name
        self.mediator = mediator

    def send_to_mediator(self, event: str):
        if self.mediator:
            self.mediator.notify_event(self, event)

    def update(self, message: str):
        print(f"[{self.name}] Otrzymano powiadomienie z systemu: {message}")


class MotionSensor(SmartDevice):
    def detect_motion(self):
        print(f"[{self.name}] Wykryto ruch!")
        # TODO: Poinformuj mediatora o zdarzeniu "motion_detected"
        pass


class Light(SmartDevice):
    def turn_on(self):
        print(f"[{self.name}] Światło włączone.")

    def turn_off(self):
        print(f"[{self.name}] Światło wyłączone.")


class Alarm(SmartDevice):
    def activate(self):
        print(f"[{self.name}] ALARM URUCHOMIONY!")


# --- CZĘŚĆ 4: Implementacja Mediatora (Logika Biznesowa) ---

class HomeAutomationHub(Mediator, Publisher):
    """
    Centrum sterowania pełniące rolę Mediatora (koordynacja urządzeń) 
    oraz Publishera (wysyłanie ogólnych powiadomień do wszystkich).
    """
    def __init__(self):
        super().__init__()
        self.lights = []
        self.sensor = None
        self.alarm = None

    def set_devices(self, lights: list[Light], sensor: MotionSensor, alarm: Alarm):
        self.lights = lights
        self.sensor = sensor
        self.alarm = alarm

    def notify_event(self, sender: object, event: str):
        # TODO: Zaimplementuj logikę reakcji na zdarzenia:
        # 1. Jeśli sender to MotionSensor i event to "motion_detected":
        #    - Włącz światło (light.turn_on)
        #    - Wyślij powiadomienie do wszystkich subskrybentów (self.notify) o treści "Ruch w salonie!"
        # 2. Jeśli sender to Alarm i event to "intruder_alert":
        #    - Włącz wszystkie światła
        #    - Wyślij powiadomienie "ALARM: Intruz!"
        pass


# --- CZĘŚĆ 5: Uruchomienie Systemu (Skrypt testowy) ---

if __name__ == "__main__":
    hub = HomeAutomationHub()

    # Inicjalizacja urządzeń
    salon_light = Light("Światło Salon", hub)
    kuchnia_light = Light("Światło Kuchnia", hub)
    sensor = MotionSensor("Czujnik Ruchu", hub)
    alarm_sys = Alarm("System Alarmowy", hub)

    hub.set_devices([salon_light, kuchnia_light], sensor, alarm_sys)

    # Rejestracja urządzeń w systemie powiadomień (Observer)
    # TODO: Dodaj salon_light, kuchnia_light i alarm_sys do subskrybentów hub-a
    
    print("--- Test 1: Wykrycie ruchu ---")
    # TODO: Wywołaj metodę detect_motion na czujniku
    
    print("\n--- Test 2: Globalny komunikat ---")
    hub.notify("System przechodzi w tryb nocny o 22:00.")