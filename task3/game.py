from dataclasses import dataclass
from typing import List, Dict, Type, Callable, Any

# --- 1. INFRASTRUCTURE (THE BUS) ---
# --- do not modify ---

class MessageBus:
    def __init__(self, handlers: Dict[Type, List[Callable]]):
        self.handlers = handlers
        self.queue: List[Any] = []

    def handle(self, message: Any):
        self.queue.append(message)
        
        while self.queue:
            current_msg = self.queue.pop(0)
            msg_type = type(current_msg)
            
            if msg_type in self.handlers:
                for handler in self.handlers[msg_type]:
                    handler(current_msg, self)  # Przekazujemy 'bus' do handlera
            else:
                print(f"[BUS] No handler for {msg_type.__name__}")

# --- 2. DOMAIN MESSAGES ---
# --- do not modify ---

@dataclass
class EnemyKilled:
    enemy_name: str
    xp_reward: int

@dataclass
class LevelUp:
    new_level: int

# --- 3. GAME STATE ---

class PlayerState:
    def __init__(self):
        self.xp = 0
        self.level = 1
        self.health = 100
        self.max_health = 100

player = PlayerState()

# --- 4. SYSTEM LOGIC (HANDLERS) ---
# --- do not modify ---

def play_sound_handler(event: Any, bus: MessageBus):
    """Prosty handler 'efektów ubocznych'."""
    if isinstance(event, EnemyKilled):
        print(f"🔊 [AUDIO] Playing 'victory.mp3' for killing {event.enemy_name}")
    elif isinstance(event, LevelUp):
        print("🔊 [AUDIO] Playing 'level_up_fanfare.wav'!!!")

# --- to be modified: ---

# ZADANIE 1: Zaimplementuj handler przyznawania doświadczenia.
# Logika:
# 1. Dodaj xp z eventu do gracza (player.xp).
# 2. Wyświetl komunikat.
# 3. Sprawdź, czy player.xp >= 100.
# 4. JEŚLI TAK:
#    - Zwiększ player.level o 1.
#    - Wyzeruj xp (lub odejmij 100).
#    - KLUCZOWE: Opublikuj nowe zdarzenie LevelUp na szynie (bus.handle(...)).
def grant_xp_handler(event: EnemyKilled, bus: MessageBus):
    ...

# ZADANIE 2: Zaimplementuj handler leczenia przy awansie.
# Logika: Gdy gracz awansuje, ulecz go do pełna (player.health = player.max_health)
# i wyświetl komunikat "Player fully healed!".
def heal_on_level_up_handler(event: LevelUp, bus: MessageBus):
    ...

# ZADANIE 3: Skonfiguruj Routing.
# Przypisz typy wiadomości do listy funkcji, które mają je obsłużyć.
# Pamiętaj, że jeden event może uruchomić wiele handlerów (np. EnemyKilled -> XP oraz Dźwięk).

HANDLERS = {
    # EnemyKilled: [ ... ],
    # LevelUp: [ ... ]
}

# --- 6. SIMULATION ---
# --- do not modify ---

def main():
    # Setup
    bus = MessageBus(HANDLERS)
    
    print("--- GAME START ---")
    print(f"Stats: LVL {player.level} | XP {player.xp} | HP {player.health}")

    # Scenariusz: Gracz zabija małego potwora (50 XP)
    print("\n>>> Event: Killing Rat (50 XP)")
    bus.handle(EnemyKilled("Rat", 50))
    print(f"Stats: LVL {player.level} | XP {player.xp}")

    # Scenariusz: Gracz jest ranny i zabija dużego potwora (60 XP)
    # To powinno wywołać kaskadę: EnemyKilled -> grant_xp -> (Nowy Event) LevelUp -> heal_on_level_up
    player.health = 10  # Gracz ranny
    print("\n>>> Event: Killing Dragon (60 XP) [Should trigger Level Up!]")
    bus.handle(EnemyKilled("Dragon", 60))
    
    print(f"Stats: LVL {player.level} | XP {player.xp} | HP {player.health}")

if __name__ == "__main__":
    main()