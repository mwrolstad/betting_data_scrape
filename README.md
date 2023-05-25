# betting_data_scrape

An easy tool to scrape the current odds listed on bettingdata.com

### Use as a command line:

```cmd
python3 src/betting_data_scrape/__init__.py --sport "MLB" --game_date "05-21-2023"
```

### Import and use as a package:

```python
from betting_data_scrape import BetScraper
import json
odds_scraper = BetScraper(sport="MLB", game_date="05-21-2023")
print(json.dumps(odds_scraper.odds[0], indent=2))
{
  "game_date": "5/21/23",
  "home_team": "Cincinnati Reds",
  "home_team_loc": "Cincinnati",
  "home_team_name": "Reds",
  "home_team_abrv": "CIN",
  "home_moneyline": 115,
  "home_run_line": 1.5,
  "home_run_line_payout": -144,
  "away_team": "New York Yankees",
  "away_team_loc": "New York",
  "away_team_name": "Yankees",
  "away_team_abrv": "NYY",
  "away_moneyline": -135,
  "away_run_line": -1.5,
  "away_run_line_payout": 119,
  "over_under": 8.5,
  "over": -115,
  "under": -105
}
```
