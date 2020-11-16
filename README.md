# Nintendo Wii GOG Galaxy 2.0 Integration

A GOG Galaxy 2.0 integration with the Dolphin emulator.
This is a fork of AHCoder (on GitHub)'s PCSX2 GOG Galaxy Plugin edited for support with Dolphin! 
If you want to download it go here:


Thank you AHCoder for the original program, and the Index file 
which gives the game database is from GameTDB.

# Setup:
Just download the file here and extract the ZIP into: ```C:\Users\<username>\AppData\Local\GOG.com\Galaxy\plugins\installed```

Edit user_config.py with your ROMs and Dolphin location.

Go into GOG Galaxy 2.0, click on integrations and connect the one with "Nintendo Wii" and you're done.

# Limitations:

All ROMs must be in the same folder. Subfolders are allowed.

If you have the game's ID in the filename you can enable ```match_by_id```. Using only this option means that any file without ID falls back to exact match between filename and game name in GamesList.txt.

Enable ```best_match_game_detection``` to allow the best match algorithm. It can work as a fallback with ```match_by_id```.

If you enable none of the above options the name of the ROM must be equivalent to its counterpart in GamesList.txt. You can look up the name in GamesList.txt and edit your file accordingly.

Supported file extensions are ISO, CISO, GCM, GCZ, WAD, WBFS, WIA, and RVZ.
