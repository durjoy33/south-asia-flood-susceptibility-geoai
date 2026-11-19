import sys,pathlib; sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'postprocessing')); from config import *
import rasterio, numpy as np, glob, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
T=str(FILLED)+'/filled_'
def rd(n):
    f=glob.glob(T+'*'+n+'*.tif')[0]
    with rasterio.open(f) as s: a=s.read(1).astype('float64'); nd=s.nodata
    return np.ma.masked_equal(a,nd)
m=np.load(MASK); r,c=np.where(m); p=40
sl=(slice(max(r.min()-p,0),r.max()+p),slice(max(c.min()-p,0),c.max()+p))
br=np.load(JENKS/'breaks.npy'); cls=np.ma.masked_equal(np.load(JENKS/'cls_filled.npy'),-99)
z=rd('gi_star_z'); gc=rd('gi_star_class'); zs=np.ma.masked_where(np.ma.getdata(gc)==0,z)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
fig,ax=plt.subplots(1,2,figsize=(16,7.6))
cm=plt.get_cmap('RdBu_r').copy(); cm.set_bad((1,1,1,0))
im=ax[0].imshow(np.clip(zs,-5,5)[sl],cmap=cm,vmin=-5,vmax=5,interpolation='nearest'); ax[0].set_axis_off()
cb=plt.colorbar(im,ax=ax[0],shrink=0.62,fraction=0.04,pad=0.02,aspect=22); cb.outline.set_linewidth(0.8); cb.set_label('Gi* z-score',fontsize=12)
cols=['#FFFFB2','#FECC5C','#FD8D3C','#E31A1C','#800026']
cm5=ListedColormap(cols); cm5.set_bad((1,1,1,0))
ax[1].imshow(cls[sl],cmap=cm5,vmin=0.5,vmax=5.5,interpolation='nearest'); ax[1].set_axis_off()
names=['Very low','Low','Moderate','High','Very high']
h=[Patch(fc=cols[i],ec='#555',lw=0.5,label=f'{names[i]}  ({br[i]:.3f}–{br[i+1]:.3f})') for i in range(5)][::-1]
lg=ax[1].legend(handles=h,title='Susceptibility class\n(Jenks natural breaks)',loc='lower right',bbox_to_anchor=(1.03,-0.01),fontsize=10.5,title_fontsize=11,frameon=True,framealpha=0.95,edgecolor='#999')
lg._legend_box.align='left'
ax[0].set_title('(a) FDR-adjusted Gi* score clusters',loc='left',fontsize=15,fontweight='bold')
ax[1].set_title('(b) Final Flood Susceptibility — Random Forest',loc='left',fontsize=15,fontweight='bold')
fig.suptitle('Flood susceptibility score and local spatial concentration across South Asia',fontsize=17,fontweight='bold',y=0.99)
fig.tight_layout(rect=(0,0,1,0.95)); fig.subplots_adjust(wspace=-0.12)
fig.savefig(str(FIGS/'fig_final_susceptibility_jenks_gistar.png'),dpi=480,facecolor='white',bbox_inches='tight',pad_inches=0.15)
fig.savefig(str(FIGS/'fig_final_susceptibility_jenks_gistar.pdf'),facecolor='white',bbox_inches='tight',pad_inches=0.15)
