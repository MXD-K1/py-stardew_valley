from enum import Enum, auto

import pygame


class Action(Enum):
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    USE_TOOL = auto()
    SWITCH_TOOL = auto()
    USE_SEED = auto()
    SWITCH_SEED = auto()
    INTERACT = auto()
    INVENTORY_LEFT = auto()
    INVENTORY_RIGHT = auto()
    INVENTORY_SELECT = auto()
    MENU_UP = auto()
    MENU_DOWN = auto()
    MENU_CONFIRM = auto()
    MENU_BACK = auto()


KEY_BINDINGS: dict[Action, int] = {
    Action.MOVE_UP: pygame.K_UP,
    Action.MOVE_DOWN: pygame.K_DOWN,
    Action.MOVE_LEFT: pygame.K_LEFT,
    Action.MOVE_RIGHT: pygame.K_RIGHT,
    Action.USE_TOOL: pygame.K_SPACE,
    Action.SWITCH_TOOL: pygame.K_q,
    Action.USE_SEED: pygame.K_LCTRL,  # Left CTRL
    Action.SWITCH_SEED: pygame.K_e,
    Action.INTERACT: pygame.K_RETURN,  # Enter Key
    Action.INVENTORY_LEFT: pygame.K_a,
    Action.INVENTORY_RIGHT: pygame.K_d,
    Action.INVENTORY_SELECT: pygame.K_RETURN,
    Action.MENU_UP: pygame.K_UP,
    Action.MENU_DOWN: pygame.K_DOWN,
    Action.MENU_CONFIRM: pygame.K_SPACE,
    Action.MENU_BACK: pygame.K_ESCAPE,
}


__all__ = ["Action", "KEY_BINDINGS"]
