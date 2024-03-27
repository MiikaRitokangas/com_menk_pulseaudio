# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.ToggleMute.ToggleMute import ToggleMute

class MicMutePlugin(PluginBase):
    def __init__(self):
        super().__init__()

        self.lm = self.locale_manager

        ## Register actions
        self.toggle_mute_holder = ActionHolder(
            plugin_base = self,
            action_base = ToggleMute,
            action_id = "dev_core447_MicMute::ToggleMute", # Change this to your own plugin id
            action_name = self.lm.get("actions.toggle-mute.name"),
        )
        self.add_action_holder(self.toggle_mute_holder)

        # Register plugin
        self.register(
            plugin_name = self.lm.get("plugin.name"),
            github_repo = "https://github.com/StreamController/MicMute",
            plugin_version = "1.0.0",
            app_version = "1.2.0-alpha"
        )