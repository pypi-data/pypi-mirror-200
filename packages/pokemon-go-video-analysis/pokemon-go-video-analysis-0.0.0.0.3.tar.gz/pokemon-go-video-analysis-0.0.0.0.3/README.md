# Pokémon Go Video Analysis

Tools for analyzing Pokémon Go Player vs. Player (PvP) Videos.

```commandline
from battle_logger.pipeline import BattleLoggerPipeline

pogo_pipeline = BattleLoggerPipeline()
output = pogo_pipeline.exec('path/to/video')
pogo_pipeline.save_output(out_path="test_output", basename="battle_logger_output")
```

Extract battles from videos and analyze what Pokémon appear in which battles:

![](https://github.com/prateekt/pokemon-go-video-analysis/blob/cc0298a845b43067ebc5629f1f8090e9b11b4b91/readme_figs/battle_1.png?raw=true)


Log your battles and analyze your Pokemon's performance:

![](https://github.com/prateekt/pokemon-go-video-analysis/blob/cc0298a845b43067ebc5629f1f8090e9b11b4b91/readme_figs/Screenshot%202023-04-02%20at%2010.05.32%20PM.png?raw=true)

<b>Installation:</b>

```
make conda_dev
conda activate pogo_video_analysis_env
pip install pokemon-go-video-analysis
```