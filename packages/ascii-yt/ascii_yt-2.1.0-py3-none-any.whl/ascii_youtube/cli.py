import argparse
from . import play

DESC = "ascii-yt - play any youtube video ▶ with ASCII in the terminal."
EPLG = "Project homepage on https://github.com/malkiAbdoo/ascii-yt"

def main():

    # get the arguments
    PARSER = argparse.ArgumentParser(prog="asciivp", description=DESC, epilog=EPLG)
    PARSER.add_argument('file', help="the youtube URL of a video.")
    PARSER.add_argument('-s', '--size', help="Set a size to the video.", type=str)
    PARSER.add_argument('--colors', action="store_true", help="use colors in the video.")
    PARSER.add_argument('-c', '--chars',  default=" .'~;icok0XN",type=str,
            help='characters depending on the grayscale value from black to white (default: "%(default)s")')
    
    ARGS = PARSER.parse_args()

    try: 
        play.play(url=ARGS.file, size=ARGS.size, chars=ARGS.chars, colors=ARGS.colors)
    except KeyboardInterrupt:
	    return

if __name__ == '__main__':
    main()

