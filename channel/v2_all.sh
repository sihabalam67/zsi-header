#!/bin/bash
# Render every standalone Short in channel/shorts_v2.py in launch-date order; youtube/auto_swap.py --v2 swaps each
# one in as soon as it's rendered and checked. Skips Shorts already listed in channel/out/vshorts_swapped_v2.json.
cd "$(dirname "$0")"
B=build/vshorts; mkdir -p $B; LOG=$B/render_v2.log
for n in ep03_short_barrel ep03_short_feathers ep04_short_cards ep04_short_savings ep04_short_why ep05_short_layoffs \
         ep01_short_prices ep01_short_wages ep01_short_rule70 ep02_short_price ep02_short_payment ep02_short_supply \
         ep05_short_hiring; do
  grep -q "\"$n\"" out/vshorts_swapped_v2.json 2>/dev/null && continue
  start=$(date +%s)
  if python3 shorts_v2.py $n > $B/r2_$n.log 2>&1; then
    echo "OK $n $(( $(date +%s) - start ))s" >> $LOG
  else
    echo "FAIL $n" >> $LOG
  fi
done
echo ALLDONE >> $LOG
