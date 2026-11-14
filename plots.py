from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mas import Settings,make_scenario

def charts(output='results'):
    out=Path(output)
    with (out/'summary.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    scenarios=['light','medium','heavy']
    for key,title,filename,ylabel in [
        ('completion_rate','Completed orders','completion.png','Fraction of completed orders'),
        ('mean_delivery_ticks','Mean time from release to delivery','delivery.png','Simulation ticks'),
        ('messages','All transmitted messages','messages.png','Messages per run'),
        ('mean_assignment_ticks','Mean assignment wait','assignment.png','Simulation ticks'),
        ('message_bytes','Communication traffic','traffic.png','Bytes per run'),
        ('emergency_recoveries','Recorded emergency interventions','recoveries.png','Interventions per run'),
    ]:
        fig,ax=plt.subplots(figsize=(7.6,4.5))
        vals={m:[float(next(r[key+'_mean'] for r in rows if r['scenario']==s and r['mode']==m)) for s in scenarios] for m in ('central','contract')}
        x=range(len(scenarios));width=.36
        ax.bar([i-width/2 for i in x],vals['central'],width,label='Centralized')
        ax.bar([i+width/2 for i in x],vals['contract'],width,label='Contract Net')
        ax.set_xticks(list(x),['Light (16)','Medium (30)','Heavy (55)'])
        ax.set_ylabel(ylabel);ax.set_title(title);ax.legend()
        if key=='completion_rate':ax.set_ylim(0,1.08)
        ax.grid(axis='y',alpha=.25);fig.tight_layout()
        fig.savefig(out/filename,dpi=175);plt.close(fig)
    cfg=Settings(width=20,height=20,n_robots=8,n_stations=2,n_orders=30,seed=0,obstacles=.10)
    sc=make_scenario(cfg)
    fig,ax=plt.subplots(figsize=(7,6.5))
    if sc.walls:
        xs,ys=zip(*sc.walls);ax.scatter(xs,ys,marker='s',s=36,color='0.3',label='Obstacles')
    for pos,label,marker in [(sc.courier_positions,'Couriers','o'),(sc.charger_positions,'Charging stations','P')]:
        xs,ys=zip(*pos);ax.scatter(xs,ys,marker=marker,s=95,label=label)
    ax.set_xlim(-.5,sc.width-.5);ax.set_ylim(-.5,sc.height-.5)
    ax.set_xticks(range(sc.width));ax.set_yticks(range(sc.height));ax.grid(alpha=.2)
    ax.set_aspect('equal');ax.legend(loc='upper center',bbox_to_anchor=(.5,-.06),ncol=3)
    ax.set_title('Example warehouse and agent starting positions')
    fig.tight_layout();fig.savefig(out/'warehouse.png',dpi=170,bbox_inches='tight');plt.close(fig)
if __name__=='__main__':charts()
