# Import StreamController modules
from src.backend.PluginManager.ActionBase import ActionBase
from src.backend.DeckManagement.DeckController import DeckController
from src.backend.PageManagement.Page import Page
from src.backend.PluginManager.PluginBase import PluginBase

# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import pulsectl

class ToggleMute(ActionBase):
    def __init__(self, action_id: str, action_name: str,
                 deck_controller: DeckController, page: Page, coords: str, plugin_base: PluginBase):
        super().__init__(action_id=action_id, action_name=action_name,
            deck_controller=deck_controller, page=page, coords=coords, plugin_base=plugin_base)
        
    def get_mute_state(self) -> bool:
        with pulsectl.Pulse('mute-microphone') as pulse:
            all_muted = True
            all_unmuted = True

            for source in pulse.source_list():
                # Get the mute state of the microphone
                muted = source.mute
                if muted:
                    all_unmuted = False
                else:
                    all_muted = False

            if all_muted:
                return True
            elif all_unmuted:
                return False
            else:
                return None
        
    def set_mute(self, state: bool) -> None:
        with pulsectl.Pulse('mute-microphone') as pulse:
            for source in pulse.source_list():
                pulse.source_mute(source.index, state)
        
    def show_state(self) -> None:
        muted = self.get_mute_state()
        if muted is None:
            self.show_error()
            return
        
        if muted:
            self.set_background_color(color=[255, 0, 0, 255])
            icon_name = "muted.png"
        else:
            self.set_background_color(color=[0, 0, 0, 0])
            icon_name = "unmuted.png"

        icon_path = os.path.join(self.plugin_base.PATH, "assets", icon_name)

        self.set_media(media_path=icon_path, size=0.75)

    def on_tick(self):
        self.show_state()

    def on_ready(self):
        self.show_state()

    def on_key_down(self):
        mute = self.get_mute_state()
        if mute is None:
            mute = False
        
        self.set_mute(not mute)
        self.show_state()