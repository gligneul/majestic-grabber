# majestic-grabber

Grabs the Majestic Casual library from Youtube as mp3 files.
The program organizes the music files into albums for each month given the date that the music was published in Majestic Casual.
This program will create the following directory structure:

```
<path>/<album_prefix> <year>.<month>/<num> <artist> - <track>.mp3
```

## Requirements

- Python >= 3.5
- requirements.txt

## Installing

Download the dependencies with the following command:

```
pip3 install -r requirements.txt
```

## Configuration

You need to create a configuration file called `.majesticgrabber.conf` in your home dir with the following syntax.
This file should contain your Youtube API key and the path where the music files should be saved.
For instance:

```
[library]
path = /Users/gligneul/Music/majestic
album_prefix = Majestic Casual

[youtube]
key = your_youtube_api_key
```

If you need help obtaining a Youtube API key, check out the following link: `https://developers.google.com/youtube/v3/getting-started`.

## Execution

After installing the dependencies and creating the config file, just run the `mg` script:

```
python3 mg
```

Atention: be sure that you have enough space in your hard disk.
