import asyncio
import subprocess
import sys


import user_config
from backend import BackendClient
from galaxy.api.consts import LicenseType, LocalGameState, Platform
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import Authentication, Game, LicenseInfo, LocalGame
from version import __version__

class DolphinPlugin(Plugin):
    def __init__(self, reader, writer, token):
        super().__init__(Platform.NintendoWii, __version__, reader, writer, token)
        self.backend_client = BackendClient()
        self.games = []
        self.local_games_cache = self.local_games_list()


    async def authenticate(self, stored_credentials=None):
        return self.do_auth()


    async def pass_login_credentials(self, step, credentials, cookies):
        return self.do_auth()


    def do_auth(self):
        user_data = {}
        username = user_config.roms_path
        user_data["username"] = username
        self.store_credentials(user_data)
        return Authentication("Dolphin", user_data["username"])


    async def launch_game(self, game_id):
        emu_path = user_config.emu_path
        for game in self.games:
            if str(game[1]) == game_id:
                subprocess.Popen([emu_path, "-b", "-e", game[0]])
                break
        return

    async def install_game(self, game_id):
        pass

    async def uninstall_game(self, game_id):
        pass


    def local_games_list(self):
        local_games = []
        for game in self.games:
            local_games.append(
                LocalGame(
                    str(game[1]),
                    LocalGameState.Installed
                )
            )
        return local_games


    def tick(self):

        async def update_local_games():
            loop = asyncio.get_running_loop()
            new_local_games_list = await loop.run_in_executor(None, self.local_games_list)
            notify_list = self.backend_client.get_state_changes(self.local_games_cache, new_local_games_list)
            self.local_games_cache = new_local_games_list
            for local_game_notify in notify_list:
                self.update_local_game_status(local_game_notify)

        asyncio.create_task(update_local_games())


    async def get_owned_games(self):
        self.games = self.backend_client.get_games_db()
        owned_games = []

        for game in self.games:
            owned_games.append(
                Game(
                    str(game[1]),
                    game[2],
                    None,
                    LicenseInfo(LicenseType.SinglePurchase, None)
                )
            )

        return owned_games

    async def get_local_games(self):
        return self.local_games_cache

    def shutdown(self):
        pass


def main():
    create_and_run_plugin(DolphinPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()
