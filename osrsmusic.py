from mediawiki import MediaWiki
import yt_dlp
import json
import taglib
import re

wiki = MediaWiki(url='https://oldschool.runescape.wiki/api.php')
wiki.user_agent = 'osrs-music-downloader'

track_names = wiki.categorymembers("Music_tracks", results=3000, subcategories=False )

print(f"Found {len(track_names)} tracks to download...")

# Download the tracks
for track_name in track_names:
    ydl_opts = {"playlist_items":"1", # This *should* download the latest version only
            "outtmpl": f"tracks/{track_name}.%(ext)s"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download( 'https://oldschool.runescape.wiki/w/' + track_name )
        page = wiki.page(track_name, auto_suggest=False)
        wikitext = page.wikitext.split("|")
        composer = "Unknown"
        for item in wikitext:
            match = re.match(r'composer\s*=\s*(.+)', item)
            if(match):
                composer = match.group(1)
        filename = f"tracks/{track_name}.ogg"
        with taglib.File(filename, save_on_exit=True) as song:
            song.tags["ALBUM"] = "Old School Runescape OST"
            song.tags["ARTIST"] = composer
            song.tags["TITLE"] = track_name