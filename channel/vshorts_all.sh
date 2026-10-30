#!/bin/bash
# Render every vertical Short in date order, skipping ones already swapped (channel/out/vshorts_swapped.json).
cd /home/user/zsi-header/channel
LOG=/home/user/zsi-header/channel/build/vshorts/render_all.log
for n in ep03_short_jump ep03_short_barrel ep03_short_feathers ep04_short_cards ep04_short_savings ep04_short_why \
         ep05_short_layoffs ep01_short_prices ep01_short_wages ep01_short_rule70 ep02_short_price ep02_short_payment \
         ep02_short_supply ep05_short_hiring; do
  grep -q "\"$n\"" /home/user/zsi-header/channel/out/vshorts_swapped.json 2>/dev/null && { echo "OK $n already-swapped" >> $LOG; continue; }
  start=$(date +%s)
  if python3 vshorts.py $n > /home/user/zsi-header/channel/build/vshorts/r_$n.log 2>&1; then
    echo "OK $n $(( $(date +%s) - start ))s $(grep -c 'WARNING' /home/user/zsi-header/channel/build/vshorts/r_$n.log) warnings" >> $LOG
  else
    echo "FAIL $n" >> $LOG
  fi
done
echo ALLDONE >> $LOG
