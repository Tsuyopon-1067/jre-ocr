import readMovie
import noiseReduction
import sys


def main():
    argv = sys.argv
    RESOLUTION = 12
    clpnt = readMovie.ClipingPoint(32, 2, 128, 149)
    MOVIE_FILE = "movie.mp4"
    if len(argv) == 7:
        MOVIE_FILE = argv[1]
        RESOLUTION = int(argv[2])
        x1 = int(argv[3])
        y1 = int(argv[4])
        x2 = int(argv[5])
        y2 = int(argv[6])
        clpnt = readMovie.ClipingPoint(x1, y1, x2, y2)
    if len(argv) == 3:
        MOVIE_FILE = argv[1]
        RESOLUTION = int(argv[2])
    if len(argv) == 2:
        MOVIE_FILE = argv[1]

    readMovie.read_movie(MOVIE_FILE, RESOLUTION, clpnt)
    noiseReduction.noise_reduction()


if __name__ == "__main__":
    main()
