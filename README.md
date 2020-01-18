# LyricVideos
Automating the creation of Lyric videos on Youtube

### Using the Tool

```{.sourceCode .bash}
$ ./create -f songs.txt
```

or

```{.sourceCode .bash}
$ ./create nine in the afternoon
```

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

We remedy this by downloading multiple lyric videos, and choosing the "best" one based on the number of correct words found within the frames in the video.