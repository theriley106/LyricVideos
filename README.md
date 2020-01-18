# LyricVideos
Generating Lyric Videos

### Using the Tool

```{.sourceCode .bash}
$ ./create -f songs.txt
```

or

```{.sourceCode .bash}
$ ./create nine in the afternoon
```

## Improving Video Quality

This program does not work as well with Lyric videos that use transitions between words.  For example:

<p align="center">
<img src="/static/example.gif"/>
</p>

Alternatively, videos with little/no transition between lyrics work really well.  For example:

<p align="center">
<img src="/static/goodExample.gif"/>
</p>

We remedy this by downloading multiple lyric videos, and choosing the "best" one based on the number of correct words found within the frames in the video.