## How does this work

Youtube videos are pulled using `youtube-dl`, and OCR is done on each *unique* frame in the video.  This gives us a general idea of the song lyrics with a timestamp range that matches the audio in the song.

We can then generate a new lyric video by recreating each frame and mending the frames together using `ffmpeg`.  The transitions and audio can then be added, and the final result is a video that's indistinguishable from other lyric videos on Youtube that follow the same style.

## Using the Tool

```{.sourceCode .bash}
$ ./create -f songs.txt
```

or

```{.sourceCode .bash}
$ ./create nine in the afternoon
```

**Note: This program is not intended to facilitate copyright infringement by any means.  Youtube is extremely good at removing copyrighted material from their site -- please only use this with [Royalty Free music](https://en.wikipedia.org/wiki/Royalty-free) or music that you have permission to upload to Youtube.**


## Video Quality

### OCR 

Everything works by default with no external APIs, but I've found that using the [AWS Rekognition API](https://aws.amazon.com/rekognition/) results in significantly higher quality videos compared to ones that only use tesseract on your local machine.

Tesseract is still the default with this program, but you can use AWS Rekognition by running `./setupAWS`.

```bash
$ ./setupAWS
What is your AWS Access Token?
my_fake_access_token

What is your AWS Secret key?
my_fake_secret_key

AWS Token: my_fake_access_token
AWS Secret Key: my_fake_secret_key

Does this look correct? (y/n)
AWS Rekognition has been setup
```

### Program Limitations

This program does not work as well with Lyric videos that use transitions between words.  For example:

<p align="center">
<img src="/static/example.gif"/>
</p>

Alternatively, videos with little/no transition between lyrics work really well.  For example:

<p align="center">
<img src="/static/goodExample.gif"/>
</p>

We remedy this by downloading multiple lyric videos, and choosing the "best" one based on the number of unique frames in the video.

The idea is that a lower number of unique frames likely means that the video is *not* using transitions.