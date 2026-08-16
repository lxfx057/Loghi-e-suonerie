# Jumbo Tone 2000

Static retro 90s/2000s ringtone selector for GitHub + Vercel.

## Add audio files

Put legally obtained MP3 files in `audio/` using these exact names:

- `crazy-frog.mp3`
- `topolona.mp3`
- `dragostea-din-tei.mp3`
- `ketchup-song.mp3`
- `super-mario-theme.mp3`
- `nokia-3310.mp3`
- `motorola-hello-moto.mp3`

The browser opens the native SMS app with a prefilled message. The user must press Send. This project does not download or extract audio from YouTube. Use files you own or are licensed to distribute; YouTube provides an official embedded-player option instead. [YouTube player docs](https://developers.google.com/youtube/player_parameters)

## Deploy

1. Create a GitHub repository.
2. Upload `index.html`, `style.css`, `app.js`, `README.md`, and the `audio/` folder.
3. Import the repository into Vercel.
4. Deploy as a static site with no build command.
