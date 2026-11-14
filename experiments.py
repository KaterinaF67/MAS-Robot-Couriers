import csv
import json
import statistics
from pathlib import Path
from mas import Settings,Simulation,make_scenario

SCENARIOS={
    'light':dict(width=16,height=16,n_robots=7,n_stations=2,n_orders=16,arrivals=100,max_ticks=700,obstacles=.05),
    'medium':dict(width=20,height=20,n_robots=8,n_stations=2,n_orders=30,arrivals=110,max_ticks=950,obstacles=.10),
    'heavy':dict(width=24,height=24,n_robots=10,n_stations=3,n_orders=55,arrivals=100,max_ticks=1400,obstacles=.12),
}
METRICS=('completion_rate','mean_delivery_ticks','mean_assignment_ticks','messages','coordination_messages','message_bytes','coordination_ticks','distance_cells','collisions_prevented','emergency_recoveries','deadlock_recoveries','unfinished')

def conduct(directory='results',seeds=range(10)):
    out=Path(directory);out.mkdir(parents=True,exist_ok=True)
    records=[]
    for name,kw in SCENARIOS.items():
        for seed in seeds:
            cfg=Settings(**kw,seed=seed,scenario=name)
            scenario=make_scenario(cfg)
            for mode in ('central','contract'):
                sim=Simulation(cfg,mode,scenario)
                row=sim.run();records.append(row)
                print(f'{name:7s} seed={seed:02d} {mode:8s} done={row["completed"]}/{row["orders"]} messages={row["messages"]}')
    with (out/'runs.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,records[0]);w.writeheader();w.writerows(records)
    summary=[]
    for s in SCENARIOS:
        for m in ('central','contract'):
            group=[r for r in records if r['scenario']==s and r['mode']==m]
            d={'scenario':s,'mode':m,'n':len(group)}
            for metric in METRICS:
                x=[r[metric] for r in group if r[metric] is not None]
                d[metric+'_mean']=round(statistics.mean(x),3) if x else None
                d[metric+'_sd']=round(statistics.stdev(x),3) if len(x)>1 else 0
            summary.append(d)
    with (out/'summary.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,summary[0]);w.writeheader();w.writerows(summary)
    (out/'config.json').write_text(json.dumps({'seeds':list(seeds),'scenarios':SCENARIOS,'methods':['central','contract']},indent=2),encoding='utf-8')
    return records,summary

if __name__=='__main__':conduct()
