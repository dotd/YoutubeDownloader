# LLMVideoProcessor

## FFMPEG useful lines
```
# Put subtitles in movie
ffmpeg -i Coratiba.mp4 -vf subtitles=Coratiba.srt Coritiba2.mp4

# Transform to gif
ffmpeg -i spring_insertion.mp4 spring_insertion.gif

# Take part of the movie
ffmpeg -ss 00:29 -i data/denso.mp4  -t 2.8 -c copy ricklis1.mp4

# Take part of the video and transform it to gif
ffmpeg -ss 00:29 -i data/denso.mp4  -t 2.8 -c copy ricklis1.gif
```


## Links to Industrial videos
https://www.youtube.com/watch?app=desktop&v=m27oD1wfQ0Y
