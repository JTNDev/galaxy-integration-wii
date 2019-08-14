import json
import os
import sys
import urllib.parse
import urllib.request

import user_config
from galaxy.api.consts import LocalGameState
from galaxy.api.types import LocalGame


class BackendClient:
    def __init__(self):
        self.paths = []
        self.results = []
        self.roms = []



    def get_games_db(self):
        database_records = self.parse_dbf()

        self.get_rom_names()

        for rom in self.roms:
            for record in database_records:
                if(rom == record[1]):
                    self.results.append(
                        [record[0], record[1]]
                    )

        for x,y in zip(self.paths, self.results):
            x.extend(y)

        return self.paths


    def parse_dbf(self):
        file = open(
            r"%LOCALAPPDATA%\GOG.com\Galaxy\plugins\installed\dolphin_fc3e85e4-c66b-4310-96c0-8f95cc43e546\Index.txt",
            encoding="utf8")

        records = []
        serials = []
        names = []
        for line in file:
            line = line.strip()                      # For each line
            if not line.startswith("TITLES"):        # check if it starts with "Name"
                split_line = line.split(" = ")       # Split the line into "Name" and the name of the game
                if split_line[1] not in names:       # If the name isn't already in the list,
                    names.append(split_line[1])      # add it
                    serials.append(split_line[0])    # Add the serial

        for serial, name in zip(serials, names):
            records.append([serial, name])

        return records

    def get_rom_names(self):
        # Search through directory for Dolphin ROMs
        for root, dirs, files in os.walk(user_config.roms_path):
            for file in files:
               if file.lower().endswith(".iso") or  file.lower().endswith(".ciso") or file.lower().endswith(".gcm") or file.lower().endswith(".gcz") or file.lower().endswith(".wbfs"):
                    self.paths.append([os.path.join(root, file)])
                    self.roms.append(os.path.splitext(os.path.basename(file))[0]) # Split name of file from it's path/extension


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
