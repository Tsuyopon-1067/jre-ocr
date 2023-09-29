import readMovie
import noiseReduction


def main():
    RESOLUTION = 12
    MOVIE_FILE = "movie.mp4"
    clpnt = readMovie.ClipingPoint(32, 2, 128, 149)
    readMovie.read_movie(MOVIE_FILE, RESOLUTION, clpnt)
    noiseReduction.noise_reduction()


if __name__ == "__main__":
    main()
