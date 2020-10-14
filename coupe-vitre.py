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
		packer.add_bin(*p)
	# Resoudre
	packer.pack()
	return (len(packer), packer.rect_list())

def Show2D(nplans, mor_list):
    for i in range(nplans):
        print(f"Feuille: {i+1}")
        fig = plt.figure()
        ax = fig.add_subplot()
        r = lambda: random.randint(25,210)
        ax.add_patch(matplotlib.patches.Rectangle((0,0), 6, 6, fill=None, hatch='///'))
        for mor in mor_list:
            p, x, y, w, h, lab = mor
            if i == p:
                print(f"    label:{lab}, x:{x}, y:{y}, largeur:{w}, hauteur:{h}")
                ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=True, color='#%02X%02X%02X' % (r(),r(),r())))
                ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=False))
                ax.text(x, y+h/2, str(h), horizontalalignment='left', verticalalignment='center')
                ax.text(x+w/2, y+h, str(w), horizontalalignment='center', verticalalignment='top')
                ax.text(x+w/2, y+h/2, lab, horizontalalignment='center', verticalalignment='center')
        plt.xlim([0, 6])
        plt.ylim([0, 6])
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show(block=False)

def PrintPDF2D(nplans, mor_list):
    with PdfPages('Impression.pdf') as pdf:
            for i in range(nplans):
                # A4 canvas
                fig_width_cm = 21
                fig_height_cm = 29.7
                inches_per_cm = 1 / 2.54
                fig_width = fig_width_cm * inches_per_cm
                fig_height = fig_height_cm * inches_per_cm
                fig_size = [fig_width, fig_height]

                plt.rc('text', usetex=False)
                fig = plt.figure()
                fig.set_size_inches(fig_size)
                ax = fig.add_subplot()
                r = lambda: random.randint(25,210)
                ax.add_patch(matplotlib.patches.Rectangle((0,0), 6, 6, fill=None, hatch='///'))
                for mor in mor_list:
                    p, x, y, w, h, lab = mor
                    if i == p:
                        ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=True, color='#%02X%02X%02X' % (r(),r(),r())))
                        ax.add_patch(matplotlib.patches.Rectangle((x,y), w, h, fill=False))
                        ax.text(x, y+h/2, str(h), horizontalalignment='left', verticalalignment='center')
                        ax.text(x+w/2, y+h, str(w), horizontalalignment='center', verticalalignment='top')
                        ax.text(x+w/2, y+h/2, lab, horizontalalignment='center', verticalalignment='center')
                plt.xlim([0, 6])
                plt.ylim([0, 6])
                plt.gca().set_aspect('equal', adjustable='box')
                plt.title(f'Page {i+1}')
                pdf.savefig(dpi=300, orientation='landscape')
                plt.close()
            d = pdf.infodict()
            d['Title'] = 'Impression de coupe'
            d['Author'] = 'RATSIMANANDOKA A. Idéalson'
            d['Subject'] = 'Impression coupe plateau vitre'
            d['CreationDate'] = datetime.datetime(2020, 10, 13)
            d['ModDate'] = datetime.datetime.today()
        
def main():
        # Mettez les mesure en mm
        morceaux = [ 
                (2, 2, '2x2'),
                (1, 3, '1x3'), 
                (4, 3, '4x3'), 
                (3, 1, '3x1'), 
                (3, 4, '3x4'), 
                (2, 2, '2x2')
                                ]
        plans = [
                (6, 6),
                (6, 6)
                        ]
        nplans, mor_list = Solver2D(morceaux,plans)
        Show2D(nplans, mor_list)
        PrintPDF2D(nplans, mor_list)

if __name__ == '__main__':
    main()



            
