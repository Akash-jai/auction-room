# Auction Room

A live, multiplayer, IPL-style player auction. Friends join a room from a link and bid in real time;
any franchise nobody claims is played by an AI with its own strategy.

Unofficial fan project. Uses generic city names, no logos. Player ratings are made-up estimates; all players are real, current and retired IPL players.


## Features
- Room codes and share links, no accounts. The host picks how many teams play (2 = duel, up to 10).
- Real-auction rules: ₹120 cr purse, squads of 18-25, max 8 overseas, bid increments that grow with price,
  marquee set first, then shuffled role-based sets, then an accelerated round for unsold players.
- Server-authoritative: the server owns the clock, bids and rules, so clients cannot cheat.
- AI franchises with personalities: squad-balance needs, scarcity awareness, purse pacing, star chasers, snipers.
  If a human disconnects, their team is played by the AI until they return (same browser).
- Voice chat: built-in WebRTC group voice (open mic up to 6 people, push-to-talk by default from 7). The game socket only relays the handshake. `/ice` serves STUN servers; set TURN_URL, TURN_USER and TURN_PASS on the host to add a relay for strict networks.
- Ending early: there is no host button. Any player can call a vote; a majority of human players ends the auction (25 s to vote, 90 s cooldown after a failed vote).
- Game modes: Match (one XI scores) or Tournament (league + playoffs simulated from full squads, so depth matters). Bidding speed: quick, normal or relaxed.
- Custom players: the host can upload an Excel or CSV file (Name, Rating, Position, Overseas), up to 1000 players. For each auction the game picks a balanced set sized to the team count (70 for 2 teams, +26 per extra team, max 260): the top-rated players always play, the rest is balanced across keepers, batters, all-rounders and bowlers and leans towards higher ratings. Template: /template.xlsx. Needs `openpyxl`.
- After the auction each player picks their playing XI (max 4 overseas) and locks it in; AI teams auto-pick. Score = XI rating total + bonuses for a keeper, 5+ bowling options and 5+ batting options.

## Run locally
```bash
pip install -r requirements.txt
uvicorn server:app --reload
# open http://localhost:8000
```

## Deploy (free tier is fine)
**Railway:** New Project > Deploy from GitHub repo. The `Procfile` sets the start command. Generate a domain
under Settings > Networking.
**Render:** New Web Service. Build: `pip install -r requirements.txt`. Start:
`uvicorn server:app --host 0.0.0.0 --port $PORT`.

Run a single instance: rooms live in memory, so a restart ends running games.

## Layout
- `server.py`: rooms, WebSocket protocol, auction engine, AI
- `players.py`: player pool and set ordering
- `static/index.html`: the whole client (vanilla JS)

## Ideas
Right to Match, retentions, real stats, spectator chat, persistent rooms (Redis).
