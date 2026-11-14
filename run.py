import argparse
import csv
import json
from pathlib import Path
from mas import Settings, Simulation, make_scenario

def main():
    p=argparse.ArgumentParser(description='Multi-agent courier simulation (LR2)')
    p.add_argument('--mode',choices=['central','contract','both'],default='both')
    p.add_argument('--seed',type=int,default=42)
    p.add_argument('--width',type=int,default=18)
    p.add_argument('--height',type=int,default=18)
    p.add_argument('--robots',type=int,default=6)
    p.add_argument('--stations',type=int,default=2)
    p.add_argument('--orders',type=int,default=30)
    p.add_argument('--ticks',type=int,default=750)
    p.add_argument('--obstacles',type=float,default=.10)
    p.add_argument('--trace',action='store_true')
    p.add_argument('--output',default='results/manual')
    a=p.parse_args()
    cfg=Settings(seed=a.seed,width=a.width,height=a.height,n_robots=a.robots,n_stations=a.stations,n_orders=a.orders,max_ticks=a.ticks,obstacles=a.obstacles,scenario='manual')
    scenario=make_scenario(cfg)
    directory=Path(a.output);directory.mkdir(parents=True,exist_ok=True)
    results=[]
    for mode in ('central','contract') if a.mode=='both' else (a.mode,):
        sim=Simulation(cfg,mode,scenario,trace=a.trace)
        item=sim.run();results.append(item)
        if a.trace:(directory/f'{mode}_trace.json').write_text(json.dumps(sim.events,indent=2,ensure_ascii=False),encoding='utf-8')
        print(json.dumps(item,ensure_ascii=False,indent=2))
    with (directory/'summary.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=results[0]);writer.writeheader();writer.writerows(results)
if __name__=='__main__':main()
