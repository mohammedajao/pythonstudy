import time
from pyducks import PyducksStore, ActionableStateItem, createReducer
from dataclasses import dataclass, field
from typing import List

# --- State Definitions ---
@dataclass
class CharacterSlice:
    hp: int = 100
    attack: int = 10

@dataclass
class EnemySlice:
    hp: int = 100
    attack: int = 8

@dataclass
class GameSlice:
    turn: str = "player"
    game_over: bool = False

@dataclass
class OverarchingState:
    player: CharacterSlice
    enemy: EnemySlice
    game: GameSlice
    logs: List[str] = field(default_factory=list)

# --- Action Definitions ---
class PlayerAttack(ActionableStateItem):
    def __init__(self):
        super().__init__("PLAYER_ATTACK")

class EnemyAttack(ActionableStateItem):
    def __init__(self):
        super().__init__("ENEMY_ATTACK")

class EndTurn(ActionableStateItem):
    def __init__(self):
        super().__init__("END_TURN")

class CheckGameOver(ActionableStateItem):
    def __init__(self):
        super().__init__("CHECK_GAME_OVER")

class LogAction(ActionableStateItem):
    def __init__(self, message: str):
        super().__init__("LOG", message)

# --- Reducer Configuration ---
def game_reducer_builder(builder):
    # Player Attack: Reduce enemy HP and log
    def player_attack_reducer(state, draft, action):
        draft.enemy.hp = state.enemy.hp - 8
        draft.logs.append(f"Player attacked {state.enemy.__class__.__name__} (Enemy HP: {state.enemy.hp})")

    builder.add_case(
        ActionableStateItem("PLAYER_ATTACK"),
        player_attack_reducer
    )
    
    # Enemy Attack: Reduce player HP and log
    builder.add_case(
        ActionableStateItem("ENEMY_ATTACK"),
        lambda state, draft, action: (
            setattr(draft.player, 'hp', max(0, state.player.hp - 8)),
            draft.logs.append(f"Enemy attacked (Player HP: {state.player.hp})")
        )
    )
    
    # End Turn: Switch turns and log
    builder.add_case(
        ActionableStateItem("END_TURN"),
        lambda state, draft, action: (
            setattr(draft.game, 'turn', "enemy" if state.game.turn == "player" else "player"),
            draft.logs.append("Turn ended")
        )
    )
    
    # Check Game Over: Update game state and log
    builder.add_case(
        ActionableStateItem("CHECK_GAME_OVER"),
        lambda state, draft, action: (
            setattr(draft.game, 'game_over', state.player.hp <= 0 or state.enemy.hp <= 0),
            draft.logs.append("Checked game over")
        )
    )
    
    # Log Action: Append custom message
    builder.add_case(
        ActionableStateItem("LOG"),
        lambda state, draft, action: draft.logs.append(action.payload)
    )

# Initialize store with createReducer
initial_state = OverarchingState(
    CharacterSlice(),
    EnemySlice(),
    GameSlice(),
    logs=[]
)
game_reducer = createReducer(initial_state, game_reducer_builder)
store = PyducksStore(game_reducer, initial_state)

# --- Simulation ---
def turn_based_simulation():
    def listener(state_change):
        old_state, new_state = state_change
        if old_state.game.turn != new_state.game.turn:
            print(f"Turn: {new_state.game.turn}, Player HP: {new_state.player.hp}, Enemy HP: {new_state.enemy.hp}")
        if new_state.game.game_over and old_state.game.game_over != new_state.game.game_over:
            print("\nGame Over!")
            if new_state.player.hp <= 0:
                print("Enemy Wins!")
            else:
                print("Player Wins!")
            # Print action log after game ends
            # print("\nAction Log:")
            # for entry in new_state.logs:
            #     print(f"- {entry}")
    
    unsubscribe = store.subscribe(listener)
    
    # Game loop
    while not store.get_state().game.game_over:
        current_turn = store.get_state().game.turn
        if current_turn == "player":
            store.dispatch(PlayerAttack())
        else:
            store.dispatch(EnemyAttack())
        store.dispatch(EndTurn())
        store.dispatch(CheckGameOver())
        # store.dispatch(LogAction(f"{current_turn} executed actions"))
        # time.sleep(1)
    
    unsubscribe()

    print("\nAction Log:")
    for log in store.get_state().logs:
        print(log)

# Run simulation
turn_based_simulation()