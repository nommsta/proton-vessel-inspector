import importlib.machinery
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


loader = importlib.machinery.SourceFileLoader("inspector", "proton-vessel-inspector")
spec = importlib.util.spec_from_loader(loader.name, loader)
inspector = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = inspector
loader.exec_module(inspector)


class InspectorTests(unittest.TestCase):
    def test_app_id_prefers_steam_game_id(self):
        self.assertEqual(inspector.app_id_for({"SteamGameId": "292000", "SteamAppId": "0"}), "292000")

    def test_expands_pressure_vessel_paths(self):
        environment = {"XDG_RUNTIME_DIR": "/run/user/1000"}
        self.assertEqual(
            inspector.expand_mount_list("$XDG_RUNTIME_DIR/discord-ipc-0:/tmp/tool", environment),
            ["/run/user/1000/discord-ipc-0", "/tmp/tool"],
        )

    def test_finds_deepest_containing_mount(self):
        mounts = [("/", "rootfs"), ("/run/user/1000", "tmpfs"), ("/run/user/1000/discord-ipc-0", "socket")]
        self.assertEqual(inspector.containing_mount("/run/user/1000/discord-ipc-0", mounts), "/run/user/1000/discord-ipc-0")

    def test_extracts_game_name_from_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "appmanifest_292000.acf"
            manifest.write_text('"appid" "292000"\n"name" "No More Room in Hell 2"\n')
            self.assertEqual(inspector.steam_game_names([Path(directory)]), {"292000": "No More Room in Hell 2"})


if __name__ == "__main__":
    unittest.main()
