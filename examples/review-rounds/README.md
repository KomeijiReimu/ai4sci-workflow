# Two rounds on a climate note: demonstrator

Read the [delivered manuscript](research/paper.md) and [latest reply](research/reply.md) together. The estimates come from two published bulletins. The manuscript versions, reviewer comments and responses illustrate a revision. They are not a record of an actual submission or independent signoff.

| Stage | What the files show |
|---|---|
| [Original note](versions/temperature-v0.md) | Gives an annual estimate without identifying the product and uses one year to draw a long-term conclusion. |
| [First revision](versions/temperature-v1.md) and [reply](versions/temperature-reply-v1.md) | Reviewer A's attribution question, `I1`, appeared answered once the note named ERA5. Reviewer B's `I2` led to the removal of the threshold claim. |
| [Second revision](versions/temperature-v2.md) and [reply](versions/temperature-reply-v2.md) | B reopened `I1` and asked to replace the ERA5 number with the WMO figure. A wanted to keep the ERA5 result. The revision gives both estimates and identifies the WMO uncertainty. A new concern, `I3`, challenged the baseline. The response explains why the manuscript keeps it. |

The [issue trail](research/rounds.json) preserves each comment, its location in the version under review and the earlier disposition. Compare the two differently named replies to see what the author changed. `research/` contains the delivery copies, separate from `versions/`.

**Evidence.** The [WMO passages](inputs/wmo.txt) come from the opening assessment and the Secretary-General's statement in the [10 January 2025 WMO bulletin](https://wmo.int/news/media-centre/wmo-confirms-2024-warmest-year-record-about-155degc-above-pre-industrial-level). The [Copernicus passages](inputs/c3s.txt) come from the global surface air temperature highlights in the [same day's Copernicus bulletin](https://climate.copernicus.eu/copernicus-2024-first-year-exceed-15degc-above-pre-industrial-level). The texts are the same excerpts retained by the [climate source study](../climate-sources/research/sources.json). The revision needs neither new measurements nor a reconstructed experiment plan.

From the checkout:

```sh
python3 checks/rounds.py examples/review-rounds
```

Expected exit: `0`. In round 2, `history[1].reopened` contains `I1`. `I2` carries forward, and `I3` ends with `no-change`. Read both bulletins and judge the interpretation before treating the note as scientifically ready.
