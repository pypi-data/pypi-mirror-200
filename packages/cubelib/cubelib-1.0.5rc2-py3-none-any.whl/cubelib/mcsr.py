try:
    from PIL import Image # icon loading and transforming
    from base64 import b64decode # icon decoding
    from io import BytesIO # in-memory png streaming    
    ICONLESS = False
except ImportError:
    ICONLESS = True

import os
import itertools
import re

from cubelib.aio import AsyncStatusRetriever, ServerError
import asyncio
import cubelib
import argparse

from cubelib.iautil import addr_parser

os.system("color")

SEMVER = "0.3.0"

NO_CONN_ICON = "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"
NO_ICON_ICON = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAAAAAAAAQCEeRdzAAAPfElEQVR4nO3adbNdxRIF8P1FIEhwCO6WBAvuGiDBQhLcgru7u0tRUJDg7u4uX2de/bpqnZp36lJEXnGrXvij7549e6TX6p6enjl3eOmll9rKLMNkKzDZ8i8Bk63AZMu/BEy2ApMt/xLw8ssvt5VVVjoCAF6yZEk9X3nllfbqq6+uPAQA/cYbb7SPP/64ffnll+27775rv/zyy8pDAMt/+OGH7c8//yz5448/SlYqAt5///0CHQJ+//33NlgL/4/Su37K7777bvv+++/bN9980z7//PNaDv8zAqyviOAymeDNTw+AP/roowIL9A8//NDee++9+vbmm2+WrDABr7/+eskdd9zR7r777nbfffe1F198ser+aYsDBOiPP/5YAe7XX39tv/32W7l6nl999VW1e+utt0pWiIDXXnutPfbYY+2MM85oO++8c9txxx3red5557XnnnvuH/UEBAAEdABH1CGE8AKescIEAM/SRxxxRNt8883bVltt1bbffvvRc/78+dWGJ3j+EyQA9PPPP7effvqptrmvv/663P+TTz5pH3zwQQF/55132ttvvz2SgZWWRwB75pln2t57710EbL311gXcc7vttmtHHXVUe/TRR4ukF154oUgYH2OiuonaLE27tAWyB4qUHrD6noQVIuDZZ59t++yzT9tss83alltu2bbZZpsRETNmzGjTp09v++23Xzv33HNHfbL+PHsPGQeSQBVvWxbdeqA9EZnX2Jl3hQh4/vnn25FHHtk22mijkUybNq0IINtuu23bYostqo19ePHixe2ee+5p1113Xbvgggtqmdx44421VRkvihn38ssvb6effnqbM2dOO+uss8qbElj/zjNC4ETkjstyE5CJgFq4cGF5wIYbbliAWV5A5BHelU866aQCbMnstddeJbvvvnvbf//922mnnVaE3HzzzaX0rbfeWsGUZxlj5syZ7eKLL651bE1LZb/99tsSFg4pyyMr5AEIYFlyySWXtE033bSWBMAIERDFh5AS8JbFwQcfXOBnzZrVDjnkkPISceOcc85pp5xySgHXP0F11113bVdddVUFOVGdKNvWrPnlJiCutKwCNPc9/vjjywPmzZtXQFnVM8th4403LjCI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"

def rgb_to_ascii(binary_pixels: bytes, width: int, placeholder: str = "m"):
    pixels = [binary_pixels[i:i + 3] for i in range(0, len(binary_pixels), 3)]

    width_control = 0
    out = ""

    for pix in pixels:
        width_control += 1

        out += f"\x1b[38;2;{';'.join([str(i) for i in pix])}m{placeholder}"

        if width_control == width:
            width_control = 0
            out += "\n"

    return out

def horizontal_matrix_multiply(m1: str, m2: str, padding: int = 0, i: str = ""):
    out = ""
    for f, s in itertools.zip_longest(m1.split("\n"), m2.split("\n")):
        out += f"{f}{i}{padding * ' '}{s if s else ''}\n"        
    return out[:-2]

MCCOLORMAP = {
    "0": (0, 0, 0),
    #"1": (0, 0, 170), worst visibility in black terminal
    "1": (104, 109, 224),
    "2": (0, 170, 0),
    "3": (0, 170, 170),
    "4": (170, 0, 0),
    "5": (170, 0, 170),
    "6": (255, 170, 0),
    "7": (170, 170, 170),
    "8": (85, 85, 85),
    "9": (85, 85, 255),
    "a": (85, 255, 85),
    "b": (85, 255, 255),
    "c": (255, 85, 85),
    "d": (256, 85, 255),
    "e": (255, 255, 85),
    "f": (255, 255, 255),
    "k": "", # dynamic obfuscation
    "l": "", # removing reason: disables coloring at all
    "m": "\033[9m", # seems it's not working
    "n": "\033[4m",
    "o": "\033[3m", # and this one
    "r": "\x1b[0m"
}

MCTCOLOR = {
    "black": "§0",
    "dark_blue": "§1",
    "dark_green": "§2",
    "dark_cyan": "§3",
    "dark_red": "§4",
    "purple": "§5",
    "gold": "§6",
    "gray": "§7",
    "dark_gray": "§8",
    "blue": "§9",
    "green": "§a",
    "aqua": "§b",
    "red": "§c",
    "pink": "§d",
    "yellow": "§e",
    "white": "§f"
}

def minecraft_colorized_text(text: str):    
    matchces = re.findall(f"§[0-z]", text)

    for match in matchces:
        modifier = MCCOLORMAP[match[1]]
        if isinstance(modifier, tuple):
            modifier = f"\x1b[38;2;{';'.join([str(i) for i in modifier])}m"

        text = re.sub(match, modifier, text)
    return text

def minecraft_uncolorize(text: str):    
    matchces = re.findall(f"§[0-z]", text)

    for match in matchces:
        text = re.sub(match, "", text)
    return text

async def main():
    global ICONLESS
    IMGW, IMGH = int(64 / 2), int(64 / 4)

    parser = argparse.ArgumentParser(description=F"Minecraft Server Status Retriever v{SEMVER}")
    parser.add_argument("host", help="Minecraft server addr like mc.hypixel.net:25565 or 127.0.0.1 or [::1], can be with port after `:` or not", metavar="host")
    parser.add_argument("--proto", type=int, help="Protocol version field value sent in Handshake packet", default="-1", metavar="47")
    parser.add_argument("--high-res", action="store_true", help="If passed, prints full resolution server icon")
    parser.add_argument("--raw", action="store_true", help="If passed, prints raw server status response excluding the icon")
    parser.add_argument("--iconless", action="store_true", help="If passed, disables server icon printing")
    
    args = parser.parse_args()
    ICONLESS = args.iconless if not ICONLESS else ICONLESS

    try:
        host, port = addr_parser(args.host, 25565)
        status, ping, family = await AsyncStatusRetriever.retrieve(host, port, protocol=args.proto)
        if args.raw:
            tmpcpy = status.copy()
            if "favicon" in tmpcpy:
                del tmpcpy["favicon"] 
            print(tmpcpy); del tmpcpy

        if "favicon" in status:        
            img = Image.open(BytesIO(b64decode(status["favicon"].split("data:image/png;base64,")[1]))) if not ICONLESS else None
        else:
            img = Image.open(BytesIO(b64decode(NO_ICON_ICON))) if not ICONLESS else None
        
        description = status['description']
        if isinstance(description, dict): # if modern description format
            description = description['text'] + ("".join([(MCTCOLOR[i['color']] if 'color' in i else '') + i['text'] for i in description['extra']]) if 'extra' in description else '')

        description = minecraft_colorized_text(description).split("\n")  

        sstatus = f"\x1b[38;2;127;127;127m{ping}ms"
        ver_name = minecraft_colorized_text(status['version']['name'])
        ver_proto = status['version']['protocol']
        players_online = status['players']['online']
        players_max = status['players']['max']
        players = ""
        if 'sample' in status['players']:
            players = status['players']['sample'][:5]
            players = ", ". join([player['name'] for player in players])
            players = minecraft_uncolorize(players)
            players = ("\x1b[38;2;227;227;227m- " + players) if players else ""

    except (TimeoutError, ConnectionError, ServerError) as e:
        img = Image.open(BytesIO(b64decode(NO_CONN_ICON))) if not ICONLESS else None

        sstatus = f"\x1b[38;2;235;77;75m{e}"
        ver_name = "-"
        ver_proto = -1
        players_online = -1
        players_max = -1
        description = [
            "\x1b[38;2;127;127;127mNaN NaN NaN NaN NaN NaN NaN NaN",
            "   \x1b[38;2;127;127;127mNaN NaN NaN NaN NaN NaN NaN NaN"
        ]
        players = ""
        family = -1
       
    text = f"""
    \x1b[38;2;72;52;212mMC:SR v{SEMVER} (cubelib v{cubelib.version}) {'ICONLESS' if ICONLESS else ''}

    \x1b[38;2;223;249;251mHost: {'v4 ' if family == 2 else ('v6 ' if family == 23 else '')}\x1b[38;2;125;252;255m{host}:{port} {sstatus}

    \x1b[38;2;223;249;251mVersion:
        \x1b[38;2;223;249;251mName: {ver_name}
        \x1b[38;2;125;252;255mProtocol: {ver_proto}

    \x1b[38;2;255;255;255mPlayers:
        \x1b[38;2;255;255;205m{players_online} \x1b[38;2;127;127;127m/ \x1b[38;2;255;255;205m{players_max} {players}

    \x1b[38;2;255;255;255mDescription:
        > {description[0]}
        > {description[1] if len(description) == 2 else ''}
    """

    if args.high_res:
        IMGW, IMGH = int(128), int(64)
    
    if not ICONLESS:
        img = img.resize((IMGW, IMGH))
        img = img.convert("RGB")
        img = rgb_to_ascii(img.tobytes(), img.width)
    else:    
        img = rgb_to_ascii(os.urandom(3*32*16), 32)

    banner = horizontal_matrix_multiply(img, text, i="\x1b[0m")    

    print(banner + "\x1b[0m")

def entry_point():
    asyncio.run(main())

if __name__ == "__main__":
    entry_point()
