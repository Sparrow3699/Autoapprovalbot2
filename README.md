# Auto Approve Bot

<h2>〽️ How To Deploy? </h2>

Go to repository settings `Secrets and Variables` > `Action`<br>
Fill required secret:
- `HEROKU_API_KEY`
- `HEROKU_APP_NAME`
- `HEROKU_EMAIL`


Go to `Action` and Deploy


## 🏷 Environment Variables

### Go to Heroku setting and fill this variable:
  - `BOT_TOKEN` - Telegram Bot Token (**Required**)
  - `TELEGRAM_API` - Telegram API (**Required**)
  - `TELEGRAM_HASH` - Telegram Hash (**Required**)
  - `OWNER_ID` - Owner ID (**Required**)
  - `DATABASE_URL` - Mongo DB url to collecting all users (**Recomended**)
  - `SUDO` - All sudo user, separated by space `12345 67890 09876 54321` (**Optional**)
  - `CHAT_IDS` - Spesific auto approve chat id, separated by space `-10012345 -10067890 -10009876 -10054321` (**Optional**)
  - `CMD_BROADCAST` - Custom broadcast message command, default to `/bc` (**Optional**)
  - `CMD_LOG` - Custom log command, default to `/log` (**Optional**)
  - `CMD_RESTART` - Custom restart bot command, default to `/restart` (**Optional**)
  - `CMD_START` - Custom start command, default to `/start` (**Optional**)
  - `CMD_USERS` - Custom get users command, default to `/users` (**Optional**)
  - `APPROVE_MESSAGE_TEXT` - Custom text message sending to user when approved, default to `Congratulation, you have been approved to join the channel!` (**Optional**)
  - `UPSTREAM_REPO` - Fill upstream repo url to get update when `/restart` (**Optional**)
  - `UPSTREAM_BRANCH` - Upstream branc repo default to `master` (**Optional**)
  - `UPDATE_EVERYTHING` - Upstream all piython lib when restart (**Optional**)
