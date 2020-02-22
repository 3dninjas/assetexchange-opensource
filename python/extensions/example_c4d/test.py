import c4d
from c4d import gui

def test():
    gui.MessageDialog('Hello World')

def test_mat(doc):
    doc.StartUndo()

    mat = c4d.BaseMaterial(c4d.Mmaterial)
    name = 'Import'
    mat.SetName(name)
    doc.InsertMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    doc.EndUndo()
    c4d.EventAdd()

