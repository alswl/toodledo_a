# alswl's TODO metrics analytics tool

Less input, more output.

Get completed todo csv:
https://www.toodledo.com/tools/csv.php?completed=1

```
c ~/download/toodledo_completed_*.csv G -v smoking G -v 'waste time' > ~/download/toodledo_completed.csv.filterd
python ./toodledo_a.py --days 7 ~/download/toodledo_completed.csv.filterd
c ~/download/toodledo_completed.csv.filterd_timer.csv | dos2unix | sed 's/^/|/g' | sed 's/$/| | |/g' | sed 's/,/|/g' | sort -g V


for i in {27..31}; do open https://www.rescuetime.com/dashboard/for/the/day/of/2020-1-$i; done
```
