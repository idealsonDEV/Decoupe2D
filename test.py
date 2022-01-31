from Rect2DPackLib import newPacker

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
                (6, 6),
                (6, 6)
                        ]
packer = newPacker()
# Ajouter à la fil des rectangle à placer
for r in morceaux:
	packer.add_rect(*r)
# Ajouter un plan
for p in plans:
	packer.add_bin(*p)
# Resoudre
packer.pack()
packer.rect_list()