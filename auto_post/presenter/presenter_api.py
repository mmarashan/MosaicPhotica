from abc import ABC
from enum import Enum

from auto_post.view.view_api import View


class State(Enum):
    IDLE = 0
    START_NEW_TASK = 1
    LOAD_GOAL_PROFILE = 2
    MAKE_MOSAICS = 3
    CHOOSE_RESULTS = 4
    POST_MOSAIC = 5


class Presenter(ABC):

    def inject(self, view: View):
        pass

    def set_state_change_listener(self, listener):
        pass

    def on_click_start(self):
        pass

    def on_choose_goal_profile(self, profile_id: str):
        pass


