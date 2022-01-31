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
                (631, 777,"01/08\nFC2V"),
                (631, 777,"01/08\nFC2V"),
                (623.5, 777,"02/08\nFC2V"),
                (623.5, 777,"02/08\nFC2V"),
                (376, 777,"03/08\nFC2V"),
                (376, 777,"03/08\nFC2V"),
                (376, 777,"04/08\nFC2V"),
                (376, 777,"04/08\nFC2V"),
                (376, 777,"05/08\nFC2V"),
                (376, 777,"05/08\nFC2V"),
                (376, 777,"06/08\nFC2V"),
                (376, 777,"06/08\nFC2V"),
                (376, 777,"07/08\nFC2V"),
                (376, 777,"07/08\nFC2V"),
                (776, 897,"08/08\nFC2V"),
                (776, 897,"08/08\nFC2V"),
                (371, 742,"09/08\nFC2V"),
                (371, 742,"09/08\nFC2V"),
                (476, 897,"10/08\nFC2V"),
                (476, 897,"10/08\nFC2V"),
                (1045, 1595,"11/08\nFC3V_2/3"),
                (1045, 1595,"11/08\nFC3V_2/3"),
                (1045, 1595,"11/08\nFC3V_2/3"),
                (1095, 1595,"12/08\nFC3V_2/3"),
                (1095, 1595,"12/08\nFC3V_2/3"),
                (1095, 1595,"12/08\nFC3V_2/3"),
                (1065, 1595,"13/08\nFC3V_2/3"),
                (1065, 1595,"13/08\nFC3V_2/3"),
                (1065, 1595,"13/08\nFC3V_2/3"),
                (1073, 1595,"14/08\nFC3V_2/3"),
                (1073, 1595,"14/08\nFC3V_2/3"),
                (1073, 1595,"14/08\nFC3V_2/3"),
                (1080, 1595,"15/08\nFC3V_2/3"),
                (1080, 1595,"15/08\nFC3V_2/3"),
                (1080, 1595,"15/08\nFC3V_2/3"),
                (1060, 1595,"16/08\nFC3V_2/3"),
                (1060, 1595,"16/08\nFC3V_2/3"),
                (1060, 1595,"16/08\nFC3V_2/3"),
                (1065, 1595,"17/08\nFC3V_2/3"),
                (1065, 1595,"17/08\nFC3V_2/3"),
                (1065, 1595,"17/08\nFC3V_2/3"),
                (880, 1595,"18/08\nFC3V_2/3"),
                (880, 1595,"18/08\nFC3V_2/3"),
                (880, 1595,"18/08\nFC3V_2/3"),
                (935, 1595,"19/08\nFC3V_2/3"),
                (935, 1595,"19/08\nFC3V_2/3"),
                (935, 1595,"19/08\nFC3V_2/3"),
                (1073, 1595,"20/08\nFC3V_2/3"),
                (1073, 1595,"20/08\nFC3V_2/3"),
                (1073, 1595,"20/08\nFC3V_2/3"),
                (1065, 1595,"21/08\nFC3V_2/3"),
                (1065, 1595,"21/08\nFC3V_2/3"),
                (1065, 1595,"21/08\nFC3V_2/3"),
                (840, 441,"22/08\nPO1V"),
                (819, 441,"22/08\nPO1V"),
                (1088, 1946,"23/08\nPC2V"),
                (1088, 1946,"23/08\nPC2V"),
                (743, 1821,"24/08\nPC2V"),
                (743, 1821,"24/08\nPC2V"),
                (855.5, 1766,"25/08\nPC2V"),
                (855.5, 1766,"25/08\nPC2V"),
                (848, 1766,"26/08\nPC2V"),
                (848, 1766,"26/08\nPC2V"),
                (740, 1819,"27/08\nPC2V"),
                (740, 1819,"27/08\nPC2V"),
                (1093, 1866,"28/08\nPC2V"),
                (1093, 1866,"28/08\nPC2V"),
                (1009, 1007,"29/08\nPO2V"),
                (1009, 1007,"29/08\nPO2V"),
                (310, 495,"30/08\nFIX"),
                (310, 495,"31/08\nFIX"),
                (212, 1152,"32/08\nFIX_2DIV"),
                (212, 1152,"32/08\nFIX_2DIV"),
                (765, 1120,"33/08\nFIX_3DIV"),
                (765, 1120,"33/08\nFIX_3DIV"),
                (765, 1120,"33/08\nFIX_3DIV"),
                (765, 1085,"34/08\nFIX_3DIV"),
                (765, 1085,"34/08\nFIX_3DIV"),
                (765, 1085,"34/08\nFIX_3DIV"),
                (765, 1105,"35/08\nFIX_3DIV"),
                (765, 1105,"35/08\nFIX_3DIV"),
                (765, 1105,"35/08\nFIX_3DIV"),
                (765, 1113,"36/08\nFIX_3DIV"),
                (765, 1113,"36/08\nFIX_3DIV"),
                (765, 1113,"36/08\nFIX_3DIV"),
                (765, 1100,"37/08\nFIX_3DIV"),
                (765, 1100,"37/08\nFIX_3DIV"),
                (765, 1100,"37/08\nFIX_3DIV"),
                (765, 920,"38/08\nFIX_3DIV"),
                (765, 920,"38/08\nFIX_3DIV"),
                (765, 920,"38/08\nFIX_3DIV"),
                (765, 975,"39/08\nFIX_3DIV"),
                (765, 975,"39/08\nFIX_3DIV"),
                (765, 975,"39/08\nFIX_3DIV"),
                (765, 1113,"40/08\nFIX_3DIV"),
                (765, 1113,"40/08\nFIX_3DIV"),
                (765, 1113,"40/08\nFIX_3DIV"),
                (765, 1105,"41/08\nFIX_3DIV"),
                (765, 1105,"41/08\nFIX_3DIV"),
                (765, 1105,"41/08\nFIX_3DIV"),
                (332, 307,"42/08\nSoufflet"),
                (332, 302,"43/08\nSoufflet"),
                (332, 287,"44/08\nSoufflet"),
                (334, 297,"45/08\nSoufflet"),
                (347, 302,"46/08\nSoufflet"),
                (327, 277,"47/08\nSoufflet"),
                                ]
        plans = [
                (1175, 125, 1, 1),
                (1175, 125, 1, 2),
                (886, 125, 1, 3),
                (1175, 125, 1, 4),
                (1175, 125, 1, 5),
                (886, 125, 1, 6),
                (1175, 125, 1, 7),
                (1175, 125, 1, 8),
                (886, 125, 1, 9),
                (990, 147, 1, 10),
                (990, 147, 1, 11),
                (760, 255, 1, 12),
                (560, 2140, 1, 13),
                (1520, 255, 1, 14),
                (605, 2140, 1, 15),
                (910, 935, 1, 18),
                (910, 935, 1, 19),
                (305, 2140, 1, 20),
                (910, 935, 1, 21),
                (910, 935, 1, 22),
                (570, 2140, 1, 24),
                (570, 2140, 1, 28),
                (594, 2140, 1, 31),
                (104, 895, 1, 32),
                (601, 390, 1, 33),
                (910, 1054, 1, 34),
                (114, 885, 1, 35),
                (910, 1054, 1, 36),
                (910, 1054, 1, 37),
                (1480, 2140, 1, 38),
                (3300, 2140,100, 0)
                        ]
        s_plans = sorted(plans, reverse=False,key=lambda r: r[0]*r[1])
        nplans, mor_list, waste, empty, bin_lst = Solver2D(morceaux,s_plans)
        dim = (3300,2140)
        lines, space = cutline(nplans, mor_list, waste, dim)
        newaste, maxid = parse_waste(waste, 38)
        #Show2D(nplans, mor_list)
        PrintPDF2D(nplans, mor_list, waste, newaste, dim, bin_lst, lines, space)

if __name__ == '__main__':
    main()



            
