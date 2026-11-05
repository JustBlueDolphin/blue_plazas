"""Render the published shop inventory. Requires matplotlib and shapely.

The inventory is a v1.7.2 snapshot, checked against compiled YTYP/YMAP doors.
Re-export the inventory after geometry/placement changes; this only redraws it.
"""
from pathlib import Path
import json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch, Rectangle

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/maps'
DATA=json.loads((OUT/'shop_inventory.json').read_text())
COLORS={'DP01':'#c5e9ec','DP02':'#95d4df','DP03':'#69b9d2','DP04':'#44a0c2',
        'DP05':'#f3bd8e','DP07':'#d1c6e9','DP08':'#b9d9ac'}
INK='#173449'; MUTED='#526a79'; BG='#f7fafb'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})

def base(ax,upper=False):
 ax.set_aspect('equal');ax.axis('off');ax.set_facecolor(BG)
 ax.set_xlim((-74,-33) if upper else (-77,3));ax.set_ylim(-32,25)
 # Orienting courtyard; no inferred parking-space, stair or access geometry.
 if not upper:
  ax.add_patch(Rectangle((-45,-25),44,24,facecolor='#e9eef0',edgecolor='none',zorder=0))
  ax.text(-24,-17,'PARKING / COURTYARD',ha='center',fontsize=12,color=MUTED,weight='bold')
  ax.text(-24,-20,'Front of the shops',ha='center',fontsize=10,color=MUTED)
  ax.text(-17,22.2,'BLUE-ROOF ROW',ha='center',fontsize=10,color=MUTED,weight='bold')
 for unit in DATA['units']:
  if (unit['level']=='upper')!=upper:continue
  for poly in unit['footprints_plan']:
   ax.add_patch(Patch(poly,facecolor=COLORS[unit['id']],edgecolor=INK,linewidth=1.3,zorder=2))
  uid=unit['id']
  label={'DP01':(-30.5,10),'DP02':(-22.09,10),'DP03':(-13.19,10),'DP04':(-4.34,10),
         'DP05':(-57.5,-8),'DP07':(-43.2,5.15),'DP08':(-59.0,-10.5)}[uid]
  ax.text(*label,uid,ha='center',va='center',fontsize=13 if uid=='DP07' else 16,weight='bold',color=INK,zorder=5)
  if uid in ('DP05','DP08'):
   ax.text(label[0],label[1]-2.4,'ONE LARGE SHOP',ha='center',fontsize=8.5,color=INK,zorder=5)
  for entrance in unit['entrances']:
   x,y=entrance['centre_plan'];nx,ny=entrance['outward_plan']
   # A bright opening marker spans the two leaf positions.
   tangent=(-ny,nx)
   ax.plot([x-1.1*tangent[0],x+1.1*tangent[0]],[y-1.1*tangent[1],y+1.1*tangent[1]],color='#fff',lw=6,zorder=6)
   ax.plot(x,y,'o',ms=5,color=INK,zorder=7)
   eid=entrance['id']
   if uid in ('DP01','DP02','DP03','DP04'):tx,ty=x,-3.0
   elif uid=='DP07':tx,ty=-42.0,-1.8
   elif eid=='DP05-D3':tx,ty=-71.3,-25.5
   elif uid=='DP05':tx,ty=-40.8,y
   else:tx,ty=x+6.6,y
   ax.annotate(eid,xy=(x,y),xytext=(tx,ty),ha='center',va='center',fontsize=9,weight='bold',color=INK,
      arrowprops={'arrowstyle':'-','color':INK,'lw':1},bbox={'facecolor':'white','edgecolor':'none','pad':2},zorder=8)
 # North uses the same world-to-plan rotation as the shop geometry.
 x,y=(-71,18) if upper else (-70,17)
 dx,dy=math.sin(math.radians(49.74)),math.cos(math.radians(49.74))
 ax.annotate('',xy=(x+4*dx,y+4*dy),xytext=(x,y),arrowprops={'arrowstyle':'-|>','color':INK,'lw':1.7})
 ax.text(x+4.8*dx,y+4.8*dy,'N',color=INK,fontsize=10,weight='bold',ha='center')
 x,y=(-69,-30) if upper else (-39,-29)
 ax.plot([x,x+10],[y,y],color=INK,lw=2)
 for v in (x,x+5,x+10):ax.plot([v,v],[y-.45,y+.45],color=INK,lw=1)
 ax.text(x+5,y+1,'10 m',ha='center',fontsize=8,color=MUTED)

fig=plt.figure(figsize=(17,10),facecolor=BG)
fig.text(.045,.94,'DEL PERRO PLAZA',color=INK,fontsize=28,weight='bold')
fig.text(.045,.904,'Shop & entrance guide',color=MUTED,fontsize=17)
fig.text(.955,.933,'7 SHOPS  /  10 ENTRANCES  /  20 DOOR LEAVES',ha='right',color=INK,fontsize=11,weight='bold')
fig.text(.955,.903,'Blue Plazas · v1.7.2',ha='right',color=MUTED,fontsize=10)
ax=fig.add_axes([.035,.20,.61,.65]);base(ax)
ax2=fig.add_axes([.65,.20,.32,.65]);base(ax2,True)
fig.text(.05,.85,'01  GROUND FLOOR',color=INK,fontsize=13,weight='bold')
fig.text(.68,.85,'02  UPPER FLOOR',color=INK,fontsize=13,weight='bold')
fig.text(.68,.822,'DP08 is above the red-roof wing.',color=MUTED,fontsize=10)
fig.text(.05,.153,'READING A DOOR NAME',color=INK,fontsize=11,weight='bold')
fig.text(.05,.113,'DP05-D3-L',color=INK,fontsize=20,weight='bold')
fig.text(.22,.125,'DP05 = shop  ·  D3 = entrance 3  ·  L = left leaf',color=INK,fontsize=12)
fig.text(.22,.097,'L / R are viewed from OUTSIDE, looking into that doorway.',color=MUTED,fontsize=11)
fig.text(.05,.045,'Blank rentable shells — business types are chosen by players.  •  Existing shop IDs are retained; there is no separate DP06.',color=MUTED,fontsize=10)
fig.text(.05,.022,'Floor outlines are a plan guide, not a construction survey. Entrance markers are checked against compiled door placements.',color=MUTED,fontsize=9)
fig.savefig(OUT/'plaza_shop_map.png',dpi=160,facecolor=BG)
fig.savefig(OUT/'plaza_shop_map.svg',facecolor=BG)
plt.close(fig)
print(OUT/'plaza_shop_map.png')
