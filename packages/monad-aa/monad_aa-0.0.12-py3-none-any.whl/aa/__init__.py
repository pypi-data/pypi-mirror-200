from aa.plug_point_config import monad_aa_plug_point_configuration
from plugin.plugin_manager import PluginManager

print("inside __init__py of src.aa")


def setup_core_plugins():
    print(f'setup_core_plugins for monad_aa')
    PluginManager.setup_core_plugins(monad_aa_plug_point_configuration)


setup_core_plugins()
