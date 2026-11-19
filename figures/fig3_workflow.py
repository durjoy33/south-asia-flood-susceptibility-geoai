import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, textwrap
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from xml.sax.saxutils import escape
plt.rcParams['font.family']='DejaVu Sans'
W,H=7.2,7.7; m=0.15; fw=W-2*m; cw=2.2; gap=(fw-3*cw)/2; xs=[m,m+cw+gap,m+2*(cw+gap)]; hw=3.4
C={'in':('#EAF0F6','#4F7191','#2A4A66'),'des':('#E5F3EE','#2F8A72','#1F6A56'),'rnd':('#FCF1DC','#B9801A','#8A5E0E'),'sp':('#DDECF8','#1F5F99','#174A78'),'sup':('#EFEAF6','#7059A0','#59458A'),'ev':('#F3E9F3','#8B4A8B','#6E366E'),'map':('#FBE8E4','#B1432F','#8F3322')}
# nodes: id,x,y(top-left in inches from top),w,h,title,lines,kind,thick,bullets
N=[]
def node(i,x,y,w,h,t,l,k,thick=False,bul=False): N.append(dict(id=i,x=x,y=y,w=w,h=h,t=t,l=l,k=k,thick=thick,bul=bul))
y1=0.15; h1=0.72
node('inv',m,y1,hw,h1,'Flood inventory',['n = 3,416 presence and background records'],'in')
node('pred',W-m-hw,y1,hw,h1,'21 conditioning factors',['Harmonised to a 1-km equal-area grid'],'in')
y2=y1+h1+0.3; h2=0.62
node('grp',m,y2,fw,h2,'1-km raster-cell grouping',['Each cell is one indivisible group in every split'],'des')
y3=y2+h2+0.3; h3=0.72
node('dep',m,y3,hw,h3,'Spatial dependence',['Moran’s I; variogram range 839.0 km'],'des')
node('mod',W-m-hw,y3,hw,h3,'Six classifiers',['LR · SVM-RBF · RF · XGBoost · LightGBM · MLP'],'des')
bus1=y3+h3+0.26
y4=bus1+0.28; h4=1.28
node('A',xs[0],y4,cw,h4,'A  Grouped random',['Exploratory nested run','6 seeds × 5 folds, fixed hyperparameters'],'rnd',bul=True)
node('B',xs[1],y4,cw,h4,'B  Buffered spatial (primary)',['5 K-means regions','629.3 km exclusion buffer','Nested tuning and calibration'],'sp',thick=True,bul=True)
node('Cc',xs[2],y4,cw,h4,'C  Supplementary',['Size-matched random reference','Decomposition C1–C4','Buffer sensitivity'],'sup',bul=True)
bus2=y4+h4+0.22
y5=bus2+0.24; h5=0.72
node('ev',m,y5,fw,h5,'Evaluation and model selection',['ROC-AUC, PR-AUC, Brier score, ECE; random–spatial gap; Random Forest selected for mapping'],'ev')
y6=y5+h5+0.36; h6=0.8
node('o1',xs[0],y6,cw,h6,'Operational surface',['Full-inventory Random Forest at 1 km'],'map')
node('o2',xs[1],y6,cw,h6,'Map comparison',['Spatial-fold mean and SD vs matched reference'],'map')
node('o3',xs[2],y6,cw,h6,'Descriptive analysis',['Gi* clusters; class areas by country'],'map')
H=y6+h6+0.45
E=[('inv','grp'),('pred','grp'),('grp','dep'),('grp','mod')]  # drawn manually below
def cx(n): return n['x']+n['w']/2
nd={n['id']:n for n in N}
# edges as polylines in inches (y from top); arrow flag
L=[]
L.append(([(m+1.7,y1+h1),(m+1.7,y2)],True)); L.append(([(W-m-1.7,y1+h1),(W-m-1.7,y2)],True))
L.append(([(m+1.7,y2+h2),(m+1.7,y3)],True)); L.append(([(W-m-1.7,y2+h2),(W-m-1.7,y3)],True))
L.append(([(m+1.7,y3+h3),(m+1.7,bus1)],False)); L.append(([(xs[0]+cw/2,bus1),(xs[2]+cw/2,bus1)],False)); L.append(([(W-m-1.7,y3+h3),(W-m-1.7,bus1)],False))
for x in xs: L.append(([(x+cw/2,bus1),(x+cw/2,y4)],True))
for x in xs: L.append(([(x+cw/2,y4+h4),(x+cw/2,bus2)],False))
L.append(([(xs[0]+cw/2,bus2),(xs[2]+cw/2,bus2)],False)); L.append(([(W/2,bus2),(W/2,y5)],True))
for x in xs: L.append(([(x+cw/2,y5+h5),(x+cw/2,y6)],True))
fig=plt.figure(figsize=(W,H)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis('off')
FS=8.6; TFS=9.4
for n in N:
    fc,ec,tc=C[n['k']]
    ax.add_patch(FancyBboxPatch((n['x'],n['y']),n['w'],n['h'],boxstyle='round,pad=0,rounding_size=0.07',fc=fc,ec=ec,lw=2.0 if n['thick'] else 1.0,zorder=2))
    yy=n['y']+0.1
    for t in textwrap.wrap(n['t'],int((n['w']-0.16)*72/(TFS*0.64))):
        ax.text(n['x']+n['w']/2,yy,t,ha='center',va='top',fontsize=TFS,fontweight='bold',color=tc,zorder=3); yy+=TFS*1.3/72
    yy+=0.04
    for ln in n['l']:
        pre='• ' if n['bul'] else ''
        for j,t in enumerate(textwrap.wrap(ln,int((n['w']-0.2)*72/(FS*0.56))-(2 if n['bul'] else 0))):
            if n['bul']: ax.text(n['x']+0.1+(0.12 if j else 0),yy,(pre if j==0 else '')+t,ha='left',va='top',fontsize=FS,color='#222',zorder=3)
            else: ax.text(n['x']+n['w']/2,yy,t,ha='center',va='top',fontsize=FS,color='#222',zorder=3)
            yy+=FS*1.28/72
        yy+=0.03
for pts,arr in L:
    xs_,ys_=zip(*pts)
    if arr:
        ax.add_patch(FancyArrowPatch(pts[-2],pts[-1],arrowstyle='-|>',mutation_scale=10,lw=1.1,color='#555',zorder=4,shrinkA=0,shrinkB=0))
        if len(pts)>2: ax.plot(xs_[:-1],ys_[:-1],color='#555',lw=1.1,zorder=4)
    else: ax.plot(xs_,ys_,color='#555',lw=1.1,zorder=4,solid_capstyle='butt')
ax.text(xs[0]+cw/2+0.1,(y5+h5+y6)/2,'Raster prediction branch',fontsize=8,fontweight='bold',color=C['map'][2],va='center')
ax.text(m,H-0.2,'Performance values are cross-validation estimates under the stated designs, not independent external validation.',fontsize=6.8,style='italic',color='#444',va='center')
fig.savefig(str(FIGS/'fig3_workflow.png'),dpi=600,facecolor='white')
# ---------- drawio ----------
S=100
cells=['<mxCell id="0"/>','<mxCell id="1" parent="0"/>']
for n in N:
    fc,ec,tc=C[n['k']]
    body='<br>'.join((('• ' if n['bul'] else '')+escape(l)) for l in n['l'])
    val=f'<b><font color="{tc}" style="font-size:13px">{escape(n["t"])}</font></b><br>{body}'
    align='left' if n['bul'] else 'center'
    st=f'rounded=1;arcSize=6;whiteSpace=wrap;html=1;align={align};verticalAlign=top;spacingTop=6;spacingLeft=8;spacingRight=8;fillColor={fc};strokeColor={ec};strokeWidth={2.5 if n["thick"] else 1.5};fontSize=12;fontColor=#222222;'
    if n['bul']: st+='spacingLeft=10;'
    # for left-aligned bullets, title also left -> acceptable; keep title centered via separate div
    if n['bul']:
        val=f'<div style="text-align:center"><b><font color="{tc}" style="font-size:13px">{escape(n["t"])}</font></b></div>'+body
    cells.append(f'<mxCell id="{n["id"]}" value="{escape(val,{chr(34):"&quot;"})}" style="{st}" vertex="1" parent="1"><mxGeometry x="{n["x"]*S:.0f}" y="{n["y"]*S:.0f}" width="{n["w"]*S:.0f}" height="{n["h"]*S:.0f}" as="geometry"/></mxCell>')
eid=0
def edge(pts,arr):
    global eid
    eid+=1
    (x0,y0),(x1,y1_)=pts[0],pts[-1]
    way=''.join(f'<mxPoint x="{x*S:.0f}" y="{y*S:.0f}"/>' for x,y in pts[1:-1])
    st=f'edgeStyle=none;html=1;strokeColor=#555555;strokeWidth=1.5;endArrow={"block" if arr else "none"};endFill=1;'
    cells.append(f'<mxCell id="e{eid}" style="{st}" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{x0*S:.0f}" y="{y0*S:.0f}" as="sourcePoint"/><mxPoint x="{x1*S:.0f}" y="{y1_*S:.0f}" as="targetPoint"/><Array as="points">{way}</Array></mxGeometry></mxCell>')
for pts,arr in L: edge(pts,arr)
cells.append(f'<mxCell id="lbl" value="Raster prediction branch" style="text;html=1;align=left;verticalAlign=middle;fontStyle=1;fontSize=11;fontColor={C["map"][2]};" vertex="1" parent="1"><mxGeometry x="{(xs[0]+cw/2+0.1)*S:.0f}" y="{((y5+h5+y6)/2-0.12)*S:.0f}" width="220" height="24" as="geometry"/></mxCell>')
cells.append(f'<mxCell id="note" value="Performance values are cross-validation estimates under the stated designs, not independent external validation." style="text;html=1;align=left;verticalAlign=middle;fontStyle=2;fontSize=10;fontColor=#444444;" vertex="1" parent="1"><mxGeometry x="{m*S:.0f}" y="{(H-0.32)*S:.0f}" width="680" height="24" as="geometry"/></mxCell>')
xml=f'<mxfile host="app.diagrams.net"><diagram id="workflow" name="Figure 3 workflow"><mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{int(W*S)}" pageHeight="{int(H*S)}" math="0" shadow="0"><root>'+''.join(cells)+'</root></mxGraphModel></diagram></mxfile>'
open(str(FIGS/'fig3_workflow.drawio'),'w').write(xml)
print(W,H)
