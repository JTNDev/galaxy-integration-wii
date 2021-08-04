import os
import user_config
from galaxy.api.consts import LocalGameState
from galaxy.api.types import LocalGame
from xml.etree import ElementTree
from fuzzywuzzy import fuzz

class WiiGame:

    def __init__(self, path, id, name):
        self.path = path
        self.id = id
        self.name = name

class BackendClient:

    def __init__(self):
        pass

    def get_games_db(self):
        games = []
        paths = self._get_rom_paths()
        database_records = self._parse_dbf()

        for p in paths:
            best_record = []
            best_ratio = 0
            file_name = os.path.splitext(os.path.basename(p))[0]
            matched = False
            for record in database_records:
                if user_config.match_by_id and record["id"] in file_name.upper():
                    games.append(WiiGame(p, record["id"], record["name"]))
                    matched = True
                elif user_config.best_match_game_detection:
                    current_ratio = fuzz.token_sort_ratio(file_name, record[
                        "name"])  # Calculate the ratio of the name with the current record
                    if current_ratio > best_ratio:
                        best_ratio = current_ratio
                        best_record = record
                else:
                    # User wants exact match
                    if file_name == record["name"]:
                        games.append(WiiGame(p, record["id"], record["name"]))

            # Save the best record that matched the game
            if user_config.best_match_game_detection and not matched:
                games.append(WiiGame(p, best_record["id"], best_record["name"]))
        return games

    def _parse_dbf(self):
        file = ElementTree.parse(os.path.dirname(os.path.realpath(__file__)) + r'\games.xml')
        games_xml = file.getroot()
        games = games_xml.findall('game')
        records = []
        for game in games:
            game_id = game.find('id').text
            game_platform = game.find('type').text
            locale = game.find('locale')
            game_name = locale.find('title').text
            if game_platform != "GameCube":
                records.append({"id": game_id, "name": game_name})
        return records

    def _get_rom_paths(self):
        paths = []
        # Search through directory for Dolphin ROMs
        for root, _, files in os.walk(user_config.roms_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in (".iso", ".ciso", ".gcm", ".gcz", ".wad", ".wbfs", ".wia", ".rvz")):
                    paths.append(os.path.join(root, file))
        return paths

    def get_state_changes(self, old_list, new_list):
        old_dict = {x.game_id: x.local_game_state for x in old_list}
        new_dict = {x.game_id: x.local_game_state for x in new_list}
        result = []
        # removed games
        result.extend(LocalGame(id, LocalGameState.None_) for id in old_dict.keys() - new_dict.keys())
        # added games
        result.extend(local_game for local_game in new_list if local_game.game_id in new_dict.keys() - old_dict.keys())
        # state changed
        result.extend(LocalGame(id, new_dict[id]) for id in new_dict.keys() & old_dict.keys() if new_dict[id] != old_dict[id])
        return result

if __name__ == "__main__":
    bc = BackendClient()
    for game in bc.get_games_db():
        print(game.id)
        print(game.name)
        print(game.path)
        print()
