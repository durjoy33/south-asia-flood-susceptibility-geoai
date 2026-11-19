import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import geopandas as gpd, rasterio, numpy as np, glob, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from shapely.geometry import box, LineString
from pyproj import Transformer
A=str(MAP_RASTERS)+'/'
NE=str(NE_VECTOR)+'/'
f=glob.glob(A+'*FINAL_full*.tif')[0]
with rasterio.open(f) as s:
    crs=s.crs; a=s.read(1,masked=True); tr=s.transform; bounds=s.bounds
valid=~np.ma.getmaskarray(a)
pad=150000
xmin,ymin,xmax,ymax=bounds.left-pad,bounds.bottom-pad,bounds.right+pad,bounds.top+pad
world=gpd.read_file(str(COUNTRY_SHP)).clip(box(40,-10,130,55)).to_crs(crs)
names=['Afghanistan','Bangladesh','Bhutan','India','Nepal','Pakistan','Sri Lanka']
study=world[world.name.isin(names)]; other=world[~world.name.isin(names)]
riv=gpd.read_file(NE+'10m_physical/ne_10m_rivers_lake_centerlines.shp').to_crs(crs)
lak=gpd.read_file(NE+'10m_physical/ne_10m_lakes.shp').to_crs(crs)
major={'Indus':1,'Ganges':1,'Brahmaputra':1,'Dihang':1,'Luhit':1,'Godävari':0,'Krishna':0,'Narmada':0,'Tapi':0,'Mahäna Nadï':0,'Cauvery':0,
 'Jhelum':0,'Chenab':0,'Ravi':0,'Sutlej':0,'Beas':0,'Ghäghara':0,'Gandak':0,'Chambal':0,'Son':0,'Tista':0,'Helmand':0,'Kabul':0,'Panj':0,'Betwa':0,'Manas':0,'Yamuna':0,'Kosi':0,'Meghna':0,'Padma':0,'Jamuna':0,'Mahaweli':0,'Harirud':0}
riv=riv[riv.name.isin(major)&riv.intersects(box(xmin,ymin,xmax,ymax))].copy()
riv['maj']=riv.name.map(major)
print(sorted(riv.name.unique()))
fig,ax=plt.subplots(figsize=(8.2,7.4))
ax.set_facecolor('#E4EEF5')
study.plot(ax=ax,color='#9CC3B0',edgecolor='none',zorder=2)
study.boundary.plot(ax=ax,color='#3A3A3A',linewidth=0.9,zorder=6)
riv[riv.maj==0].plot(ax=ax,color='#2B6CA3',linewidth=0.7,zorder=5)
riv[riv.maj==1].plot(ax=ax,color='#0B3C73',linewidth=1.6,zorder=5)
# graticule
tf=Transformer.from_crs(4326,crs,always_xy=True)
for lon in range(60,111,10):
    ys=np.linspace(0,45,60); x,y=tf.transform(np.full_like(ys,lon),ys); ax.plot(x,y,color='#9AA7B2',lw=0.35,ls=(0,(2,3)),zorder=2.5)
    xl,yl=tf.transform(lon,6) if lon<110 else (0,0)
for lat in range(10,41,10):
    xs=np.linspace(55,115,60); x,y=tf.transform(xs,np.full_like(xs,lat)); ax.plot(x,y,color='#9AA7B2',lw=0.35,ls=(0,(2,3)),zorder=2.5)
ax.set_xlim(xmin,xmax); ax.set_ylim(ymin,ymax); ax.set_aspect('equal')
# graticule tick labels along edges
def lonlab(lon):
    xs=np.array([lon]*2); 
for lon in range(60,111,10):
    # find x where graticule meets bottom edge
    ys=np.linspace(0,30,300); x,y=tf.transform(np.full_like(ys,lon),ys); i=np.argmin(abs(y-(ymin+40000)))
    if xmin<x[i]<xmax: ax.text(x[i],ymin+30000,f'{lon}°E',ha='center',va='bottom',fontsize=8,color='#444',zorder=9)
for lat in range(10,41,10):
    xs=np.linspace(55,115,400); x,y=tf.transform(xs,np.full_like(xs,lat)); i=np.argmin(abs(x-(xmin+30000)))
    ax.text(xmin+20000,y[i],f'{lat}°N',ha='left',va='bottom',fontsize=8,color='#444',zorder=9)
halo=[pe.withStroke(linewidth=2.2,foreground='white')]
# river labels
def lab(nm,frac,dx=0,dy=0,rot=None,fs=8.2,bold=True):
    g=riv[riv.name==nm].geometry
    from shapely.ops import linemerge
    m=linemerge(list(g.explode(index_parts=False)) ) if len(g)>1 else g.iloc[0]
    if m.geom_type=='MultiLineString': m=max(m.geoms,key=lambda q:q.length)
    p=m.interpolate(frac,normalized=True); 
    ax.text(p.x+dx,p.y+dy,nm,fontsize=fs,fontstyle='italic',color='#0B3C73',fontweight='bold' if bold else 'normal',ha='center',va='center',path_effects=halo,zorder=10,rotation=rot or 0)
lab('Indus',0.78,-120000,60000,rot=-70)
lab('Ganges',0.55,0,-70000,rot=-20)
lab('Brahmaputra',0.35,0,-80000,rot=0)
lab('Godävari',0.55,-10000,-60000,fs=7.4,bold=False); riv.loc[riv.name=='Godävari']  # name fixed below
# country labels
rp={n:study[study.name==n].geometry.iloc[0].representative_point() for n in names}
cl={'Afghanistan':(rp['Afghanistan'].x-1.0e5,rp['Afghanistan'].y+1.0e5),'Pakistan':(rp['Pakistan'].x-1.5e5,rp['Pakistan'].y-2.5e5),'India':(rp['India'].x-1.0e5,rp['India'].y-1.0e5),
 'Nepal':(rp['Nepal'].x,rp['Nepal'].y-1.0e5),'Bhutan':(rp['Bhutan'].x,rp['Bhutan'].y-6.5e4),'Bangladesh':(rp['Bangladesh'].x+0.1e5,rp['Bangladesh'].y-3.6e5),'Sri Lanka':(rp['Sri Lanka'].x+3.6e5,rp['Sri Lanka'].y)}
ax.plot([rp['Bangladesh'].x,rp['Bangladesh'].x+0.1e5],[rp['Bangladesh'].y-0.6e5,rp['Bangladesh'].y-3.1e5],color='#222',lw=0.7,zorder=11)
for n,(x,y) in cl.items():
    big=n in ('India','Pakistan','Afghanistan')
    ax.text(x,y,n.upper() if big else n,fontsize=9.5 if big else 7.6,fontweight='bold',color='#222',ha='center',va='center',path_effects=halo,zorder=11)
ax.text(-0.95e6,-0.55e6,'Arabian\nSea',fontsize=9,fontstyle='italic',color='#5A7C95',ha='center'); ax.text(0.9e6,-0.55e6,'Bay of\nBengal',fontsize=9,fontstyle='italic',color='#5A7C95',ha='center')
ax.text(0.25e6,1.75e6,'Tibetan Plateau',fontsize=8,fontstyle='italic',color='#8A8A84',ha='center'); ax.text(-1.55e6,0.55e6,'',fontsize=1)
# scale bar (alternating, bottom right)
L=1.0e6; seg=L/4; x0=xmax-0.06*(xmax-xmin)-L; y0=ymin+0.16*(ymax-ymin); h=4.5e4
ax.add_patch(plt.Rectangle((x0-8e4,y0-1.1e5),L+2.6e5,2.6e5,fc='white',ec='#777',lw=0.6,alpha=0.95,zorder=11))
for k in range(4):
    ax.add_patch(plt.Rectangle((x0+k*seg,y0),seg,h,fc='k' if k%2==0 else 'w',ec='k',lw=0.8,zorder=12))
for k,t in enumerate(['0','250','500','750','1,000']):
    ax.text(x0+k*seg,y0+h+2.5e4,t,fontsize=8,ha='center',va='bottom',zorder=12)
ax.text(x0+L/2,y0-4e4,'km',fontsize=8.5,ha='center',va='top',zorder=12)
# north arrow
nx=xmax-0.06*(xmax-xmin); ny=ymax-0.17*(ymax-ymin)
ax.annotate('',xy=(nx,ny+3.2e5),xytext=(nx,ny),arrowprops=dict(arrowstyle='-|>',color='k',lw=1.6,mutation_scale=16),zorder=12); ax.text(nx,ny+3.4e5,'N',ha='center',va='bottom',fontsize=11,fontweight='bold',zorder=12)
ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(''); ax.set_ylabel('')
for sp in ax.spines.values(): sp.set_linewidth(0.8)
leg=[Patch(fc='#9CC3B0',ec='#3A3A3A',label='Study area (1 km modelling grid)'),     Line2D([0],[0],color='#0B3C73',lw=1.6,label='Major rivers (Indus, Ganges, Brahmaputra)'),Line2D([0],[0],color='#2B6CA3',lw=0.7,label='Principal tributaries and peninsular rivers')]
lg=ax.legend(handles=leg,loc='lower left',fontsize=8.5,frameon=True,framealpha=0.97,edgecolor='#777',bbox_to_anchor=(0.045,0.045),title='Legend',title_fontsize=9,fancybox=False); lg.set_zorder(20)
fig.tight_layout(pad=0.4)
fig.savefig(str(FIGS/'fig1_study_area.png'),dpi=400,facecolor='white')
