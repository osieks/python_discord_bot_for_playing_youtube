# Discord Music Bot

This is a Discord bot that can join voice channels and play YouTube videos as audio.

## Features

- Join and leave voice channels
- Play YouTube videos as audio
- Pause and resume playback
- Skip to the next song in the queue
- Display the current queue

## Commands

- `!helpme`: Displays a help message with all the commands and their descriptions.
- `!github`: Sends a link to the bot's GitHub repository.
- `!unpause`: Resumes playback if it was paused.
- `!play`: Plays a YouTube video as audio. You can provide a URL directly, or search for a video.
- `!pause`: Pauses the current playback.
- `!skip`: Skips to the next song in the queue.
- `!queue`: Displays the current queue.
- `!join`: Makes the bot join your current voice channel.
- `!leave`: Makes the bot leave the current voice channel.

## Installation

1. Clone this repository
2. Install the required dependencies: `discord.py`, `vlc`, `pytube`, and `youtube_search`
3. Create a `secret_bot_token.py` file with your bot's token
4. Run the bot with `python bot.py`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT
