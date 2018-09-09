# alswl's TODO metrics analytics tool

Less input, more output.

Get completed todo csv:
https://www.toodledo.com/tools/csv.php?completed=1

```
c ~/download/toodledo_completed.csv G -v smoking G -v 'waste time' > ~/download/toodledo_completed.csv.filterd
python ./toodledo_a.py --days 7 ~/download/toodledo_completed.csv.filterd
```
