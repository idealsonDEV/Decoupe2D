from Rect2DPackLib import newPacker
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
from matplotlib.backends.backend_pdf import PdfPages
import random
import datetime

def Solver2D(morceaux, plans):
	# Nouvelle empacteur
	packer = newPacker()
	# Ajouter à la fil des rectangle à placer
	for r in morceaux:
		packer.add_rect(*r)
	# Ajouter un plan
	for p in plans:
		wd, hg, qt, iden = p
		packer.add_bin(width=wd, height=hg, count=qt, bid=iden)
	# Resoudre
	packer.pack()
	return (len(packer), packer.rect_list(), packer.waste_list(), packer.empty_list(), packer.bin_list())

def Show2D(nplans, mor_list):
    for i in range(nplans):
        #print(f"Feuille: {i+1}")
        fig = plt.figure()
        ax = fig.add_subplot()
        r = lambda: random.randint(25,210)
        ax.add_patch(matplotlib.patches.Rectangle((0,0), 6, 6, fill=None, hatch='///'))
        for mor in mor_list:
            p, x, y, w, h, lab = mor
            if i == p:
                #print(f"    label:{lab}, x:{x}, y:{y}, largeur:{w}, hauteur:{h}")
                ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=True, color='#%02X%02X%02X' % (r(),r(),r())))
                ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=False))
                ax.text(x, y+h/2, str(h), horizontalalignment='left', verticalalignment='center')
                ax.text(x+w/2, y+h, str(w), horizontalalignment='center', verticalalignment='top')
                ax.text(x+w/2, y+h/2, lab, horizontalalignment='center', verticalalignment='center')
        plt.xlim([0, 6])
        plt.ylim([0, 6])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show(block=False)

def PrintPDF2D(nplans, mor_list, waste, newaste, dim, bin_lst, lines, space):
    dwidth, dheight = dim
    with PdfPages('Impression '+ 'Vitre Claire 5 mm' +'.pdf') as pdf:
            for i in range(nplans):
                dwidth, dheight, bid = bin_lst[i]
                # A4 canvas
                fig_width_cm = 29.7
                fig_height_cm = 21
                inches_per_cm = 1 / 2.54
                fig_width = fig_width_cm * inches_per_cm
                fig_height = fig_height_cm * inches_per_cm
                fig_size = [fig_width, fig_height]

                plt.rc('text', usetex=False)
                fig = plt.figure()
                fig.set_size_inches(fig_size)
                ax = fig.add_subplot()
                r = lambda: random.randint(25,210)
                ax.add_patch(matplotlib.patches.Rectangle((0,0), dwidth, dheight, fill=None, hatch='/'))
                ax.xaxis.set_visible(False)
                ax.yaxis.set_visible(False)
                ax.axis('off')
                ax.text(dwidth/2,-80, str(dwidth),ha='center', va='top', fontsize=14, fontweight='bold')
                ax.text(-65,dheight/2,str(dheight),ha='right', va='center', fontsize=14, fontweight='bold')
                for mor in mor_list:
                    p, x, y, w, h, lab = mor
                    if i == p:
                        ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=True, color='white'))
                        ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=False))
                for wst in waste:
                    wp, wx, wy, ww, wh = wst
                    if i == wp:
                        ax.add_patch(matplotlib.patches.Rectangle((wx, wy), ww, wh, fill=True, color='#FFCAC9'))
                        ax.add_patch(matplotlib.patches.Rectangle((wx, wy), ww, wh, fill=False))
                for wst in newaste:
                    wp, wx, wy, ww, wh, wid = wst
                    if i == wp:
                        ax.add_patch(matplotlib.patches.Rectangle((wx, wy), ww, wh, fill=True, color='#A4CAFF'))
                        ax.add_patch(matplotlib.patches.Rectangle((wx, wy), ww, wh, fill=False))
                        ax.text(wx+ww/2, wy+wh/2, 'C'+str(wid)+'\n'+str(ww)+'\n'+str(wh), horizontalalignment='center', verticalalignment='center', fontsize=10, color='#800000')
                for line in lines:
                    lp, x = line
                    if i == lp:
                        plt.plot([x, x], [-25, dheight+25], color='red', linewidth=2)
                for sc in space:
                    sp, x1, x2 = sc
                    if i == sp:
                        plt.plot([x1+25, x2-25], [-25, -25], color='blue', linewidth=2)
                        ax.text((float(x2-x1)/2)+float(x1), -60, str(x2-x1), horizontalalignment='center', verticalalignment='center', color='blue')
                for mor in mor_list:
                    p, x, y, w, h, lab = mor
                    if i == p:
                        ax.text(x, y+h/2, str(h), horizontalalignment='right', verticalalignment='center', color='#386616', fontsize=10)
                        ax.text(x+w/2, y+h, str(w), horizontalalignment='center', verticalalignment='bottom', color='#386616', fontsize=10)
                        ax.text(x+w/2, y+h/2, lab, horizontalalignment='center', verticalalignment='center', fontsize=10)
                #    x, y, sew, seh, wd, ht = sec
                plt.xlim([0, dwidth])
                plt.ylim([-50, dheight+50])
                plt.gca().set_aspect('equal', adjustable='box')
                tit = '( C'+str(bid)+'_'+str(dwidth)+'_'+str(dheight)+' )  ' if bid != 0 else ''
                plt.title( tit + 'Vitre Claire 5 mm' + f' {i+1}')
                pdf.savefig(dpi=300, orientation='landscape')
                plt.close()
            d = pdf.infodict()
            d['Title'] = 'Impression de coupe'
            d['Author'] = 'RATSIMANANDOKA A. Idéalson'
            d['Subject'] = 'Impression coupe plateau vitre'
            d['CreationDate'] = datetime.datetime(2020, 10, 13)
            d['ModDate'] = datetime.datetime.today()

def cutline(nplans, mor, wast, dim):
    dwidth, dheight = dim
    seg = []
    cuts = []
    defcuts = []
    spacing = []
    for i in mor:
        p, x, y, width, height, rid = i
        seg.append((p, x, x+width))
        if y == 0 and x+width != dwidth:
            cuts.append((p, x+width))
    for i in wast:
        p, x, y, width, height = i
        seg.append((p, x, x+width))
        if y == 0 and x+width != dwidth:
            cuts.append((p, x+width))
    for cut in cuts:
        p, x = cut
        yr = True
        for se in seg:
            p2, x2, wd = se
            if p == p2:
                if x > x2 and x < wd:
                    yr = False
        if yr == True:
            defcuts.append(cut)
    for pl in range(nplans):
        inc = 0
        for cut in defcuts:
            p, x = cut
            if pl == p:
                spacing.append((p, inc, x))
                inc=x
    return defcuts, spacing

def parse_waste(waste, maxid):
    newaste = []
    for wst in waste:
        p, x, y, width, height = wst
        if (width >= 100 and height >= 290) or (width >= 290 and height >= 100):
            maxid += 1
            newaste.append((p, x, y, width, height, maxid))
    return newaste, maxid
     
def main():
        # Mettez les mesure en mm
        morceaux = [
                (772, 885,"SO18089\n772x885\nGinah"),
                (782, 895,"SO18089\n782x895\nGinah"),
                (430, 930,"01 SO18291\n430x930\nLandy"),
                (430, 930,"02 SO18291\n430x930\nLandy"),
                (610, 1750,"SO18204\n610x1750\nNicolas"),
                (990, 1993,"01 SO18204\n990x1993\nNicolas"),
                (990, 1993,"02 SO18204\n990x1993\nNicolas"),
                (886, 2015,"01 SO18204\n886x2015\nSarobidy"),
                (886, 2015,"02 SO18204\n886x2015\nSarobidy"),
                (886, 2015,"03 SO18204\n886x2015\nSarobidy"),
                (1175, 2015,"01 SO18204\n1175x2015\nSarobidy"),
                (1175, 2015,"02 SO18204\n1175x2015\nSarobidy"),
                (1175, 2015,"03 SO18204\n1175x2015\nSarobidy"),
                (1175, 2015,"04 SO18204\n1175x2015\nSarobidy"),
                (1175, 2015,"05 SO18204\n1175x2015\nSarobidy"),
                (1175, 2015,"06 SO18204\n1175x2015\nSarobidy"),
                (886, 1205,"01 SO18204\n886x1205\nSarobidy"),
                (886, 1205,"02 SO18204\n886x1205\nSarobidy"),
                (886, 1205,"03 SO18204\n886x1205\nSarobidy"),
                (1175, 1205,"01 SO18204\n1175x1205\nSarobidy"),
                (1175, 1205,"02 SO18204\n1175x1205\nSarobidy"),
                (1175, 1205,"03 SO18204\n1175x1205\nSarobidy"),
                (1175, 1205,"04 SO18204\n1175x1205\nSarobidy"),
                (1175, 1205,"05 SO18204\n1175x1205\nSarobidy"),
                (1175, 1205,"06 SO18204\n1175x1205\nSarobidy"),
                (910, 1205,"01/03 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"02/03 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"03/03 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"01/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"02/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"03/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"04/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"05/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"06/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"07/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"08/09 SO18204\n910x1205\nSarobidy"),
                (910, 1205,"09/09 SO18204\n910x1205\nSarobidy"),
                (910, 1086,"01/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"02/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"03/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"04/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"05/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"06/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"07/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"08/09 SO18204\n910x1086\nSarobidy"),
                (910, 1086,"09/09 SO18204\n910x1086\nSarobidy"),
                (760, 1885,"01 SO18204\n760x1885\nSarobidy"),
                (760, 1885,"02 SO18204\n760x1885\nSarobidy"),
                (760, 1885,"03 SO18204\n760x1885\nSarobidy")
                                ]
        plans = [
                (3300, 2140,100, 0)
                        ]
        nplans, mor_list, waste, empty, bin_lst = Solver2D(morceaux,plans)
        dim = (3300,2140)
        lines, space = cutline(nplans, mor_list, waste, dim)
        newaste, maxid = parse_waste(waste, 0)
        #Show2D(nplans, mor_list)
        PrintPDF2D(nplans, mor_list, waste, newaste, dim, bin_lst, lines, space)

if __name__ == '__main__':
    main()



            
