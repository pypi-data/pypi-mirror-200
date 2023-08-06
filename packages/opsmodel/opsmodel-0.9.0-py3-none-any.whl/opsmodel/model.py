import numpy as np
import copy
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os
import pandas as pd
import numbers

tolerance = 1e-10
ndm = 3

class Model:
    def __init__(self, name=''):
        self.Name = name
        self.Members = []
        self.NodalLoads = []
        self.LineUniLoads = []
        self.QuadUniLoads = []
        self.BodyLoads = []
        self.SurfLoads = []
        self.NodalMasses = []
        self.SpConstraints = []
        self.EqualDofs = []
        self.RigidDiaphragms = []
        self.RigidLinks = []

    def addmember(self, member):
        members = self.Members
        members.append(member)

    def removemember(self,member):
        members = self.Members
        members.remove(member)

    def assign_nodeload(self, pattern, xyz, vals):
        noloads = self.NodalLoads
        noloads.append([pattern, xyz, vals])

    def assign_nodalmass(self, xyz, vals):
        nomasses = self.NodalMasses
        nomasses.append([xyz, vals])

    def assign_spconstraint(self, xlim=[], ylim=[], zlim=[], constrValues=[]):
        spconsts = self.SpConstraints
        spconsts.append([xlim, ylim, zlim, constrValues])

    def assign_equaldof(self,xyzr, xclim=[], yclim=[], zclim=[], dofs=[]):
        eqdofs = self.EqualDofs
        eqdofs.append([xyzr, xclim, yclim, zclim, dofs])

    def assign_rigiddiaphragm(self, xyzr, perpdirn=2, xclim=[], yclim=[], zclim=[], massr=[], rests=[2, 4, 6]):
        rgdiaphs = self.RigidDiaphragms
        rgdiaphs.append([xyzr, perpdirn, xclim, yclim, zclim, massr, rests])

    def assign_rigidlink(self, xyzr, type='beam', xclim=[], yclim=[], zclim=[]):
        rglinks = self.RigidLinks
        rglinks.append([xyzr, type, xclim, yclim, zclim])

    def getNodes(self):
        model_nodes = {}
        for m in self.Members:
            model_nodes.update( m.Nodes)

        return model_nodes

    def getElements(self):
        model_elements = {}
        for m in self.Members:
            model_elements.update(m.Elements)

        return model_elements

def replicate_linear(model, number, dx, dy, dz):
    allnewmembers = []
    newmodel = Model()
    for m in model.Members:
        newmembers = m.replicate_linear(number, dx, dy, dz)
        allnewmembers.extend(newmembers)

    for newm in allnewmembers:
            newmodel.addmember(newm)

    return newmodel

def replicate_mirror(model, xyz1, xyz2, xyz3):
    allnewmembers=[]
    newmodel = Model()
    for m in model.Members:
        newmembers = m.replicate_mirror(xyz1, xyz2, xyz3)
        allnewmembers.append(newmembers)

    for newm in allnewmembers:
            newmodel.addmember(newm)

    return newmodel

def replicate_rotate(model, number, xyz1, xyz2, teta):
    allnewmembers=[]
    newmodel = Model()
    for m in model.Members:
        newmembers = m.replicate_rotate(number, xyz1, xyz2, teta)
        allnewmembers.extend(newmembers)

    for newm in allnewmembers:
            newmodel.addmember(newm)

    return newmodel

def mergemodels(model1, model2):
    for m in model2.Members:
        model1.addmember(m)

def plotmodel(model, ax, name='n', propname='y', subdivisions='y', linewidth=0.2, edgelinewidth=0.2, fill='y', coloring='default',
               fontsize=3, xlim=[], ylim=[], zlim=[], facenumber='n',alpha=0.5):
    for member in model.Members:
        plotmember(ax, member, name, propname, subdivisions, linewidth, edgelinewidth, fill, coloring,
               fontsize, xlim, ylim, zlim, facenumber,alpha)


def assemble(*submodels):
    mainmodel = Model()
    for m in submodels:
        for memb in m.Members:
            mainmodel.addmember(memb)

        for loads in m.NodalLoads:
            mainmodel.assign_nodeload(loads)

        for spconsts in m.SpConstraints:
            mainmodel.assign_spconstraint(spconsts)

        for mpconsts in m.EqualDofs:
            mainmodel.assign_equaldof(mpconsts)

        for mpconsts in m.RigidDiaphragms:
            mainmodel.assign_rigiddiaphragm(mpconsts)

        for mpconsts in m.RigidLinks:
            mainmodel.assign_rigidlink(mpconsts)

        for mass in m.NodalMasses:
            mainmodel.assign_nodalmass(mass)

    return mainmodel

class Brick:
    def __init__(self, name, eleProps, xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8, N12=5, N14=5, N15=5, attach='y'):
        self.Name = name
        self.EleProps = eleProps
        self.XYZ1 = xyz1
        self.XYZ2 = xyz2
        self.XYZ3 = xyz3
        self.XYZ4 = xyz4
        self.XYZ5 = xyz5
        self.XYZ6 = xyz6
        self.XYZ7 = xyz7
        self.XYZ8 = xyz8
        self.N12 = N12
        self.N14 = N14
        self.N15 = N15
        self.Attach = attach
        self.Surfload = []
        self.Bodyload = []
        self.NodeSets = {1: {'Nodes': [],
                          'ij': [],
                          'jk': [],
                          'kl': [],
                          'li': []
                          },
                          2: {'Nodes': [],
                          'ij': [],
                          'jk': [],
                          'kl': [],
                          'li': []
                          },
                          3: {'Nodes': [],
                          'ij': [],
                          'jk': [],
                          'kl': [],
                          'li': []
                          },
                          4: {'Nodes': [],
                          'ij': [],
                          'jk': [],
                          'kl': [],
                          'li': []
                          },
                          5: {'Nodes': [],
                          'ij': [],
                          'jk': [],
                          'kl': [],
                          'li': []
                          },
                          6: {'Nodes': [],
                          'ij': [],
                          'jk': [],
                          'kl': [],
                          'li': []
                          }
               }
        self.Nodes = {}
        self.Elements = {}
    ###### validation VBlock ( Set and Get Properties ) ########################
    def __get_name(self):
            return self._Name

    def __set_name(self, name):

        if type(name) is not str:
            raise ValueError("name must be string")
        self._Name = name

    def __del_name(self):
        del self._Name

    Name = property(__get_name, __set_name, __del_name)

    # XYZ1
    def __get_XYZ1(self):
        return self._XYZ1

    def __set_XYZ1(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ1 = value

    def __del_XYZ1(self):
        del self._XYZ1

    XYZ1 = property(__get_XYZ1, __set_XYZ1, __del_XYZ1)

    # XYZ2
    def __get_XYZ2(self):
        return self._XYZ2

    def __set_XYZ2(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ2 = value

    def __del_XYZ2(self):
        del self._XYZ2

    XYZ2 = property(__get_XYZ2, __set_XYZ2, __del_XYZ2)

    # XYZ3
    def __get_XYZ3(self):
        return self._XYZ3

    def __set_XYZ3(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ3 = value

    def __del_XYZ3(self):
        del self._XYZ3

    XYZ3 = property(__get_XYZ3, __set_XYZ3, __del_XYZ3)

    # XYZ4
    def __get_XYZ4(self):
        return self._XYZ4

    def __set_XYZ4(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ4 = value

    def __del_XYZ4(self):
        del self._XYZ4

    XYZ4 = property(__get_XYZ4, __set_XYZ4, __del_XYZ4)

    # XYZ5
    def __get_XYZ5(self):
        return self._XYZ5

    def __set_XYZ5(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ5 = value

    def __del_XYZ5(self):
        del self._XYZ5

    XYZ5 = property(__get_XYZ5, __set_XYZ5, __del_XYZ5)

    # XYZ6
    def __get_XYZ6(self):
        return self._XYZ6

    def __set_XYZ6(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ6 = value

    def __del_XYZ6(self):
        del self._XYZ6

    XYZ6 = property(__get_XYZ6, __set_XYZ6, __del_XYZ6)

    # XYZ7
    def __get_XYZ7(self):
        return self._XYZ7

    def __set_XYZ7(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ7 = value

    def __del_XYZ7(self):
        del self._XYZ7

    XYZ7 = property(__get_XYZ7, __set_XYZ7, __del_XYZ7)

    # XYZ8
    def __get_XYZ8(self):
        return self._XYZ8

    def __set_XYZ8(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ8 = value

    def __del_XYZ8(self):
        del self._XYZ8

    XYZ8 = property(__get_XYZ8, __set_XYZ8, __del_XYZ8)

    # N12 Validation
    def __get_N12(self):
        return self._N12

    def __set_N12(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._N12 = val

    def __del_N12(self):
        del self._N12

    N12 = property(__get_N12, __set_N12, __del_N12)

    # N14 Validation
    def __get_N14(self):
        return self._N14

    def __set_N14(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._N14 = val

    def __del_N14(self):
        del self._N14

    N14 = property(__get_N14, __set_N14, __del_N14)

    # N15 Validation
    def __get_N15(self):
        return self._N15

    def __set_N15(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._N15 = val

    def __del_N15(self):
        del self._N15

    N15 = property(__get_N15, __set_N15, __del_N15)

    # EleProps Validation
    def __get_EleProps(self):
        return self._EleProps

    def __set_EleProps(self, value):
        if type(value) != dict:
            raise ValueError('eleProps must be a python dictionary')

        self._EleProps = value

    def __del_EleProps(self):
        del self._EleProps

    EleProps = property(__get_EleProps, __set_EleProps, __del_EleProps)

    ## End of validation

    ###### loading ########################
    def assign_surfload(self, pattern, face, value, direction=2):
        if face not in [1, 2, 3, 4, 5, 6]:
            raise ValueError('face must be one of 1, 2, 3, 4, 5 or 6')

        if isinstance(value, numbers.Number) == False:
            raise ValueError('value must be a numeric value')

        if direction not in [1, 2, 3]:
            raise ValueError('direction must be one of 1, 2 or 3')

        uniloads = self.Surfload
        uniloads.append([pattern, face, value, direction])

    def assign_bodyload(self, pattern, value, direction=2):
        if isinstance(value, numbers.Number) == False:
            raise ValueError('value must be a numeric value')

        if direction not in [1, 2, 3]:
            raise ValueError('direction must be one of 1, 2 or 3')
        bodloads = self.Bodyload
        bodloads.append([pattern, value, direction])

    ###### linear replicate ########################
    def replicate_linear(self, number, dx, dy, dz):
        if type(number) != int:
            raise ValueError("Number of replications must be positive integer value")

        if number <= 0:
            raise ValueError("Number of replications must be positive integer value")

        if isinstance(dx, numbers.Number) == False:
            raise ValueError('dx must be a numeric value')

        if isinstance(dy, numbers.Number) == False:
            raise ValueError('dy must be a numeric value')

        if isinstance(dz, numbers.Number) == False:
            raise ValueError('dz must be a numeric value')

        newmembers = []
        name = self.Name
        x1, y1, z1 = self.XYZ1
        x2, y2, z2 = self.XYZ2
        x3, y3, z3 = self.XYZ3
        x4, y4, z4 = self.XYZ4
        x5, y5, z5 = self.XYZ5
        x6, y6, z6 = self.XYZ6
        x7, y7, z7 = self.XYZ7
        x8, y8, z8 = self.XYZ8
        for i in range(number):
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newx1, newy1, newz1 = x1 + (i + 1) * dx, y1 + (i + 1) * dy, z1 + (i + 1) * dz
            newx2, newy2, newz2 = x2 + (i + 1) * dx, y2 + (i + 1) * dy, z2 + (i + 1) * dz
            newx3, newy3, newz3 = x3 + (i + 1) * dx, y3 + (i + 1) * dy, z3 + (i + 1) * dz
            newx4, newy4, newz4 = x4 + (i + 1) * dx, y4 + (i + 1) * dy, z4 + (i + 1) * dz
            newx5, newy5, newz5 = x5 + (i + 1) * dx, y5 + (i + 1) * dy, z5 + (i + 1) * dz
            newx6, newy6, newz6 = x6 + (i + 1) * dx, y6 + (i + 1) * dy, z6 + (i + 1) * dz
            newx7, newy7, newz7 = x7 + (i + 1) * dx, y7 + (i + 1) * dy, z7 + (i + 1) * dz
            newx8, newy8, newz8 = x8 + (i + 1) * dx, y8 + (i + 1) * dy, z8 + (i + 1) * dz
            newmember.XYZ1 = [newx1, newy1, newz1]
            newmember.XYZ2 = [newx2, newy2, newz2]
            newmember.XYZ3 = [newx3, newy3, newz3]
            newmember.XYZ4 = [newx4, newy4, newz4]
            newmember.XYZ5 = [newx5, newy5, newz5]
            newmember.XYZ6 = [newx6, newy6, newz6]
            newmember.XYZ7 = [newx7, newy7, newz7]
            newmember.XYZ8 = [newx8, newy8, newz8]

            newmember.Name = newname
            newmembers.append(newmember)
        return newmembers

    ###### replicate mirror ########################
    def replicate_mirror(self, xyz1, xyz2, xyz3):
        name = self.Name
        newname = name + "_mir"
        newmember = copy.deepcopy(self)
        newmember.XYZ1 = MyMath.mirrorpoint(self.XYZ1, xyz1, xyz2, xyz3)
        newmember.XYZ2 = MyMath.mirrorpoint(self.XYZ2, xyz1, xyz2, xyz3)
        newmember.XYZ3 = MyMath.mirrorpoint(self.XYZ3, xyz1, xyz2, xyz3)
        newmember.XYZ4 = MyMath.mirrorpoint(self.XYZ4, xyz1, xyz2, xyz3)
        newmember.XYZ5 = MyMath.mirrorpoint(self.XYZ5, xyz1, xyz2, xyz3)
        newmember.XYZ6 = MyMath.mirrorpoint(self.XYZ6, xyz1, xyz2, xyz3)
        newmember.XYZ7 = MyMath.mirrorpoint(self.XYZ7, xyz1, xyz2, xyz3)
        newmember.XYZ8 = MyMath.mirrorpoint(self.XYZ8, xyz1, xyz2, xyz3)
        newmember.Name = newname
        return newmember

    ###### replicate rotate ########################
    def replicate_rotate(self, number, xyz1, xyz2, teta):
        newmembers = []
        name = self.Name
        for i in range(number):
            rot_t = teta * (i + 1)
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newmember.XYZ1 = MyMath.rotatepoint(self.XYZ1, xyz1, xyz2, rot_t)
            newmember.XYZ2 = MyMath.rotatepoint(self.XYZ2, xyz1, xyz2, rot_t)
            newmember.XYZ3 = MyMath.rotatepoint(self.XYZ3, xyz1, xyz2, rot_t)
            newmember.XYZ4 = MyMath.rotatepoint(self.XYZ4, xyz1, xyz2, rot_t)
            newmember.XYZ5 = MyMath.rotatepoint(self.XYZ5, xyz1, xyz2, rot_t)
            newmember.XYZ6 = MyMath.rotatepoint(self.XYZ6, xyz1, xyz2, rot_t)
            newmember.XYZ7 = MyMath.rotatepoint(self.XYZ7, xyz1, xyz2, rot_t)
            newmember.XYZ8 = MyMath.rotatepoint(self.XYZ8, xyz1, xyz2, rot_t)
            newmember.Name = newname
            newmembers.append(newmember)
        return newmembers

    ###### Create Elements ########################

    def createelements(self):
        global ndm
        eleProps = self.EleProps
        xyz1 = self.XYZ1
        xyz2 = self.XYZ2
        xyz3 = self.XYZ3
        xyz4 = self.XYZ4
        xyz5 = self.XYZ5
        xyz6 = self.XYZ6
        xyz7 = self.XYZ7
        xyz8 = self.XYZ8
        N12 = self.N12
        N14 = self.N14
        N15 = self.N15

        xyz = [xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8]

        if ndm == 3:
            for xyzi in xyz:
                if len(xyzi) != 3:
                    raise ValueError("ndm = 3: xyz should be a list contains coordinates [x, y, z]")
        else:
            for xyzi in xyz:
                if len(xyzi) < 2:
                    raise ValueError("ndm = 2: xyz should be a list contains coordinates [x, y]")

            xyz1 = [xyz1[0], xyz1[1], 0]
            xyz2 = [xyz2[0], xyz2[1], 0]
            xyz3 = [xyz3[0], xyz3[1], 0]
            xyz4 = [xyz4[0], xyz4[1], 0]
            xyz5 = [xyz5[0], xyz5[1], 0]
            xyz6 = [xyz6[0], xyz6[1], 0]
            xyz7 = [xyz7[0], xyz7[1], 0]
            xyz8 = [xyz8[0], xyz8[1], 0]

        coords, Noderange, Nodes = MyMath.dividecube(xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8, N12, N14, N15)

        edgeNodes = MyMath.extractbricknodesets(Noderange)
        Elements = MyMath.extractbrickelements(coords, N12, N14)

        return Nodes, Elements, edgeNodes

class Polygon:
    def __init__(self, name, eleProps, xyz, Ndiv=4, attach='y'):
        self.Name = name
        self.EleProps = eleProps
        self.XYZ = xyz
        self.NDiv = Ndiv
        self.Attach = attach
        self.Uniload = []
        self.NodeSets = {}
        self.Nodes = {}
        self.Elements = {}
    ###### validation VBlock ( Set and Get Properties ) ########################
    def __get_name(self):
            return self._Name

    def __set_name(self, name):
        if type(name) is not str:
            raise ValueError("name must be string")
        self._Name = name

    def __del_name(self):
        del self._Name

    Name = property(__get_name, __set_name, __del_name)

    # XYZ
    def __get_XYZ(self):
        return self._XYZ

    def __set_XYZ(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ = value

    def __del_XYZ(self):
        del self._XYZ

    XYZ = property(__get_XYZ, __set_XYZ, __del_XYZ)


    # NDiv Validation
    def __get_NDiv(self):
        return self._NDiv

    def __set_NDiv(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._NDiv = val

    def __del_NDiv(self):
        del self._NDiv

    NDiv = property(__get_NDiv, __set_NDiv, __del_NDiv)

    # EleProps Validation
    def __get_EleProps(self):
        return self._EleProps

    def __set_EleProps(self, value):
        if type(value) != dict:
            raise ValueError('eleProps must be a python dictionary')

        self._EleProps = value

    def __del_EleProps(self):
        del self._EleProps

    EleProps = property(__get_EleProps, __set_EleProps, __del_EleProps)

    ## End of validation

    ###### loading ########################
    def assign_uniload(self, pattern, value, direction=2):
        if isinstance(value, numbers.Number) == False:
            raise ValueError('value must be a numeric value')

        if direction not in [1, 2, 3]:
            raise ValueError('direction must be one of 1, 2 or 3')
        uniloads = self.Uniload
        uniloads.append([pattern, value, direction])

    ###### linear replicate ########################
    def replicate_linear(self, number, dx, dy, dz):
        if (type(number) != int):
            raise ValueError("Number of replications must be positive integer value")

        if (number <= 0):
            raise ValueError("Number of replications must be positive integer value")

        if isinstance(dx, numbers.Number) == False :
            raise ValueError('dx must be a numeric value')

        if isinstance(dy, numbers.Number) == False:
            raise ValueError('dy must be a numeric value')

        if isinstance(dz, numbers.Number) == False:
            raise ValueError('dz must be a numeric value')

        newmembers = []
        name = self.Name
        xyz = self.XYZ
        for i in range(number):
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            xyznew = []
            for j in range(len(xyz)):
                newxi, newyi, newzi = xyz[j][0] + (i + 1) * dx, xyz[j][1] + (i + 1) * dy, xyz[j][2]  + (i + 1) * dz
                xyznew.append([newxi, newyi, newzi])

            newmember.XYZ = xyznew
            newmember.Name = newname
            newmembers.append(newmember)

        return newmembers

    ###### replicate mirror ########################
    def replicate_mirror(self, xyz1, xyz2, xyz3):
        name = self.Name
        newname = name + "_mir"
        xyz = self.XYZ
        newmember = copy.deepcopy(self)
        xyznew = []

        for j in range(len(xyz)):
            newxyz = MyMath.mirrorpoint(xyz[j], xyz1, xyz2, xyz3)
            xyznew.append(newxyz)

        newmember.XYZ = xyznew
        newmember.Name = newname
        return newmember

    ###### replicate rotate ########################
    def replicate_rotate(self, number, xyz1, xyz2, teta):
        newmembers = []
        name = self.Name
        xyz = self.XYZ
        for i in range(number):
            rot_t = teta * (i + 1)
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            xyznew = []
            for j in range(len(xyz)):
                newxyz = MyMath.rotatepoint(xyz[j], xyz1, xyz2, rot_t)
                xyznew.append(newxyz)
            newmember.Name = newname
            newmember.XYZ = xyznew
            newmembers.append(newmember)

        return newmembers
    def __createmembers(self):
        members = []
        xyz = self.XYZ
        if len(xyz) == 1:
            pass
        elif len(xyz) == 2:
            pass
        elif len(xyz) == 3:
            members.append(Triangle(self.Name, self.EleProps, xyz[0], xyz[1], xyz[2], Ndiv=self.NDiv,
                                attach=self.Attach))
        elif len(xyz) == 4:
            members.append(Quad(self.Name,self.EleProps,xyz[0], xyz[1], xyz[2], xyz[3], Nij=self.NDiv,
                                Njk=self.NDiv,attach=self.Attach))
        else:
            node_tags = list(np.linspace(1, len(xyz), len(xyz), dtype=int))

            nodenum = len(node_tags)
            while nodenum > 4:
                a = [node_tags[0]-1, node_tags[1]-1, node_tags[-2]-1, node_tags[-1]-1]
                members.append(Quad(self.Name, self.EleProps, xyz[a[0]], xyz[a[1]], xyz[a[2]], xyz[a[3]], Nij=self.NDiv,
                                    Njk=self.NDiv, attach=self.Attach))
                node_tags.remove(node_tags[0])
                node_tags.remove(node_tags[-1])
                nodenum = len(node_tags)

            if nodenum == 3:
                members.append(Triangle(self.Name, self.EleProps, xyz[node_tags[0]-1], xyz[node_tags[1]-1],
                                        xyz[node_tags[2]-1], Ndiv=self.NDiv, attach=self.Attach))
            elif nodenum == 4:

                members.append(Quad(self.Name, self.EleProps, xyz[node_tags[0]-1], xyz[node_tags[1]-1], xyz[node_tags[2]-1],
                                    xyz[node_tags[3]-1], Nij=self.NDiv, Njk=self.NDiv, attach=self.Attach))

        return members

    def createelements(self):
        n = len(self.XYZ)
        members = self.__createmembers()
        members2 = []
        Elements = {}
        Nodes = {}
        edgeNodes = []

        if len(members) == 1:
                Nodes, Elements, edgeNodes = members[0].createelements()
        else:
            elecount = 0
            nodecount = 0

            for m in members:
                mnodes, melements, medgenodes = m.createelements()
                mnodes2={}
                melements2 = {}
                medgenodes2 = []
                for el in melements.keys():
                    elenodes = melements[el]
                    nodetags = [x + nodecount for x in elenodes]
                    eletag = el + elecount
                    melements2[eletag] = nodetags

                for no in mnodes.keys():
                    xyz_n = mnodes[no]
                    nodetag = no + nodecount
                    mnodes2[nodetag] = xyz_n

                for i in range(len(medgenodes)):
                    nodetags = [x + nodecount for x in medgenodes[i]]
                    medgenodes2.append(nodetags)

                elecount = max(melements2.keys())
                nodecount = max(mnodes2.keys())

                members2.append([mnodes2, melements2, medgenodes2])

            edgenodes_temp = [[]] * n

            for i in range(len(members2) - 1):
                mnodes_1, melements_1, medgenodes_1 = members2[i]
                edgenodes_temp[i] = medgenodes_1[0]
                edgenodes_temp[n-i-2] = medgenodes_1[2]
                if i == 0:
                    edgenodes_temp[-1] = medgenodes_1[-1]

            mnodes_1, melements_1, medgenodes_1 = members2[-1]
            if len(medgenodes_1) == 4:
                edgenodes_temp[int(n/2 - 2)] = medgenodes_1[0]
                edgenodes_temp[int(n / 2 - 1)] = medgenodes_1[1]
                edgenodes_temp[int(n / 2)] = medgenodes_1[2]

            elif len(medgenodes_1) == 3:
                m = (n+1) / 2
                edgenodes_temp[int(m - 2)] = medgenodes_1[0]
                edgenodes_temp[int(m - 1)] = medgenodes_1[1]


            for i in range(len(members2) - 1):
                mnodes_1, melements_1, medgenodes_1 = members2[i]
                mnodes_2, melements_2, medgenodes_2 = members2[i + 1]
                repnodes_1 = medgenodes_1[1]
                repnodes_2 = medgenodes_2[-1]
                repnodes_2.reverse()

                for ke in list(melements_2.keys()):
                    for j in range(len(repnodes_1)):
                        for k in range(len(melements_2[ke])):
                            if melements_2[ke][k] == repnodes_2[j]:
                                melements_2[ke][k] = repnodes_1[j]

                for nod in repnodes_2:
                    mnodes_2.pop(nod)

                for nod in mnodes_1.keys():
                    Nodes[nod] = mnodes_1[nod]

                for nod in mnodes_2.keys():
                    Nodes[nod] = mnodes_2[nod]

                for j in range(len(repnodes_1)):
                    for l in range(len(edgenodes_temp)):
                        for k in range(len(edgenodes_temp[l])):
                            if edgenodes_temp[l][k] == repnodes_2[j]:
                                edgenodes_temp[l][k] = repnodes_1[j]

                Elements.update(melements_1)
                Elements.update(melements_2)

            edgeNodes = edgenodes_temp

        return Nodes, Elements, edgeNodes

class Quad:
    def __init__(self, name, eleProps, xyzi, xyzj, xyzk, xyzl, Nij=5, Njk=5, attach='y'):
        self.Name = name
        self.EleProps = eleProps
        self.XYZi = xyzi
        self.XYZj = xyzj
        self.XYZk = xyzk
        self.XYZl = xyzl
        self.Nij = Nij
        self.Njk = Njk
        self.Attach = attach
        self.Uniload = []
        self.NodeSets = {'ij': [],'jk': [],'kl': [],'li': []}
        self.Nodes = {}
        self.Elements = {}
    ###### validation VBlock ( Set and Get Properties ) ########################
    def __get_name(self):
            return self._Name

    def __set_name(self, name):
        if type(name) is not str:
            raise ValueError("name must be string")
        self._Name = name

    def __del_name(self):
        del self._Name

    Name = property(__get_name, __set_name, __del_name)

    # XYZi
    def __get_XYZi(self):
        return self._XYZi

    def __set_XYZi(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZi = value

    def __del_XYZi(self):
        del self._XYZi

    XYZi = property(__get_XYZi, __set_XYZi, __del_XYZi)

    # XYZj
    def __get_XYZj(self):
        return self._XYZj

    def __set_XYZj(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZj = value

    def __del_XYZj(self):
        del self._XYZj

    XYZj = property(__get_XYZj, __set_XYZj, __del_XYZj)

    # XYZk
    def __get_XYZk(self):
        return self._XYZk

    def __set_XYZk(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZk = value

    def __del_XYZk(self):
        del self._XYZk

    XYZk = property(__get_XYZk, __set_XYZk, __del_XYZk)

    # XYZl
    def __get_XYZl(self):
        return self._XYZl

    def __set_XYZl(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZl = value

    def __del_XYZl(self):
        del self._XYZl

    XYZl = property(__get_XYZl, __set_XYZl, __del_XYZl)


    # Nij Validation
    def __get_Nij(self):
        return self._Nij

    def __set_Nij(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._Nij = val

    def __del_Nij(self):
        del self._Nij

    Nij = property(__get_Nij, __set_Nij, __del_Nij)


    # Njk Validation
    def __get_Njk(self):
        return self._Njk

    def __set_Njk(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._Njk = val

    def __del_Njk(self):
        del self._Njk

    Njk = property(__get_Njk, __set_Njk, __del_Njk)

    # EleProps Validation
    def __get_EleProps(self):
        return self._EleProps

    def __set_EleProps(self, value):
        if type(value) != dict:
            raise ValueError('eleProps must be a python dictionary')


        self._EleProps = value

    def __del_EleProps(self):
        del self._EleProps

    EleProps = property(__get_EleProps, __set_EleProps, __del_EleProps)

    ## End of validation

    ###### loading ########################
    def assign_uniload(self, pattern, value, direction=2):
        if isinstance(value, numbers.Number) == False:
            raise ValueError('value must be a numeric value')

        if direction not in [1, 2, 3]:
            raise ValueError('direction must be one of 1, 2 or 3')
        uniloads = self.Uniload
        uniloads.append([pattern, value, direction])

    ###### linear replicate ########################
    def replicate_linear(self, number, dx, dy, dz):
        if (type(number) != int):
            raise ValueError("Number of replications must be positive integer value")

        if (number <= 0):
            raise ValueError("Number of replications must be positive integer value")

        if isinstance(dx, numbers.Number) == False :
            raise ValueError('dx must be a numeric value')

        if isinstance(dy, numbers.Number) == False:
            raise ValueError('dy must be a numeric value')

        if isinstance(dz, numbers.Number) == False:
            raise ValueError('dz must be a numeric value')

        newmembers = []
        name = self.Name
        xi, yi, zi = self.XYZi
        xj, yj, zj = self.XYZj
        xk, yk, zk = self.XYZk
        xl, yl, zl = self.XYZl
        for i in range(number):
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newxi, newyi, newzi  = xi + (i + 1) * dx, yi + (i + 1) * dy, zi + (i + 1) * dz
            newxj, newyj, newzj = xj + (i + 1) * dx, yj + (i + 1) * dy, zj + (i + 1) * dz
            newxk, newyk, newzk = xk + (i + 1) * dx, yk + (i + 1) * dy, zk + (i + 1) * dz
            newxl, newyl, newzl = xl + (i + 1) * dx, yl + (i + 1) * dy, zl + (i + 1) * dz
            newmember.XYZi = [newxi, newyi, newzi]
            newmember.XYZj = [newxj, newyj, newzj]
            newmember.XYZk = [newxk, newyk, newzk]
            newmember.XYZl = [newxl, newyl, newzl]
            newmember.Name = newname
            newmembers.append(newmember)
        return newmembers

    ###### replicate mirror ########################
    def replicate_mirror(self, xyz1, xyz2, xyz3):
        name = self.Name
        newname = name + "_mir"
        newmember = copy.deepcopy(self)
        newmember.XYZi = MyMath.mirrorpoint(self.XYZi, xyz1, xyz2, xyz3)
        newmember.XYZj = MyMath.mirrorpoint(self.XYZj, xyz1, xyz2, xyz3)
        newmember.XYZk = MyMath.mirrorpoint(self.XYZk, xyz1, xyz2, xyz3)
        newmember.XYZl = MyMath.mirrorpoint(self.XYZl, xyz1, xyz2, xyz3)
        newmember.Name = newname
        return newmember

    ###### replicate rotate ########################
    def replicate_rotate(self, number, xyz1, xyz2, teta):
        newmembers = []
        name = self.Name
        for i in range(number):
            rot_t = teta * (i + 1)
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newmember.XYZi = MyMath.rotatepoint(self.XYZi, xyz1, xyz2, rot_t)
            newmember.XYZj = MyMath.rotatepoint(self.XYZj, xyz1, xyz2, rot_t)
            newmember.XYZk = MyMath.rotatepoint(self.XYZk, xyz1, xyz2, rot_t)
            newmember.XYZl = MyMath.rotatepoint(self.XYZl, xyz1, xyz2, rot_t)
            newmember.Name = newname
            newmembers.append(newmember)
        return newmembers

    ###### Create Elements ########################
    def createelements(self):
        global ndm
        eleProps = self.EleProps
        xyzi = self.XYZi
        xyzj = self.XYZj
        xyzk = self.XYZk
        xyzl = self.XYZl
        Nij = self.Nij
        Njk = self.Njk

        nodeTag = 1
        eleTag = 1

        if ndm == 3:
            if len(xyzi) != 3 or len(xyzj) != 3 or len(xyzk) != 3 or len(xyzl) != 3:
                raise ValueError("ndm = 3: xyz should be a list contains coordinates [x, y, z]")
            xi, yi, zi = xyzi
            xj, yj, zj = xyzj
            xk, yk, zk = xyzk
            xl, yl, zl = xyzl
        else:
            if len(xyzi) < 2 or len(xyzj) < 2 or len(xyzk) < 2 or len(xyzl) < 2:
                raise ValueError("ndm = 2: xyz should be a list contains coordinates [x, y]")
            xi, yi = xyzi[0], xyzi[1]
            xj, yj = xyzj[0], xyzj[1]
            xk, yk = xyzk[0], xyzk[1]
            xl, yl = xyzl[0], xyzl[1]
            zi = zj = zk = zl = 0

        if eleProps['eleType'] in ['ShellNL', '9_4_QuadUP']:
            XX = np.zeros((2 * Njk + 1, 2 * Nij + 1))
            YY = np.zeros((2 * Njk + 1, 2 * Nij + 1))
            ZZ = np.zeros((2 * Njk + 1, 2 * Nij + 1))
            Noderange = np.zeros((2 * Njk + 1, 2 * Nij + 1))

            Xst = np.linspace(xi, xl, num=2 * Njk + 1)
            Xen = np.linspace(xj, xk, num=2 * Njk + 1)

            Yst = np.linspace(yi, yl, num=2 * Njk + 1)
            Yen = np.linspace(yj, yk, num=2 * Njk + 1)

            Zst = np.linspace(zi, zl, num=2 * Njk + 1)
            Zen = np.linspace(zj, zk, num=2 * Njk + 1)
        else:
            XX = np.zeros((Njk + 1, Nij + 1))
            YY = np.zeros((Njk + 1, Nij + 1))
            ZZ = np.zeros((Njk + 1, Nij + 1))
            Noderange = np.zeros((Njk + 1, Nij + 1))
            Xst = np.linspace(xi, xl, num=Njk + 1)
            Xen = np.linspace(xj, xk, num=Njk + 1)

            Yst = np.linspace(yi, yl, num=Njk + 1)
            Yen = np.linspace(yj, yk, num=Njk + 1)

            Zst = np.linspace(zi, zl, num=Njk + 1)
            Zen = np.linspace(zj, zk, num=Njk + 1)


        if eleProps['eleType'] in ['ShellNL', '9_4_QuadUP']:
            for i in range(0, 2 * Njk + 1):
                xrow = np.linspace(Xst[i], Xen[i], num=2 * Nij + 1)
                yrow = np.linspace(Yst[i], Yen[i], num=2 * Nij + 1)
                zrow = np.linspace(Zst[i], Zen[i], num=2 * Nij + 1)
                nraw = np.linspace(i * (2 * Nij + 1) + 1, i * (2 * Nij + 1) + 1 + 2 * Nij, num=2 * Nij + 1)
                XX[i, :] = xrow
                YY[i, :] = yrow
                ZZ[i, :] = zrow
                Noderange[i, :] = nraw
        else:
            for i in range(0, Njk + 1):
                xrow = np.linspace(Xst[i], Xen[i], num=Nij + 1)
                yrow = np.linspace(Yst[i], Yen[i], num=Nij + 1)
                zrow = np.linspace(Zst[i], Zen[i], num=Nij + 1)
                nraw = np.linspace(i * (Nij + 1) + 1, i * (Nij + 1) + 1 + Nij, num=Nij + 1)
                XX[i, :] = xrow
                YY[i, :] = yrow
                ZZ[i, :] = zrow
                Noderange[i, :] = nraw

        edgeNodes = []
        edgeNodes.append(list(Noderange[0]))
        edgeNodes.append(list(np.transpose(Noderange)[-1]))
        b = list(Noderange[-1])
        b.reverse()
        edgeNodes.append(b)
        b = list(np.transpose(Noderange)[0])
        b.reverse()
        edgeNodes.append(b)
        for i in range(len(edgeNodes)):
            edgeNodes[i] = [int(x) for x in edgeNodes[i]]

        Nodes = {}

        for i in np.arange(len(XX.reshape(-1))):
            x = XX.reshape(-1)[i]
            y = YY.reshape(-1)[i]
            z = ZZ.reshape(-1)[i]
            Nodes[nodeTag] = [x, y, z]
            nodeTag += 1

        # Extract Elements Node Tags
        Elements = {}
        if eleProps['eleType'] in ['ShellDKGT', 'ShellNLDKGT', 'Tri31']:
            for i in range(0, Njk):
                for j in range(1, Nij + 1):
                    nodei = i * (Nij + 1) + j
                    nodej = nodei + 1
                    nodek = nodej + (Nij + 1)
                    nodel = nodei + (Nij + 1)
                    Elements[eleTag] = [nodei, nodej, nodek]
                    eleTag += 1
                    Elements[eleTag] = [nodei, nodek, nodel]
                    eleTag += 1
        elif eleProps['eleType'] in ['quad', 'ShellMITC4', 'ShellDKGQ', 'ShellNLDKGQ', 'bbarQuad', 'enhancedQuad',
                                     'SSPquad']:
            for i in range(0, Njk):
                for j in range(1, Nij + 1):
                    nodei = i * (Nij + 1) + j
                    nodej = nodei + 1
                    nodek = nodej + (Nij + 1)
                    nodel = nodei + (Nij + 1)
                    Elements[eleTag] = [nodei, nodej, nodek, nodel]
                    eleTag += 1
        elif eleProps['eleType'] in ['ShellNL', '9_4_QuadUP']:
            for i in range(0, Njk):
                for j in range(1, 2 * Nij + 1, 2):
                    node1 = 2 * i * (2 * Nij + 1) + j
                    node2 = node1 + 2
                    node3 = node2 + 2 * (2 * Nij + 1)
                    node4 = node1 + 2 * (2 * Nij + 1)
                    node5 = node1 + 1
                    node6 = node2 + (2 * Nij + 1)
                    node7 = node3 - 1
                    node8 = node1 + (2 * Nij + 1)
                    node9 = node5 + (2 * Nij + 1)

                    Elements[eleTag] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                    eleTag += 1

        return Nodes, Elements, edgeNodes
        ## End of CreatePatches Function
class Triangle:
    def __init__(self, name, eleProps, xyzi, xyzj, xyzk, Ndiv=4, attach='y'):
        self.Name = name
        self.EleProps = eleProps
        self.XYZi = xyzi
        self.XYZj = xyzj
        self.XYZk = xyzk
        self.NDiv = Ndiv
        self.Attach = attach
        self.Uniload = []
        self.NodeSets = {'ij':[],'jk':[],'ki':[]}
        self.Nodes = {}
        self.Elements = {}
    ###### validation VBlock ( Set and Get Properties ) ########################
    def __get_name(self):
            return self._Name

    def __set_name(self, name):
        if type(name) is not str:
            raise ValueError("name must be string")
        self._Name = name

    def __del_name(self):
        del self._Name

    Name = property(__get_name, __set_name, __del_name)

    # XYZi
    def __get_XYZi(self):
        return self._XYZi

    def __set_XYZi(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZi = value

    def __del_XYZi(self):
        del self._XYZi

    XYZi = property(__get_XYZi, __set_XYZi, __del_XYZi)

    # XYZj
    def __get_XYZj(self):
        return self._XYZj

    def __set_XYZj(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZj = value

    def __del_XYZj(self):
        del self._XYZj

    XYZj = property(__get_XYZj, __set_XYZj, __del_XYZj)

    # XYZk
    def __get_XYZk(self):
        return self._XYZk

    def __set_XYZk(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZk = value

    def __del_XYZk(self):
        del self._XYZk

    XYZk = property(__get_XYZk, __set_XYZk, __del_XYZk)

    # NDiv Validation
    def __get_NDiv(self):
        return self._NDiv

    def __set_NDiv(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._NDiv = val

    def __del_NDiv(self):
        del self._NDiv

    NDiv = property(__get_NDiv, __set_NDiv, __del_NDiv)


    # EleProps Validation
    def __get_EleProps(self):
        return self._EleProps

    def __set_EleProps(self, value):
        if type(value) != dict:
            raise ValueError('eleProps must be a python dictionary')


        self._EleProps = value

    def __del_EleProps(self):
        del self._EleProps

    EleProps = property(__get_EleProps, __set_EleProps, __del_EleProps)

    ## End of validation

    ###### loading ########################
    def assign_uniload(self, pattern, value, direction=2):
        if isinstance(value, numbers.Number) == False:
            raise ValueError('value must be a numeric value')

        if direction not in [1, 2, 3]:
            raise ValueError('direction must be one of 1, 2 or 3')
        uniloads = self.Uniload
        uniloads.append([pattern, value, direction])

    ###### linear replicate ########################
    def replicate_linear(self, number, dx, dy, dz):
        if (type(number) != int):
            raise ValueError("Number of replications must be positive integer value")

        if (number <= 0):
            raise ValueError("Number of replications must be positive integer value")

        if isinstance(dx, numbers.Number) == False:
            raise ValueError('dx must be a numeric value')

        if isinstance(dy, numbers.Number) == False:
            raise ValueError('dy must be a numeric value')

        if isinstance(dz, numbers.Number) == False:
            raise ValueError('dz must be a numeric value')

        newmembers = []
        name = self.Name
        xi, yi, zi = self.XYZi
        xj, yj, zj = self.XYZj
        xk, yk, zk = self.XYZk

        for i in range(number):
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newxi, newyi, newzi  = xi + (i + 1) * dx, yi + (i + 1) * dy, zi + (i + 1) * dz
            newxj, newyj, newzj = xj + (i + 1) * dx, yj + (i + 1) * dy, zj + (i + 1) * dz
            newxk, newyk, newzk = xk + (i + 1) * dx, yk + (i + 1) * dy, zk + (i + 1) * dz
            newmember.XYZi = [newxi, newyi, newzi]
            newmember.XYZj = [newxj, newyj, newzj]
            newmember.XYZk = [newxk, newyk, newzk]
            newmember.Name = newname
            newmembers.append(newmember)
        return newmembers

    ###### replicate mirror ########################
    def replicate_mirror(self, xyz1, xyz2, xyz3):
        name = self.Name
        newname = name + "_mir"
        newmember = copy.deepcopy(self)
        newmember.XYZi = MyMath.mirrorpoint(self.XYZi, xyz1, xyz2, xyz3)
        newmember.XYZj = MyMath.mirrorpoint(self.XYZj, xyz1, xyz2, xyz3)
        newmember.XYZk = MyMath.mirrorpoint(self.XYZk, xyz1, xyz2, xyz3)
        newmember.Name = newname
        return newmember

    ###### replicate rotate ########################
    def replicate_rotate(self, number, xyz1, xyz2, teta):
        newmembers = []
        name = self.Name
        for i in range(number):
            rot_t = teta * (i + 1)
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newmember.XYZi = MyMath.rotatepoint(self.XYZi, xyz1, xyz2, rot_t)
            newmember.XYZj = MyMath.rotatepoint(self.XYZj, xyz1, xyz2, rot_t)
            newmember.XYZk = MyMath.rotatepoint(self.XYZk, xyz1, xyz2, rot_t)
            newmember.Name = newname
            newmembers.append(newmember)
        return newmembers

    ###### Create Elements ########################
    def createelements(self):
        global ndm
        eleProps = self.EleProps
        xyzi = self.XYZi
        xyzj = self.XYZj
        xyzk = self.XYZk
        N = self.NDiv

        if ndm == 3:
            if len(xyzi) != 3 or len(xyzj) != 3 or len(xyzk) != 3:
                raise ValueError("ndm = 3: xyz should be a list contains coordinates [x, y, z]")

        else:
            if len(xyzi) < 2 or len(xyzj) < 2 or len(xyzk) < 2:
                raise ValueError("ndm = 2: xyz should be a list contains coordinates [x, y]")
            xyzi = [xyzi[0], xyzi[1], 0]
            xyzj = [xyzj[0], xyzj[1], 0]
            xyzk = [xyzk[0], xyzk[1], 0]

        # Extract Elements Node Tags
        ele_numnodes = 4
        if eleProps['eleType'] in ['ShellDKGT', 'ShellNLDKGT', 'Tri31']:
            ele_numnodes = 3

        elif eleProps['eleType'] in ['ShellNL', '9_4_QuadUP']:
            ele_numnodes = 9

        Nodes, Elements, aedgeNodes = MyMath.dividetriangle(N, ele_numnodes, xyzi, xyzj, xyzk)
        edgeNodes = [list(aedgeNodes['ij']), list(aedgeNodes['jk']), list(aedgeNodes['ki'])]

        for i in range(len(edgeNodes)):
            edgeNodes[i] = [int(x) for x in edgeNodes[i]]

        return Nodes, Elements, edgeNodes
        ## End of CreatePatches Function

class Line:
    def __init__(self, name, eleProps, xyzi, xyzj, Ndiv=1, attach='y'):
        self.Name = name
        self.EleProps = eleProps
        self.XYZi = xyzi
        self.XYZj = xyzj
        self.NDiv = Ndiv
        self.Attach = attach
        self.Uniload = []
        self.Pointload = []
        self.NodeSets = {'i': 0, 'j': 0}
        self.Nodes = {}
        self.Elements = {}

    ###### alidation VBlock ( Set and Get Properties ) ########################
    def __get_name(self):
            return self._Name

    def __set_name(self, name):
        if type(name) is not str:
            raise ValueError("name must be string")
        self._Name = name

    def __del_name(self):
        del self._Name

    Name = property(__get_name, __set_name, __del_name)

    # XYZi
    def __get_XYZi(self):
        return self._XYZi

    def __set_XYZi(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])
            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZi = value

    def __del_XYZi(self):
        del self._XYZi

    XYZi = property(__get_XYZi, __set_XYZi, __del_XYZi)

    # XYZj
    def __get_XYZj(self):
        return self._XYZj

    def __set_XYZj(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZj = value

    def __del_XYZj(self):
        del self._XYZj

    XYZj = property(__get_XYZj, __set_XYZj, __del_XYZj)

    # NDiv Validation
    def __get_NDiv(self):
        return self._NDiv

    def __set_NDiv(self, val):
        if (type(val) != int):
            raise ValueError("Number of subdivisions must be positive integer value")

        if (val <= 0):
            raise ValueError("Number of subdivisions must be positive integer value")

        self._NDiv = val

    def __del_NDiv(self):
        del self._NDiv

    NDiv = property(__get_NDiv, __set_NDiv, __del_NDiv)

    # EleProps Validation
    def __get_EleProps(self):
        return self._EleProps

    def __set_EleProps(self, value):
        if type(value) != dict:
            raise ValueError('eleProps must be a python dictionary')

        self._EleProps = value

    def __del_EleProps(self):
        del self._EleProps

    EleProps = property(__get_EleProps, __set_EleProps, __del_EleProps)

    ## End of validation
    ###### Assign Loads ########################
    def assign_uniload(self, pattern, value, direction=2):
        if isinstance(value, numbers.Number) == False:
            raise ValueError('value must be a numeric value')

        if direction not in [1, 2, 3]:
            raise ValueError('direction must be one of 1, 2 or 3')
        uniloads = self.Uniload
        uniloads.append([pattern, value, direction])

    # def assign_pointload(self, pattern, *distvalue, direction=2):
    #     poloads = self.Pointload
    #     poloads.append([pattern, distvalue, direction])

    ###### linear replicate ########################
    def replicate_linear(self, number, dx, dy, dz):
        if (type(number) != int):
            raise ValueError("Number of replications must be positive integer value")

        if (number <= 0):
            raise ValueError("Number of replications must be positive integer value")

        if isinstance(dx, numbers.Number) == False:
            raise ValueError('dx must be a numeric value')

        if isinstance(dy, numbers.Number) == False:
            raise ValueError('dy must be a numeric value')

        if isinstance(dz, numbers.Number) == False:
            raise ValueError('dz must be a numeric value')

        newmembers = []
        name = self.Name
        xi, yi, zi = self.XYZi
        xj, yj, zj = self.XYZj
        for i in range(number):
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newxi, newyi, newzi = xi + (i + 1) * dx, yi + (i + 1) * dy, zi + (i + 1) * dz
            newxj, newyj, newzj = xj + (i + 1) * dx, yj + (i + 1) * dy, zj + (i + 1) * dz
            newmember.XYZi = [newxi, newyi, newzi]
            newmember.XYZj = [newxj, newyj, newzj]
            newmember.Name = newname
            newmembers.append(newmember)

        return newmembers

    ###### replicate mirror ########################
    def replicate_mirror(self, xyz1, xyz2, xyz3):
        name = self.Name
        newname = name + "_mir"
        newmember = copy.deepcopy(self)
        newmember.XYZi = MyMath.mirrorpoint(self.XYZi, xyz1, xyz2, xyz3)
        newmember.XYZj = MyMath.mirrorpoint(self.XYZj, xyz1, xyz2, xyz3)
        newmember.Name = newname
        return newmember

    ###### replicate rotate ########################
    def replicate_rotate(self, number, xyz1, xyz2, teta):
        newmembers = []
        name = self.Name
        for i in range(number):
            rot_t = teta * (i + 1)
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newmember.XYZi = MyMath.rotatepoint(self.XYZi, xyz1, xyz2, rot_t)
            newmember.XYZj = MyMath.rotatepoint(self.XYZj, xyz1, xyz2, rot_t)
            newmember.Name = newname
            newmembers.append(newmember)

        return newmembers

    ###### Create Elements ########################
    def createelements(self):
        global ndm
        eleProps = self.EleProps
        xyzi = self.XYZi
        xyzj = self.XYZj
        Nij = self.NDiv
        nodeTag = 1
        eleTag = 1

        if eleProps['eleType'] in ['ModElasticBeam2d']:
            if ndm == 3:
                print('Warning: Using ModElasticBeam2d element: ndm set to 2')
            ndm = 2

        if ndm == 3:
            if len(xyzi) != 3 or len(xyzj) != 3:
                raise ValueError("ndm = 3: xyz should be a list contains coordinates [x, y, z]")
            xi, yi, zi = xyzi
            xj, yj, zj = xyzj

        else:
            if len(xyzi) < 2 or len(xyzj) < 2:
                raise ValueError("ndm = 2: xyz should be a list contains coordinates [x, y]")
            xi, yi = xyzi[0], xyzi[1]
            xj, yj = xyzj[0], xyzj[1]
            zi = zj = 0


        XX = np.linspace(xi, xj, num=Nij + 1)
        YY = np.linspace(yi, yj, num=Nij + 1)
        ZZ = np.linspace(zi, zj, num=Nij + 1)
        edgeNodes = [1, Nij + 1]

        Nodes = {}

        for i in np.arange(len(XX)):
            x = XX[i]
            y = YY[i]
            z = ZZ[i]
            Nodes[nodeTag] = [x, y, z]
            nodeTag += 1

        # Extract Elements Node Tags
        Elements = {}

        for i in range(1, Nij + 1):
            nodei = i
            nodej = nodei + 1
            Elements[eleTag] = [nodei, nodej]
            eleTag += 1

        return Nodes, Elements, edgeNodes
        ## End of CreatePatches Function

class Point:
    def __init__(self, name, xyz, mass=[], rest=[], attach='y'):
        self.XYZ = xyz
        self.Name = name
        self.NodeTag = 0
        self.Pointload = []
        self.Attach = attach
        self.Mass = mass
        self.Rest = rest
    ###### alidation VBlock ( Set and Get Properties ) ########################
    def __get_name(self):
            return self._Name

    def __set_name(self, name):
        if type(name) is not str:
            raise ValueError("name must be string")
        self._Name = name

    def __del_name(self):
        del self._Name

    Name = property(__get_name, __set_name, __del_name)

    # XYZ
    def __get_XYZ(self):
        return self._XYZ

    def __set_XYZ(self, value):
        value = list(value)
        if len(value) not in [2, 3]:
            raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

        for i in range(len(value)):
            if type(value[i]) is int:
                value[i] = float(value[i])

            if isinstance(value[i], numbers.Number) == False:
                raise ValueError("Coordinates must be numeric values")

        self._XYZ = value

    def __del_XYZ(self):
        del self._XYZ

    XYZ = property(__get_XYZ, __set_XYZ, __del_XYZ)

    ## End of validation

    def assign_pointload(self, pattern, *values):
        for value in values:
            if isinstance(value, numbers.Number) == False:
                raise ValueError('value must be a numeric value')

        poloads = self.Pointload
        poloads.append([pattern, values])

    ###### linear replicate ########################
    def replicate_linear(self, number, dx, dy, dz):
        if (type(number) != int):
            raise ValueError("Number of replications must be positive integer value")

        if (number <= 0):
            raise ValueError("Number of replications must be positive integer value")

        if isinstance(dx, numbers.Number) == False:
            raise ValueError('dx must be a numeric value')

        if isinstance(dy, numbers.Number) == False:
            raise ValueError('dy must be a numeric value')

        if isinstance(dz, numbers.Number) == False:
            raise ValueError('dz must be a numeric value')

        newmembers = []
        name = self.Name
        x, y, z = self.XYZ
        for i in range(number):
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newx, newy, newz = x + (i + 1) * dx, y + (i + 1) * dy, z + (i + 1) * dz
            newmember.XYZ = [newx, newy, newz]
            newmember.Name = newname
            newmembers.append(newmember)

        return newmembers

    ###### replicate mirror ########################
    def replicate_mirror(self, xyz1, xyz2, xyz3):
        name = self.Name
        newname = name + "_mir"
        newmember = copy.deepcopy(self)
        newmember.XYZ = MyMath.mirrorpoint(self.XYZ, xyz1, xyz2, xyz3)
        newmember.Name = newname
        return newmember

    ###### replicate rotate ########################
    def replicate_rotate(self, number, xyz1, xyz2, teta):
        newmembers = []
        name = self.Name
        for i in range(number):
            rot_t = teta * (i + 1)
            newname = name + "_" + str(i + 1)
            newmember = copy.deepcopy(self)
            newmember.XYZ = MyMath.rotatepoint(self.XYZ, xyz1, xyz2, rot_t)
            newmember.Name = newname
            newmembers.append(newmember)

        return newmembers

    # ###### Create Elements ########################
    # def createnode(self):
    #     global ndm
    #     xyz = self.XYZ
    #     nodeTag = 1
    #     eleTag = 1
    #
    #     if ndm == 3:
    #         if len(xyz) != 3:
    #             raise ValueError("ndm = 3: xyz should be a list contains coordinates [x, y, z]")
    #         x, y, z = xyz
    #
    #     else:
    #         if len(xyzi) < 2 or len(xyzj) < 2 :
    #             raise ValueError("ndm = 2: xyz should be a list contains coordinates [x, y]")
    #         xi, yi = xyzi[0], xyzi[1]
    #         xj, yj = xyzj[0], xyzj[1]
    #         zi = zj = 0
    #
    #
    #     XX = np.linspace(xi, xj, num=Nij + 1)
    #     YY = np.linspace(yi, yj, num=Nij + 1)
    #     ZZ = np.linspace(zi, zj, num=Nij + 1)
    #     edgeNodes = [1, Nij + 1]
    #
    #     Nodes = {}
    #
    #     for i in np.arange(len(XX)):
    #         x = XX[i]
    #         y = YY[i]
    #         z = ZZ[i]
    #         Nodes[nodeTag] = [x, y, z]
    #         nodeTag += 1
    #
    #     # Extract Elements Node Tags
    #     Elements = {}
    #
    #     for i in range(1, Nij + 1):
    #         nodei = i
    #         nodej = nodei + 1
    #         Elements[eleTag] = [nodei, nodej]
    #         eleTag += 1
    #
    #     return Nodes, Elements, edgeNodes
    #     ## End of CreatePatches Function

### Class point]
def createopsmodel(ops, model, printcommand='n'):
    if type(printcommand) != str:
        raise ValueError('mergenodes must be \'y\', \'yes\',\'n\' or \'no\'')

    if printcommand.lower() not in ['y', 'yes', 'n','no']:
        raise ValueError('mergenodes must be \'y\', \'yes\',\'n\' or \'no\'')

    file_elements = open("file_elements.txt", "a")

    output = {}
    lineuniloads = {}
    quaduniloads = {}
    bodyloads = {}
    members_attached = []
    members_notattached = []

    for member in model.Members:
        if member.Attach.lower() in ['y', 'yes']:
            members_attached.append(member)
        else:
            members_notattached.append(member)

    orgmembers = members_attached
    orgmembers.extend(members_notattached)

    for member in orgmembers:

        modelexnodes = ops.getNodeTags()

        if len(modelexnodes) == 0:
            nodeTag = 0
        else:
            nodeTag = int(np.max(ops.getNodeTags()))

        if len(ops.getEleTags()) == 0:
            eleTag = 0
        else:
            eleTag = int(np.max(ops.getEleTags()))

        Nodesatsameloc = []
        exnodes = []
        mergenodes = member.Attach

        if isinstance(member, Point):
            x, y, z = member.XYZ
            exnodeTag = nodeexist(ops, [x, y, z])
            if mergenodes.lower() not in ['y', 'yes']:
                if exnodeTag != False:
                    Nodesatsameloc.append([exnodeTag, 1 + nodeTag])
                    exnodeTag = False

            if exnodeTag == False:
                if ndm == 2:
                    str_command = "ops.node(" + str(int(1 + nodeTag)) + ", " + str(x) + ", " + str(y) + ")"

                elif ndm == 3:
                    str_command = "ops.node(" + str(int(1 + nodeTag)) + ", " + str(x) + ", " + str(y) + \
                                  ", " + str(z) + ")"

                if printcommand.lower() in ['y', 'yes']:
                    print(str_command)

                eval(str_command)
                member.NodeTag = 1 + nodeTag
                if len(member.Rest) != 0:
                    __assignrest(ops, 1 + nodeTag, member.Rest, printcommand)

                if len(member.Mass) != 0:
                    file_mass = open("file_mass.txt", "a")
                    str_vals = ""
                    for m in member.Mass:
                        str_vals = str_vals + ", " + str(m)

                    str_command_m = "ops.mass(" + str(1 + nodeTag) + str_vals + ")"
                    file_mass.write(str_command_m + '\n')

                    if printcommand.lower() in ['y', 'yes']:
                        print(str_command_m)
                    eval(str_command_m)
                    file_mass.close()

                file_nodes = open("file_nodes.txt", "a")
                file_nodes.write(str_command + '\n')
                file_nodes.close()
            else:
                member.NodeTag = exnodeTag

            continue

        Nodes, Elements, Noderange = member.createelements()
        eleProps = member.EleProps
        nodes_ = member.Nodes
        elements_ = member.Elements
        nodecounts = {}

        for tag in Nodes.keys():
            x = Nodes[tag][0]
            y = Nodes[tag][1]
            z = Nodes[tag][2]
            exnodeTag = nodeexist(ops, [x, y, z])
            if mergenodes.lower() not in ['y', 'yes']:
                if exnodeTag != False:
                    Nodesatsameloc.append([exnodeTag, tag + nodeTag])
                    exnodeTag = False

            if exnodeTag == False:
                nodecounts[tag] = tag + nodeTag
                nodes_[tag + nodeTag] = [x, y, z]
            else:
                exnodes.append(exnodeTag)
                nodecounts[tag] = exnodeTag
                nodes_[exnodeTag] = [x, y, z]

        # Create Node Objects
        file_nodes = open("file_nodes.txt", "a")
        for nod in nodes_.keys():
            x, y, z = nodes_[nod]
            if nod not in exnodes:
                if ndm == 2:
                    str_command = "ops.node(" + str(int(nod)) + ", " + str(x) + ", " + str(y) +")"
                elif ndm == 3:
                    str_command = "ops.node(" + str(int(nod)) + ", " + str(x) + ", " + str(y) + ", " + str(z) + ")"

                file_nodes.write(str_command + '\n')

                if printcommand.lower() in ['y', 'yes']:
                    print(str_command)

                eval(str_command)

        file_nodes.close()
        nodeset = member.NodeSets

        if isinstance(member, Brick):
            for face in Noderange.keys():
                fnodes = Noderange[face]['Nodes']
                nfnodes = []
                for nn in fnodes:
                    nfnodes_ = []
                    for n in nn:
                        nfnodes_.append(int(nodecounts[n]))

                    nfnodes.append(nfnodes_)

                nodeset[face]['Nodes'] = nfnodes

                fnodes = Noderange[face]['ij']
                nfnodes_ = []
                for nn in fnodes:
                    nfnodes_.append(int(nodecounts[nn]))

                nodeset[face]['ij'] = nfnodes_

                fnodes = Noderange[face]['jk']
                nfnodes_ = []
                for nn in fnodes:
                    nfnodes_.append(int(nodecounts[nn]))

                nodeset[face]['jk'] = nfnodes_

                fnodes = Noderange[face]['kl']
                nfnodes_ = []
                for nn in fnodes:
                    nfnodes_.append(int(nodecounts[nn]))

                nodeset[face]['kl'] = nfnodes_

                fnodes = Noderange[face]['li']
                nfnodes_ = []
                for nn in fnodes:
                    nfnodes_.append(int(nodecounts[nn]))

                nodeset[face]['li'] = nfnodes_


        elif isinstance(member, Quad):

            nodeset['ij'] = [nodecounts[x] for x in Noderange[0]]
            nodeset['jk'] = [nodecounts[x] for x in Noderange[1]]
            nodeset['kl'] = [nodecounts[x] for x in Noderange[2]]
            nodeset['li'] = [nodecounts[x] for x in Noderange[3]]

        elif isinstance(member, Triangle):

            nodeset['ij'] = [nodecounts[x] for x in Noderange[0]]
            nodeset['jk'] = [nodecounts[x] for x in Noderange[1]]
            nodeset['ki'] = [nodecounts[x] for x in Noderange[2]]
        elif isinstance(member, Polygon):
            nrcount = 1
            for node_r in Noderange:
                nodeset[str(nrcount)] = [nodecounts[x] for x in node_r]
                nrcount += 1
        elif isinstance(member, Line):
            nodeset['i'] = nodecounts[Noderange[0]]
            nodeset['j'] = nodecounts[Noderange[1]]

        if isinstance(member, Line):
            for ele in Elements.keys():
                nodes = []
                for n in Elements[ele]:
                    nodes.append(nodecounts[n])

                str_elecommand = propcommand(ele + eleTag, nodes, eleProps)
                str_command = "ops." + str_elecommand

                file_elements.write(str_command + '\n')

                if printcommand.lower() in ['y', 'yes']:
                    print(str_command)

                eval(str_command)
                elements_[ele + eleTag] = nodes
                lineuniloads[ele + eleTag] = member.Uniload

        elif isinstance(member, Triangle):

            for ele in Elements.keys():
                nodes = []
                for n in Elements[ele]:
                    nodes.append(nodecounts[n])

                str_elecommand = propcommand(ele + eleTag, nodes, eleProps)
                str_command = "ops." + str_elecommand

                file_elements.write(str_command + '\n')

                if printcommand.lower() in ['y', 'yes']:
                    print(str_command)

                eval(str_command)
                elements_[ele + eleTag] = nodes
                quaduniloads[ele + eleTag] = member.Uniload

        elif isinstance(member, Quad):
            for ele in Elements.keys():
                nodes = []
                for n in Elements[ele]:
                    nodes.append(nodecounts[n])

                str_elecommand = propcommand(ele + eleTag, nodes, eleProps)
                str_command = "ops." + str_elecommand

                file_elements.write(str_command + '\n')

                if printcommand.lower() in ['y', 'yes']:
                    print(str_command)

                eval(str_command)
                elements_[ele + eleTag] = nodes
                quaduniloads[ele + eleTag] = member.Uniload

        elif isinstance(member, Brick):
            for ele in Elements.keys():
                nodes = []
                for n in Elements[ele]:
                    nodes.append(nodecounts[n])

                str_elecommand = propcommand(ele + eleTag, nodes, eleProps)
                str_command = "ops." + str_elecommand

                file_elements.write(str_command + '\n')

                if printcommand.lower() in ['y', 'yes']:
                    print(str_command)

                eval(str_command)
                elements_[ele + eleTag] = nodes

        print("# Elements for " + member.Name + '  were created.')

        output[member.Name] = [nodes_, elements_, Nodesatsameloc]

    model.LineUniLoads = lineuniloads
    model.QuadUniLoads = quaduniloads
    model.BodyLoads = bodyloads

    __addmass(ops, model.NodalMasses, printcommand)

    for spconsts in model.SpConstraints:
        __assignspconstraint(ops, spconsts, printcommand)

    for const in model.EqualDofs:
        __assignequaldof(ops, const, printcommand)

    masternodes = []
    for const in model.RigidDiaphragms:
        rnode = __assignrigiddiaph(ops, const, printcommand)
        masternodes.append(rnode)

    for const in model.RigidLinks:
        __assignrigidlink(ops, const, printcommand)

    file_elements.close()

    return output, masternodes

def __assignrest(ops, nodetag, cvals, printcommand):
    str_vals = ""
    for m in cvals:
        str_vals += ", " + str(m)

    file_fix = open("file_fix.txt", "a")

    str_command = "ops.fix(" + str(nodetag) + str_vals + ")"
    file_fix.write(str_command + '\n')

    if printcommand.lower() in ['y', 'yes']:
        print(str_command)

    eval(str_command)
    file_fix.close()

def __assignspconstraint(ops, spconsts, printcommand):
    xlim, ylim, zlim, cvals = spconsts[0], spconsts[1], spconsts[2], spconsts[3]

    if len(xlim) == 2:
        check_x = True
    elif len(xlim) == 0:
        check_x = False
    else:
        raise ValueError('xlim should be an empty list or a list with xmin and xmax values')

    if len(ylim) == 2:
        check_y = True
    elif len(ylim) == 0:
        check_y = False
    else:
        raise ValueError('ylim should be an empty list or a list with ymin and ymax values')

    if len(zlim) == 2:
        check_z = True
    elif len(zlim) == 0:
        check_z = False
    else:
        raise ValueError('zlim should be an empty list or a list with zmin and zmax values')

    if ndm == 2:
        if len(cvals) == 0:
            str_vals = ", 1, 1, 1"
        else:
            str_vals = ""
            for m in cvals:
                str_vals += ", " + str(m)

    else:
        if len(cvals) == 0:
            str_vals = ", 1, 1, 1, 1, 1, 1"
        else:
            str_vals = ""
            for m in cvals:
                str_vals += ", " + str(m)

    file_fix = open("file_fix.txt", "a")
    node_s = findnodes(ops, xlim, ylim, zlim)
    if node_s == False:
        return

    for nod in node_s:
        str_command = "ops.fix(" + str(nod) + str_vals + ")"
        file_fix.write(str_command + '\n')

        if printcommand.lower() in ['y', 'yes']:
            print(str_command)

        eval(str_command)

    file_fix.close()

def __assignrigidlink(ops, rigidlink, printcommand):
    xyzr, type, xlim, ylim, zlim = rigidlink[0], rigidlink[1], rigidlink[2], rigidlink[3], rigidlink[4]

    if len(xlim) == 2:
        check_x = True
    elif len(xlim) == 0:
        check_x = False
    else:
        raise ValueError('xlim should be an empty list or a list with xmin and xmax values')

    if len(ylim) == 2:
        check_y = True
    elif len(ylim) == 0:
        check_y = False
    else:
        raise ValueError('ylim should be an empty list or a list with ymin and ymax values')

    if len(zlim) == 2:
        check_z = True
    elif len(zlim) == 0:
        check_z = False
    else:
        raise ValueError('zlim should be an empty list or a list with zmin and zmax values')

    noder = nodeexist(ops, xyzr)
    if noder == False:
        print("Note:")
        print("rigidLink constraint: Master node was not found")
        return

    for nod in ops.getNodeTags():
        if ndm == 3:
            xn, yn, zn = ops.nodeCoord(nod)
        elif ndm == 2:
            xn, yn = ops.nodeCoord(nod)
            check_z = False

        if nod == noder:
            continue

        if check_x:
            if xn < xlim[0] or xn > xlim[1] :
                continue

        if check_y:
            if yn < ylim[0] or yn > ylim[1] :
                continue

        if check_z:
            if zn < zlim[0] or zn > zlim[1] :
                continue
        # rigidLink(type, rNodeTag, cNodeTag)
        if type == 'beam':
            str_command = "ops.rigidLink('beam', " + str(noder) + ", " + str(nod) + ")"
        elif type == 'bar':
            str_command = "ops.rigidLink('bar', " + str(noder) + ", " + str(nod) + ")"

        file_constraint = open("file_constraint.txt", "a")
        file_constraint.write(str_command + '\n')

        if printcommand.lower() in ['y', 'yes']:
            print(str_command)

        eval(str_command)
        file_constraint.close()

def __assignequaldof(ops, equaldof, printcommand):

    xyzr, xlim, ylim, zlim, dofs = equaldof[0], equaldof[1], equaldof[2], equaldof[3], equaldof[4]
    if len(xlim) == 2:
        check_x = True
    elif len(xlim) == 0:
        check_x = False
    else:
        raise ValueError('xlim should be an empty list or a list with xmin and xmax values')

    if len(ylim) == 2:
        check_y = True
    elif len(ylim) == 0:
        check_y = False
    else:
        raise ValueError('ylim should be an empty list or a list with ymin and ymax values')

    if len(zlim) == 2:
        check_z = True
    elif len(zlim) == 0:
        check_z = False
    else:
        raise ValueError('zlim should be an empty list or a list with zmin and zmax values')

    # equalDOF(rNodeTag, cNodeTag, *dofs)
    if ndm == 2:
        if len(dofs) <= 3 and len(dofs) != 0:
            str_vals = ""
            for d in dofs:
              str_vals = str_vals + ", " + str(dofs[d])
        elif len(dofs) == 0:
            str_vals = ", 1, 2, 3"
        else:
            raise ValueError('ndm = 2: list of dofs values should be an empty list(dofs = 1, 2, 3) or a list with maximum of 3 values(1 through 3)')
    else:
        if len(dofs) <= 6 and len(dofs) != 0:
            str_vals = ""
            for d in dofs:
              str_vals = str_vals + ", " + str(dofs[d])
        elif len(dofs) == 0:
            str_vals = ", 1, 2, 3, 4, 5, 6"
        else:
            raise ValueError('ndm = 3: list of dofs values should be an empty list(dofs = 1, 2, 3, 4, 5, 6) or a list with maximum of 6 values(1 through 6)')

    noder = nodeexist(ops, xyzr)
    if noder == False:
        print("# Note:")
        print("# eualDof constraint: Master node was not found")
        return

    for nod in ops.getNodeTags():
        if ndm == 3:
            xn, yn, zn = ops.nodeCoord(nod)
        elif ndm == 2:
            xn, yn = ops.nodeCoord(nod)
            check_z = False


        if nod == noder:
            continue

        if check_x:
            if xn < xlim[0] or xn > xlim[1] :
                continue

        if check_y:
            if yn < ylim[0] or yn > ylim[1] :
                continue

        if check_z:
            if zn < zlim[0] or zn > zlim[1] :
                continue

        str_command = "ops.equalDOF(" + str(noder) + ", " + str(nod) + str_vals + ")"

        file_constraint = open("file_constraint.txt", "a")
        file_constraint.write(str_command + '\n')

        if printcommand.lower() in ['y', 'yes']:
            print(str_command)

        eval(str_command)
        file_constraint.close()


def __assignrigiddiaph(ops, rigiddiaph, printcommand):

    xyzr, perpdirn = rigiddiaph[0], rigiddiaph[1]
    xlim, ylim, zlim, massr, rests  = rigiddiaph[2], rigiddiaph[3], rigiddiaph[4], rigiddiaph[5], rigiddiaph[6]
    if len(xlim) == 2:
        check_x = True
    elif len(xlim) == 0:
        check_x = False
    else:
        raise ValueError('xlim should be an empty list or a list with xmin and xmax values')

    if len(ylim) == 2:
        check_y = True
    elif len(ylim) == 0:
        check_y = False
    else:
        raise ValueError('ylim should be an empty list or a list with ymin and ymax values')

    if len(zlim) == 2:
        check_z = True
    elif len(zlim) == 0:
        check_z = False
    else:
        raise ValueError('zlim should be an empty list or a list with zmin and zmax values')

    noder = nodeexist(ops, xyzr)
    file_constraint = open("file_constraint.txt", "a")
    if noder == False:
        print("# Note:")
        print("# Rigid Diaphragm constraint: Master node was not found. A new node was created as master node")
        rnode = createnode(ops, xyzr,printcommand)
        if len(rests) != 0:
            file_fix = open("file_fix.txt", "a")
            if ndm == 2:
                restvals = [0, 0, 0]
                for rs in rests:
                    restvals[rs-1] = 1
            else:
                restvals = [0, 0, 0, 0, 0, 0]
                for rs in rests:
                    restvals[rs-1] = 1
            str_vals = ""
            for rsv in restvals:
                str_vals = str_vals + ", " + str(rsv)

            str_command = "ops.fix(" + str(rnode) + str_vals + ")"

            file_fix.write(str_command + '\n')

            if printcommand.lower() in ['y', 'yes']:
                print(str_command)
            eval(str_command)
            file_fix.close()

    else:
        rnode = noder

    if len(massr) != 0:
        file_mass = open("file_mass.txt", "a")
        str_vals = ""
        for m in massr:
            str_vals = str_vals + ", " + str(m)

        str_command = "ops.mass(" + str(rnode) + str_vals + ")"
        file_mass.write(str_command + '\n')

        if printcommand.lower() in ['y', 'yes']:
            print(str_command)
        eval(str_command)
        file_mass.close()

    cNodeTags = []
    for nod in ops.getNodeTags():
        if ndm == 3:
            xn, yn, zn = ops.nodeCoord(nod)
        elif ndm == 2:
            xn, yn = ops.nodeCoord(nod)
            check_z = False

        if nod == rnode:
            continue

        if check_x:
            if xn < xlim[0] or xn > xlim[1] :
                continue

        if check_y:
            if yn < ylim[0] or yn > ylim[1] :
                continue

        if check_z:
            if zn < zlim[0] or zn > zlim[1] :
                continue
        cNodeTags.append(nod)

    str_cnodes = ""
    for n in cNodeTags:
        str_cnodes = str_cnodes + ", " + str(n)

    str_command = "ops.rigidDiaphragm(" + str(perpdirn) + ", " + str(rnode) + str_cnodes + ")"

    file_constraint.write(str_command + '\n')
    if printcommand.lower() in ['y', 'yes']:
        print(str_command)

    eval(str_command)
    file_constraint.close()

    return rnode

def createnode(ops, xyz, printcommand):
    exnode = nodeexist(ops, xyz)
    if exnode != False:
        print("# Note:")
        print("#    Node " + str(exnode) + " exists at this location.")

    nodeTag = int(np.max(ops.getNodeTags())) + 1
    if ndm == 2:
        str_command = "ops.node(" + str(int(nodeTag)) + ", " + str(xyz[0]) + ", " + str(xyz[1]) + ")"

    elif ndm == 3:
        str_command = "ops.node(" + str(int(nodeTag)) + ", " + str(xyz[0]) + ", " + str(xyz[1]) + ", " + str(xyz[2]) + ")"

    if printcommand.lower() in ['y', 'yes']:
        print(str_command)

    eval(str_command)
    file_nodes = open("file_nodes.txt", "a")
    file_nodes.write(str_command + '\n')
    file_nodes.close()
    return nodeTag
def __addmass(ops, nodemasses, printcommand):

    for el in nodemasses:
        xyz = el[0]
        vals = el[1]
        if len(vals) == 0:
            continue
        file_mass = open("file_mass.txt", "a")
        tag = nodeexist(ops, xyz)
        if tag != False:
            strvals = ""
            for m in vals:
                strvals += ", " + str(m)

            str_command = "ops.mass(" + str(tag) + strvals + ")"

            if printcommand.lower() in ['y', 'yes']:
                print(str_command)

            file_mass.write(str_command + '\n')
            file_mass.close()
            eval(str_command)
def __applybrickloads(ops,member,loadpattern, printcommand,file_loading):

    sfactor = loadpattern['scalefactor']
    if len(member.Surfload) != 0:
        for lo in member.Surfload:
            if lo[0] == loadpattern:
                face = lo[1]
                fnodes = member.NodeSets[face]['Nodes']
                Njk, Nij = len(fnodes), len(fnodes[0])
                for i in range(Njk - 1):
                    for j in range(Nij - 1):
                        node_s = []
                        node_s.append(fnodes[i][j])
                        node_s.append(fnodes[i][j + 1])
                        node_s.append(fnodes[i + 1][j + 1])
                        node_s.append(fnodes[i+1][j])
                        xyzi = ops.nodeCoord(node_s[0])
                        xyzj = ops.nodeCoord(node_s[1])
                        xyzk = ops.nodeCoord(node_s[2])
                        xyzl = ops.nodeCoord(node_s[3])
                        nodloads = __quadnodalloads(xyzi, xyzj, xyzk, xyzl, lo[2])

                        for k in range(4):
                            str_tag = str(node_s[k])
                            wx = wy = wz = 0.0
                            if lo[3] == 1:
                                wx = nodloads[k]
                            elif lo[3] == 2:
                                wy = nodloads[k]
                            elif lo[3] == 3:
                                wz = nodloads[k]
                            else:
                                raise ValueError('brick surface loading: ndm = 3 ==> direction should be 1, 2 or 3')
                            str_wx, str_wy, str_wz = str(wx * sfactor), str(wy * sfactor), str(wz * sfactor)
                            str_command = "ops.load(" + str_tag + ", " + str_wx + ", " + str_wy + ", " + str_wz  + ")"
                            if printcommand.lower() in ['y', 'yes']:
                                print(str_command)

                            eval(str_command)
                            file_loading.write(str_command + '\n')

    if len(member.Bodyload) != 0:
        for lo in member.Bodyload:
            if lo[0] == loadpattern:
                elements = member.Elements
                for ele in elements.keys():
                    node_s = elements[ele]
                    xyz1 = ops.nodeCoord(node_s[0])
                    xyz2 = ops.nodeCoord(node_s[1])
                    xyz3 = ops.nodeCoord(node_s[2])
                    xyz4 = ops.nodeCoord(node_s[3])
                    xyz5 = ops.nodeCoord(node_s[4])
                    xyz6 = ops.nodeCoord(node_s[5])
                    xyz7 = ops.nodeCoord(node_s[6])
                    xyz8 = ops.nodeCoord(node_s[7])
                    nodeshares = MyMath.bricknodeshare(xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8)

                    for k in range(8):
                        str_tag = str(node_s[k])
                        wx = wy = wz = 0.0
                        if lo[2] == 1:
                            wx = nodeshares[k] * lo[1]
                        elif lo[2] == 2:
                            wy = nodeshares[k] * lo[1]
                        elif lo[2] == 3:
                            wz = nodeshares[k] * lo[1]
                        else:
                            raise ValueError('brick surface loading: ndm = 3 ==> direction should be 1, 2 or 3')
                        str_wx, str_wy, str_wz = str(wx * sfactor), str(wy * sfactor), str(wz * sfactor)
                        str_command = "ops.load(" + str_tag + ", " + str_wx + ", " + str_wy + ", " + str_wz + ")"
                        if printcommand.lower() in ['y', 'yes']:
                            print(str_command)

                        eval(str_command)
                        file_loading.write(str_command + '\n')

def applyloads(ops, model, *loadpatterns, printcommand='n'):

    lineuniloads = model.LineUniLoads
    quaduniloads = model.QuadUniLoads
    nodeloads = model.NodalLoads
    for loadpattern in loadpatterns:
        if os.path.exists("file_loading_" + loadpattern['Name'] + ".txt"):
            os.remove("file_loading_" + loadpattern['Name'] + ".txt")

        file_loading = open("file_loading_" + loadpattern['Name'] + ".txt", "a")
        file_loading.write("# " + loadpattern['Name'] + '\n')

        print('# Applying Loads: ', loadpattern['Name'])
        str_timeser = str(loadpattern['tsTag'])
        sfactor = loadpattern['scalefactor']
        pattag = loadpattern['Tag']
        if loadpattern['Type'] == 'Plain':
            str_command = "ops.pattern('Plain', " + str(pattag) + ", " + str_timeser + ")"

        if printcommand.lower() in ['y', 'yes']:
            print(str_command)
        file_loading.write(str_command + '\n')
        eval(str_command)
        # eleLoad('-ele', '-type', '-beamUniform', Wy, <Wz>, Wx=0.0)
        for el in lineuniloads.keys():
            if len(lineuniloads[el]) != 0:
                for lo in lineuniloads[el]:
                    if len(lo) != 0:
                        if ndm == 2:
                            wx = wy = 0.0
                            if lo[2] == 1:
                                wx = lo[1]
                            elif lo[2] == 2:
                                wy = lo[1]
                            else:
                                raise ValueError('beam uniform loading: ndm = 2 ==> direction should be 1 or 2')
                        else:
                            wx = wy = wz = 0.0
                            if lo[2] == 1:
                                wx = lo[1]
                            elif lo[2] == 2:
                                wy = lo[1]
                            elif lo[2] == 3:
                                wz = lo[1]
                            else:
                                raise ValueError('beam uniform loading: ndm = 3 ==> direction should be 1, 2 or 3')

                        if lo[0] == loadpattern:
                            str_eletag = str(el)
                            if ndm == 2:
                                str_wx, str_wy = str(wx * sfactor), str(wy * sfactor)
                                str_command = "ops.eleLoad('-ele', " + str_eletag + ", '-type', '-beamUniform', " + \
                                              str_wy + ", " + str_wx + ")"
                            else:
                                str_wx, str_wy, str_wz = str(wx), str(wy * sfactor), str(wz * sfactor)
                                str_command = "ops.eleLoad('-ele', " + str_eletag + ", '-type', '-beamUniform', " + \
                                              str_wy + ", " + str_wz + ", " + str_wx + ")"

                            if printcommand.lower() in ['y', 'yes']:
                                print(str_command)

                            eval(str_command)
                            file_loading.write(str_command + '\n')

        # load(nodeTag, *loadValues)
        for el in quaduniloads.keys():
            if len(quaduniloads[el]) != 0:
                for lo in quaduniloads[el]:
                    if len(lo) != 0:
                        if lo[0] == loadpattern:
                            ele_nodes = ops.eleNodes(el)
                            if len(ele_nodes) == 3:
                                xyzi = ops.nodeCoord(ele_nodes[0])
                                xyzj = ops.nodeCoord(ele_nodes[1])
                                xyzk = ops.nodeCoord(ele_nodes[2])
                                nodloads = __trinodalloads(xyzi, xyzj, xyzk, lo[1])
                                for i in range(3):
                                    str_tag= str(ele_nodes[i])
                                    if ndm == 3:
                                        wx = wy = wz = 0.0
                                        if lo[2] == 1:
                                            wx = nodloads[i]
                                        elif lo[2] == 2:
                                            wy = nodloads[i]
                                        elif lo[2] == 3:
                                            wz = nodloads[i]
                                        else:
                                            raise ValueError('quad uniform loading: ndm = 3 ==> direction should be 1, 2 or 3')
                                        str_wx, str_wy, str_wz = str(wx * sfactor), str(wy * sfactor), str(wz * sfactor)
                                        str_command = "ops.load(" + str_tag + ", " + str_wx + ", " + str_wy + ", " + str_wz + ", 0.0, 0.0, 0.0)"
                                    else:
                                        wx = wy = 0.0
                                        if lo[2] == 1:
                                            wx = nodloads[i]
                                        elif lo[2] == 2:
                                            wy = nodloads[i]
                                        else:
                                            raise ValueError('quad uniform loading: ndm = 2 ==> direction should be 1, 2')
                                        str_wx, str_wy = str(wx * sfactor), str(wy * sfactor)
                                        str_command = "ops.load(" + str_tag + ", " + str_wx + ", " + str_wy + ", 0.0)"

                                    if printcommand.lower() in ['y', 'yes']:
                                        print(str_command)

                                    eval(str_command)
                                    file_loading.write(str_command + '\n')

                            elif len(ele_nodes) in [4, 9]:
                                xyzi = ops.nodeCoord(ele_nodes[0])
                                xyzj = ops.nodeCoord(ele_nodes[1])
                                xyzk = ops.nodeCoord(ele_nodes[2])
                                xyzl = ops.nodeCoord(ele_nodes[3])
                                nodloads = __quadnodalloads(xyzi, xyzj, xyzk, xyzl, lo[1])
                                for i in range(4):
                                    str_tag= str(ele_nodes[i])
                                    if ndm == 3:
                                        wx = wy = wz = 0.0
                                        if lo[2] == 1:
                                            wx = nodloads[i]
                                        elif lo[2] == 2:
                                            wy = nodloads[i]
                                        elif lo[2] == 3:
                                            wz = nodloads[i]
                                        else:
                                            raise ValueError('quad uniform loading: ndm = 3 ==> direction should be 1, 2 or 3')
                                        str_wx, str_wy, str_wz = str(wx * sfactor), str(wy * sfactor), str(wz * sfactor)
                                        str_command = "ops.load(" + str_tag + ", " + str_wx + ", " + str_wy + ", " + str_wz + ", 0.0, 0.0, 0.0)"
                                    else:
                                        wx = wy = 0.0
                                        if lo[2] == 1:
                                            wx = nodloads[i]
                                        elif lo[2] == 2:
                                            wy = nodloads[i]
                                        else:
                                            raise ValueError('quad uniform loading: ndm = 2 ==> direction should be 1, 2')
                                        str_wx, str_wy = str(wx * sfactor), str(wy * sfactor)
                                        str_command = "ops.load(" + str_tag + ", " + str_wx + ", " + str_wy + ", 0.0)"

                                    if printcommand.lower() in ['y', 'yes']:
                                        print(str_command)

                                    eval(str_command)
                                    file_loading.write(str_command + '\n')
        for member in model.Members:
            if isinstance(member, Brick):
                __applybrickloads(ops, member, loadpattern, printcommand,file_loading)

            elif isinstance(member, Point):
                __applypointloads(ops, member, loadpattern, printcommand, file_loading)

        for el in nodeloads:
            pat = el[0]
            xyz = el[1]
            vals = el[2]

            if len(vals) == 0:
                continue

            if pat == loadpattern:
                tag = nodeexist(ops, xyz)
                if tag != False:

                    strvals = " "
                    for f in vals:
                        strvals += ", " + str(f)

                    str_command = "ops.load(" + str(tag) + strvals + ")"

                    if printcommand.lower() in ['y', 'yes']:
                        print(str_command)

                    eval(str_command)
                    file_loading.write(str_command + '\n')

        print('# Applying Loads: ', loadpattern['Name'], 'Done')
        file_loading.close()
def __applypointloads(ops, member, loadpattern, printcommand, file_loading):
    for lo in member.Pointload:
        pat = lo[0]
        vals = lo[1]
        tag = member.NodeTag
        if pat == loadpattern:
            strvals = " "
            if len(vals) != 0:
                for f in vals:
                    strvals += ", " + str(f)

                str_command = "ops.load(" + str(tag) + strvals + ")"

                if printcommand.lower() in ['y', 'yes']:
                    print(str_command)

                eval(str_command)
                file_loading.write(str_command + '\n')

def CopyMember(member, newname):
    newmember = copy.deepcopy(member)
    newmember.Name = newname
    return newmember

def plotmember(ax, member, name = 'n' , propname='y', subdivisions = 'y', linewidth=0.2, edgelinewidth = 0.2, fill='y', coloring='default',
                          fontsize=3,xlim=[], ylim=[],zlim=[], facenumber='n',alpha=0.5):

    for arg in [name, subdivisions, fill, propname]:
        if arg not in ['yes', 'y', 'no', 'n']:
            raise ValueError("name and subdivisions can "
                             "be \"yes\", \"y\",  \"no\" or \"n\" ")

    if coloring not in ['default', 'eleProps', 'eleType']:
        print('coloring can be  \'default\' or \'eleProps\' or \'eleType\'. default will be used ')
        coloring = 'default'

    if len(xlim) not in [0, 2]:
        print('xlim must be an empty list(default) or a list with two float number. default will be used ')
        xlim = []

    if len(zlim) not in [0, 2]:
        print('zlim must be an empty list(default) or a list with two float number. default will be used ')
        zlim = []

    if len(ylim) not in [0, 2]:
        print('ylim must be an empty list(default) or a list with two float number. default will be used ')
        ylim = []

    if isinstance(member, Point):
        xyz = member.XYZ
        plot_ele = True
        if len(xlim) != 0:
            for xx in [xyz[0]]:
                if xx < xlim[0] or xx > xlim[1]:
                    plot_ele = False
        if len(ylim) != 0:
            for yy in [xyz[1]]:
                if yy < ylim[0] or yy > ylim[1]:
                    plot_ele = False
        if len(zlim) != 0:
            for zz in [xyz[2]]:
                if zz < zlim[0] or zz > zlim[1]:
                    plot_ele = False

        if plot_ele == False:
            return

        x = [xyz[0]]
        y = [xyz[1]]
        z = [xyz[2]]

        if name.lower() in ['y', 'yes']:
            ax.text(x, y, z, member.Name, '', size=fontsize, horizontalalignment='center')
        co = 'blue'
        ax.scatter(z, x, y, c=co, s=linewidth * 2, alpha=0.7)

        return

    Nodes, Elements, nodeset = member.createelements()
    if isinstance(member, Brick):
        xyz1 = member.XYZ1
        xyz2 = member.XYZ2
        xyz3 = member.XYZ3
        xyz4 = member.XYZ4
        xyz5 = member.XYZ5
        xyz6 = member.XYZ6
        xyz7 = member.XYZ7
        xyz8 = member.XYZ8

        plot_ele = True
        if len(xlim) != 0:
            for xx in [xyz1[0], xyz2[0], xyz3[0], xyz4[0], xyz5[0], xyz6[0], xyz7[0], xyz8[0]]:
                if xx < xlim[0] or xx > xlim[1]:
                    plot_ele = False
        if len(ylim) != 0:
            for yy in [xyz1[1], xyz2[1], xyz3[1], xyz4[1], xyz5[1], xyz6[1], xyz7[1], xyz8[1]]:
                if yy < ylim[0] or yy > ylim[1]:
                    plot_ele = False
        if len(zlim) != 0:
            for zz in [xyz1[2], xyz2[2], xyz3[2], xyz4[2], xyz5[2], xyz6[2], xyz7[2], xyz8[2]]:
                if zz < zlim[0] or zz > zlim[1]:
                    plot_ele = False

        if plot_ele == False:
            return

        co = 'turquoise'
        if coloring == 'eleProps':
            co = member.EleProps['Color']
        elif coloring == 'eleType':
            co = 'turquoise'
            # if member.EleProps['eleType'] == 'Tri31':
            #     co = 'springgreen'
            # elif member.EleProps['eleType'] in ['ShellMITC4', 'ShellNL', 'ShellDKGQ', 'ShellDKGT', 'ShellNLDKGQ',
            #                                     'ShellNLDKGT']:
            #     co = 'silver'
            # elif member.EleProps['eleType'] in ['bbarQuad', 'quad', 'enhancedQuad',
            #                                     'SSPquad']:
            #     co = 'blueviolet'
        MyMath.plotbrickmember(ax, member, name, propname, subdivisions, edgelinewidth, fill, co, fontsize,facenumber, alpha)

    elif isinstance(member, Polygon):
        xyz = member.XYZ
        XX = []
        YY = []
        ZZ = []
        for coords in xyz:
            XX.append(coords[0])
            YY.append(coords[1])
            ZZ.append(coords[2])
        plot_ele = True
        if len(xlim) != 0:
            for xx in XX:
                if xx < xlim[0] or xx > xlim[1]:
                    plot_ele = False
        if len(ylim) != 0:
            for yy in YY:
                if yy < ylim[0] or yy > ylim[1]:
                    plot_ele = False
        if len(zlim) != 0:
            for zz in ZZ:
                if zz < zlim[0] or zz > zlim[1]:
                    plot_ele = False

        if plot_ele == False:
            return

        if subdivisions.lower() in ['y', 'yes']:
            for ele in Elements.keys():
                if len(Elements[ele]) in [4, 9]:
                    nodei = Elements[ele][0]
                    nodej = Elements[ele][1]
                    nodek = Elements[ele][2]
                    nodel = Elements[ele][3]

                    x = [Nodes[nodei][0], Nodes[nodej][0], Nodes[nodek][0], Nodes[nodel][0], Nodes[nodei][0]]
                    y = [Nodes[nodei][1], Nodes[nodej][1], Nodes[nodek][1], Nodes[nodel][1], Nodes[nodei][1]]
                    z = [Nodes[nodei][2], Nodes[nodej][2], Nodes[nodek][2], Nodes[nodel][2], Nodes[nodei][2]]
                elif len(Elements[ele]) == 3:
                    nodei = Elements[ele][0]
                    nodej = Elements[ele][1]
                    nodek = Elements[ele][2]
                    x = [Nodes[nodei][0], Nodes[nodej][0], Nodes[nodek][0], Nodes[nodei][0]]
                    y = [Nodes[nodei][1], Nodes[nodej][1], Nodes[nodek][1], Nodes[nodei][1]]
                    z = [Nodes[nodei][2], Nodes[nodej][2], Nodes[nodek][2], Nodes[nodei][2]]

                ax.plot(z, x, y, linewidth=edgelinewidth, color='gray')

        if name.lower() in ['y', 'yes']:
            xa = np.average(XX)
            ya = np.average(YY)
            za = np.average(ZZ)
            ax.text(za, xa, ya, member.Name, 'y', size=fontsize, horizontalalignment='center')

        if propname.lower() in ['y', 'yes']:
            prname = member.EleProps['Name']
            xa = np.average(XX)
            ya = np.average(YY)
            za = np.average(ZZ)
            ax.text(za, xa, ya, prname, 'y', size=fontsize, horizontalalignment='center')

        if coloring == 'default':
            co = 'turquoise'
        elif coloring == 'eleProps':
            co = member.EleProps['Color']
        elif coloring == 'eleType':
            co = 'turquoise'
            if member.EleProps['eleType'] == 'Tri31':
                co = 'springgreen'
            elif member.EleProps['eleType'] in ['ShellMITC4', 'ShellNL', 'ShellDKGQ', 'ShellDKGT', 'ShellNLDKGQ',
                                                'ShellNLDKGT']:
                co = 'silver'
            elif member.EleProps['eleType'] in ['bbarQuad', 'quad', 'enhancedQuad',
                                                'SSPquad']:
                co = 'blueviolet'

        if fill.lower() in ['y', 'yes']:
            vertices = [list(zip(ZZ, XX, YY))]
            poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=co, edgecolor='silver')
            ax.add_collection3d(poly)

        x = XX
        x.append(XX[0])
        y = YY
        y.append(YY[0])
        z = ZZ
        z.append(ZZ[0])
        ax.plot(z, x, y, lw=edgelinewidth, color='silver')

    elif isinstance(member, Quad):
        xyzi = member.XYZi
        xyzj = member.XYZj
        xyzk = member.XYZk
        xyzl = member.XYZl
        plot_ele = True
        if len(xlim) != 0:
            for xx in [xyzi[0], xyzj[0], xyzk[0], xyzl[0]]:
                if xx < xlim[0] or xx > xlim[1]:
                    plot_ele = False
        if len(ylim) != 0:
            for yy in [xyzi[1], xyzj[1], xyzk[1], xyzl[1]]:
                if yy < ylim[0] or yy > ylim[1]:
                    plot_ele = False
        if len(zlim) != 0:
            for zz in [xyzi[2], xyzj[2], xyzk[2], xyzl[2]]:
                if zz < zlim[0] or zz > zlim[1]:
                    plot_ele = False

        if plot_ele == False:
            return

        if subdivisions.lower() in ['y', 'yes']:
            for ele in Elements.keys():
                if len(Elements[ele]) in [4, 9]:
                    nodei = Elements[ele][0]
                    nodej = Elements[ele][1]
                    nodek = Elements[ele][2]
                    nodel = Elements[ele][3]
                    x = [Nodes[nodei][0], Nodes[nodej][0], Nodes[nodek][0], Nodes[nodel][0], Nodes[nodei][0]]
                    y = [Nodes[nodei][1], Nodes[nodej][1], Nodes[nodek][1], Nodes[nodel][1], Nodes[nodei][1]]
                    z = [Nodes[nodei][2], Nodes[nodej][2], Nodes[nodek][2], Nodes[nodel][2], Nodes[nodei][2]]
                elif len(Elements[ele]) == 3:
                    nodei = Elements[ele][0]
                    nodej = Elements[ele][1]
                    nodek = Elements[ele][2]
                    x = [Nodes[nodei][0], Nodes[nodej][0], Nodes[nodek][0], Nodes[nodei][0]]
                    y = [Nodes[nodei][1], Nodes[nodej][1], Nodes[nodek][1], Nodes[nodei][1]]
                    z = [Nodes[nodei][2], Nodes[nodej][2], Nodes[nodek][2], Nodes[nodei][2]]

                ax.plot(z, x, y, linewidth=edgelinewidth, color='gray')

        if name.lower() in ['y', 'yes']:
            xa = np.average([xyzi[0], xyzj[0], xyzk[0], xyzl[0]])
            ya = np.average([xyzi[1], xyzj[1], xyzk[1], xyzl[1]])
            za = np.average([xyzi[2], xyzj[2], xyzk[2], xyzl[2]])
            ax.text(za, xa, ya, member.Name, 'y', size=fontsize, horizontalalignment='center')

        if propname.lower() in ['y', 'yes']:
            prname = member.EleProps['Name']
            xa = np.average([xyzi[0], xyzj[0], xyzk[0], xyzl[0]])
            ya = np.average([xyzi[1], xyzj[1], xyzk[1], xyzl[1]])
            za = np.average([xyzi[2], xyzj[2], xyzk[2], xyzl[2]])
            ax.text(za, xa, ya, prname, 'y', size=fontsize, horizontalalignment='center')

        if coloring == 'default':
            co = 'turquoise'
        elif coloring == 'eleProps':
            co = member.EleProps['Color']
        elif coloring == 'eleType':
            co = 'turquoise'
            if member.EleProps['eleType'] == 'Tri31':
                co = 'springgreen'
            elif member.EleProps['eleType'] in ['ShellMITC4', 'ShellNL', 'ShellDKGQ', 'ShellDKGT', 'ShellNLDKGQ',
                                                'ShellNLDKGT']:
                co = 'silver'
            elif member.EleProps['eleType'] in ['bbarQuad', 'quad', 'enhancedQuad',
                                                'SSPquad']:
                co = 'blueviolet'


        if fill.lower() in ['y', 'yes']:
            x = [xyzi[0], xyzj[0], xyzk[0], xyzl[0]]
            y = [xyzi[1], xyzj[1], xyzk[1], xyzl[1]]
            z = [xyzi[2], xyzj[2], xyzk[2], xyzl[2]]
            vertices = [list(zip(z, x, y))]
            poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=co, edgecolor='silver')
            ax.add_collection3d(poly)


        x = [xyzi[0], xyzj[0], xyzk[0], xyzl[0], xyzi[0]]
        y = [xyzi[1], xyzj[1], xyzk[1], xyzl[1], xyzi[1]]
        z = [xyzi[2], xyzj[2], xyzk[2], xyzl[2], xyzi[2]]
        ax.plot(z, x, y, lw=edgelinewidth, color='silver')

    elif isinstance(member, Triangle):
        xyzi = member.XYZi
        xyzj = member.XYZj
        xyzk = member.XYZk

        plot_ele = True
        if len(xlim) != 0:
            for xx in [xyzi[0], xyzj[0], xyzk[0]]:
                if xx < xlim[0] or xx > xlim[1]:
                    plot_ele = False
        if len(ylim) != 0:
            for yy in [xyzi[1], xyzj[1], xyzk[1]]:
                if yy < ylim[0] or yy > ylim[1]:
                    plot_ele = False
        if len(zlim) != 0:
            for zz in [xyzi[2], xyzj[2], xyzk[2]]:
                if zz < zlim[0] or zz > zlim[1]:
                    plot_ele = False

        if plot_ele == False:
            return

        if subdivisions.lower() in ['y', 'yes']:
            for ele in Elements.keys():
                if len(Elements[ele]) in [4, 9]:
                    nodei = Elements[ele][0]
                    nodej = Elements[ele][1]
                    nodek = Elements[ele][2]
                    nodel = Elements[ele][3]
                    x = [Nodes[nodei][0], Nodes[nodej][0], Nodes[nodek][0], Nodes[nodel][0], Nodes[nodei][0]]
                    y = [Nodes[nodei][1], Nodes[nodej][1], Nodes[nodek][1], Nodes[nodel][1], Nodes[nodei][1]]
                    z = [Nodes[nodei][2], Nodes[nodej][2], Nodes[nodek][2], Nodes[nodel][2], Nodes[nodei][2]]
                elif len(Elements[ele]) == 3:
                    nodei = Elements[ele][0]
                    nodej = Elements[ele][1]
                    nodek = Elements[ele][2]
                    x = [Nodes[nodei][0], Nodes[nodej][0], Nodes[nodek][0], Nodes[nodei][0]]
                    y = [Nodes[nodei][1], Nodes[nodej][1], Nodes[nodek][1], Nodes[nodei][1]]
                    z = [Nodes[nodei][2], Nodes[nodej][2], Nodes[nodek][2], Nodes[nodei][2]]

                ax.plot(z, x, y, linewidth=edgelinewidth, color='gray')

        if name.lower() in ['y', 'yes']:
            xa = np.average([xyzi[0], xyzj[0], xyzk[0]])
            ya = np.average([xyzi[1], xyzj[1], xyzk[1]])
            za = np.average([xyzi[2], xyzj[2], xyzk[2]])
            ax.text(za, xa, ya, member.Name, 'y', size=fontsize, horizontalalignment='center')

        if propname.lower() in ['y', 'yes']:
            prname = member.EleProps['Name']
            xa = np.average([xyzi[0], xyzj[0], xyzk[0]])
            ya = np.average([xyzi[1], xyzj[1], xyzk[1]])
            za = np.average([xyzi[2], xyzj[2], xyzk[2]])
            ax.text(za, xa, ya, prname, 'y', size=fontsize, horizontalalignment='center')

        if coloring == 'default':
            co = 'turquoise'
        elif coloring == 'eleProps':
            co = member.EleProps['Color']
        elif coloring == 'eleType':
            co = 'turquoise'
            if member.EleProps['eleType'] == 'Tri31':
                co = 'springgreen'
            elif member.EleProps['eleType'] in ['ShellMITC4', 'ShellNL', 'ShellDKGQ', 'ShellDKGT', 'ShellNLDKGQ',
                                                'ShellNLDKGT']:
                co = 'silver'
            elif member.EleProps['eleType'] in ['bbarQuad', 'quad', 'enhancedQuad',
                                                'SSPquad']:
                co = 'blueviolet'

        if fill.lower() in ['y', 'yes']:
            x = [xyzi[0], xyzj[0], xyzk[0]]
            y = [xyzi[1], xyzj[1], xyzk[1]]
            z = [xyzi[2], xyzj[2], xyzk[2]]
            vertices = [list(zip(z, x, y))]
            poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=co, edgecolor='silver')
            ax.add_collection3d(poly)

        x = [xyzi[0], xyzj[0], xyzk[0], xyzi[0]]
        y = [xyzi[1], xyzj[1], xyzk[1], xyzi[1]]
        z = [xyzi[2], xyzj[2], xyzk[2], xyzi[2]]
        ax.plot(z, x, y, lw=edgelinewidth, color='silver')

    elif isinstance(member, Line):
        xyzi = member.XYZi
        xyzj = member.XYZj
        plot_ele = True
        if len(xlim) != 0:
            for xx in [xyzi[0], xyzj[0]]:
                if xx < xlim[0] or xx > xlim[1]:
                    plot_ele = False
        if len(ylim) != 0:
            for yy in [xyzi[1], xyzj[1]]:
                if yy < ylim[0] or yy > ylim[1]:
                    plot_ele = False
        if len(zlim) != 0:
            for zz in [xyzi[2], xyzj[2]]:
                if zz < zlim[0] or zz > zlim[1]:
                    plot_ele = False

        if plot_ele == False:
            return

        x = [xyzi[0], xyzj[0]]
        y = [xyzi[1], xyzj[1]]
        z = [xyzi[2], xyzj[2]]
        dirz = [xyzj[2] - xyzi[2], xyzj[0] - xyzi[0], xyzj[1] - xyzi[1]]
        if name.lower() in ['y', 'yes']:
            xa = np.average([xyzi[0], xyzj[0]])
            ya = np.average([xyzi[1], xyzj[1]])
            za = np.average([xyzi[2], xyzj[2]])
            ax.text(za, xa, ya, member.Name, dirz, size=fontsize, horizontalalignment='center')

        if propname.lower() in ['y', 'yes']:
            prname = member.EleProps['Name']
            xa = np.average([xyzi[0], xyzj[0]])
            ya = np.average([xyzi[1], xyzj[1]])
            za = np.average([xyzi[2], xyzj[2]])
            ax.text(za, xa, ya, prname, dirz, size=fontsize, horizontalalignment='center')


        if coloring == 'default':
            co = 'royalblue'
        elif coloring == 'eleProps':
            co = member.EleProps['Color']
        elif coloring == 'eleType':
            co = 'royalblue'
            if member.EleProps['eleType'] == 'twoNodeLink':
                co = 'springgreen'
            elif member.EleProps['eleType'] in ['Truss', 'TrussSection', 'corotTruss', 'corotTrussSection']:
                co = 'darkorange'
            elif member.EleProps['eleType'] in ['elasticBeamColumn', 'elasticBeamColumnSec', 'ModElasticBeam2d', 'ElasticTimoshenkoBeam']:
                co = 'blueviolet'
            elif member.EleProps['eleType'] in ['dispBeamColumn']:
                co = 'seagreen'
            elif member.EleProps['eleType'] in ['forceBeamColumn', 'nonlinearBeamColumn']:
                co = 'royalblue'


        ax.plot(z, x, y, lw=linewidth, color=co)

    ax.axis('equal')

def plotopsmodel(ops, ax, elements='y', eletag='n', nodes='y', nodetag='n', linewidth=0.7, edgelineidth=0.3,
                 noesize=1.0,nodecolor='g', fill='y',fontsize=3, xlim=[], ylim=[],zlim=[], alpha=0.9):

    for arg in [nodes, eletag, fill, nodetag, elements]:
        if arg not in ['yes', 'y', 'no', 'n']:
            raise ValueError("name and subdivisions can "
                             "be \"yes\", \"y\",  \"no\" or \"n\" ")

    if len(xlim) not in [0, 2]:
        print('xlim must be an empty list(default) or a list with two float number. default will be used ')
        xlim = []

    if len(zlim) not in [0, 2]:
        print('zlim must be an empty list(default) or a list with two float number. default will be used ')
        zlim = []

    if len(ylim) not in [0, 2]:
        print('ylim must be an empty list(default) or a list with two float number. default will be used ')
        ylim = []


    if os.path.exists('mymodel.txt'):
        os.remove('mymodel.txt')

   ### Plot Nodes
    plotednodes = []
    if nodes.lower() in ['y', 'yes']:
        XX, YY, ZZ = [], [], []
        for nod in ops.getNodeTags():
            xyz = ops.nodeCoord(nod)
            if ndm == 2:
                xyz.append(0.0)

            plot_node = True
            if len(xlim) != 0:
                for xx in [xyz[0]]:
                    if xx < xlim[0] or xx > xlim[1]:
                        plot_node = False
            if len(ylim) != 0:
                for yy in [xyz[1]]:
                    if yy < ylim[0] or yy > ylim[1]:
                        plot_node = False
            if len(zlim) != 0:
                for zz in [xyz[2]]:
                    if zz < zlim[0] or zz > zlim[1]:
                        plot_node = False

            if plot_node != False:
                XX.append(xyz[0])
                YY.append(xyz[1])
                ZZ.append(xyz[2])
                plotednodes.append(nod)
                if nodetag.lower() in ['y', 'yes']:
                    x, y, z = xyz
                    ax.text(z, x, y, str(nod), None, size=fontsize, horizontalalignment='center')

        if len(XX) != 0:
            ax.scatter(ZZ, XX, YY, c=nodecolor, s=noesize, alpha=0.7)

        ### Restraints
        maxDi = max(abs(max(XX) - min(XX)), abs(max(ZZ) - min(ZZ)))
        factor = maxDi / 65
        modelfile = 'mymodel.txt'
        ops.printModel('-file', modelfile)
        cnodes = {}
        with open(modelfile) as f:
            lines = f.readlines()

        for line in lines:
            line2 = line.split(" ")
            if line2[0] == 'SP_Constraint:':
                n = cnodes.get(line2[3])
                if int(line2[3]) not in plotednodes:
                    continue

                if n == None:
                    cnodes[line2[3]] = [line2[5]]
                else:
                    if line2[5] not in n:
                        n.append(line2[5])
                        cnodes[line2[3]] = n
        __plotrestraint(ops, ax, cnodes, factor)

        rnodes = {}
        with open(modelfile) as f:
            lines = f.readlines()

        for line in lines:
            line2 = line.strip().split(" ")
            if line2[0] == 'Node' and line2[1] == 'Constrained:':
                n = rnodes.get(line2[5])
                if int(line2[5]) not in plotednodes:
                    continue

                if n == None:
                    rnodes[line2[5]] = [line2[2]]
                else:
                    if line2[2] not in n:
                        n.append(line2[2])
                        rnodes[line2[5]] = n

        __plotrigiddiaph(ops, ax, rnodes)
        ### Plot Elements
    if elements.lower() in ['y', 'yes']:
        Xzero = []
        Yzero = []
        Zzero = []
        Tzero = []
        for ele in ops.getEleTags():
            elenodes = ops.eleNodes(ele)
            if len(elenodes) == 2:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                if ndm == 2 :
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                plot_ele = True
                if len(xlim) != 0:
                    for xx in [xyzi[0], xyzj[0]]:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in [xyzi[1], xyzj[1]]:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in [xyzi[2], xyzj[2]]:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    x = [xyzi[0], xyzj[0]]
                    y = [xyzi[1], xyzj[1]]
                    z = [xyzi[2], xyzj[2]]
                    co = 'royalblue'
                    if xyzi[0] == xyzj[0] and xyzi[1] == xyzj[1] and xyzi[2] == xyzj[2]:
                        Xzero.append(x[0])
                        Yzero.append(y[0])
                        Zzero.append(z[0])
                        Tzero.append(ele)
                        continue
                    if eletag.lower() in ['y', 'yes']:
                        xa = np.average([xyzi[0], xyzj[0]])
                        ya = np.average([xyzi[1], xyzj[1]])
                        za = np.average([xyzi[2], xyzj[2]])
                        ax.text(za, xa, ya, str(ele), '', size=fontsize, horizontalalignment='center')

                    ax.plot(z, x, y, lw=linewidth, color=co)

            elif len(elenodes) == 3:

                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                xyzk = ops.nodeCoord(elenodes[2])

                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    xyzk.append(0.0)

                plot_ele = True
                if len(xlim) != 0:
                    for xx in [xyzi[0], xyzj[0], xyzk[0]]:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in [xyzi[1], xyzj[1], xyzk[1]]:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in [xyzi[2], xyzj[2], xyzk[2]]:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    co = 'turquoise'
                    if fill.lower() in ['y', 'yes']:
                        x = [xyzi[0], xyzj[0], xyzk[0]]
                        y = [xyzi[1], xyzj[1], xyzk[1]]
                        z = [xyzi[2], xyzj[2], xyzk[2]]
                        vertices = [list(zip(z, x, y))]
                        poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelineidth, color=co, edgecolor='gray')
                        ax.add_collection3d(poly)
                    else:
                        x = [xyzi[0], xyzj[0], xyzk[0], xyzi[0]]
                        y = [xyzi[1], xyzj[1], xyzk[1], xyzi[1]]
                        z = [xyzi[2], xyzj[2], xyzk[2], xyzi[2]]
                        ax.plot(z, x, y, lw=edgelineidth, color='silver')

                    if eletag.lower() in ['y', 'yes']:
                        xa = np.average([xyzi[0], xyzj[0], xyzk[0]])
                        ya = np.average([xyzi[1], xyzj[1], xyzk[1]])
                        za = np.average([xyzi[2], xyzj[2], xyzk[2]])
                        ax.text(za, xa, ya, str(ele), None, size=fontsize, horizontalalignment='center')
            elif len(elenodes) in [4, 9]:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                xyzk = ops.nodeCoord(elenodes[2])
                xyzl = ops.nodeCoord(elenodes[3])
                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    xyzk.append(0.0)
                    xyzl.append(0.0)
                plot_ele = True
                if len(xlim) != 0:
                    for xx in [xyzi[0], xyzj[0], xyzk[0], xyzl[0]]:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in [xyzi[1], xyzj[1], xyzk[1], xyzl[1]]:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in [xyzi[2], xyzj[2], xyzk[2], xyzl[2]]:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    co = 'turquoise'
                    if fill.lower() in ['y', 'yes']:
                        x = [xyzi[0], xyzj[0], xyzk[0], xyzl[0]]
                        y = [xyzi[1], xyzj[1], xyzk[1], xyzl[1]]
                        z = [xyzi[2], xyzj[2], xyzk[2], xyzl[2]]
                        vertices = [list(zip(z, x, y))]
                        poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelineidth, color=co, edgecolor='gray')
                        ax.add_collection3d(poly)
                    else:
                        x = [xyzi[0], xyzj[0], xyzk[0], xyzl[0], xyzi[0]]
                        y = [xyzi[1], xyzj[1], xyzk[1], xyzl[1], xyzi[1]]
                        z = [xyzi[2], xyzj[2], xyzk[2], xyzl[2], xyzi[2]]
                        ax.plot(z, x, y, lw=edgelineidth, color='silver')

                    if eletag.lower() in ['y', 'yes']:
                        xa = np.average([xyzi[0], xyzj[0], xyzk[0], xyzl[0]])
                        ya = np.average([xyzi[1], xyzj[1], xyzk[1], xyzl[1]])
                        za = np.average([xyzi[2], xyzj[2], xyzk[2], xyzl[2]])
                        ax.text(za, xa, ya, str(ele), None, size=fontsize, horizontalalignment='center')
            elif len(elenodes) == 8:
                xyz1 = ops.nodeCoord(elenodes[0])
                xyz2 = ops.nodeCoord(elenodes[1])
                xyz3 = ops.nodeCoord(elenodes[2])
                xyz4 = ops.nodeCoord(elenodes[3])
                xyz5 = ops.nodeCoord(elenodes[4])
                xyz6 = ops.nodeCoord(elenodes[5])
                xyz7 = ops.nodeCoord(elenodes[6])
                xyz8 = ops.nodeCoord(elenodes[7])
                plot_ele = True
                if len(xlim) != 0:
                    for xx in [xyz1[0], xyz2[0], xyz3[0], xyz4[0], xyz5[0], xyz6[0], xyz7[0], xyz8[0]]:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in [xyz1[1], xyz2[1], xyz3[1], xyz4[1], xyz5[1], xyz6[1], xyz7[1], xyz8[1]]:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in [xyz1[2], xyz2[2], xyz3[2], xyz4[2], xyz5[2], xyz6[2], xyz7[2], xyz8[2]]:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    if eletag.lower() in ['y', 'yes']:
                        xa = np.average([xyz1[0], xyz2[0], xyz3[0], xyz4[0], xyz5[0], xyz6[0], xyz7[0], xyz8[0]])
                        ya = np.average([xyz1[1], xyz2[1], xyz3[1], xyz4[1], xyz5[1], xyz6[1], xyz7[1], xyz8[1]])
                        za = np.average([xyz1[2], xyz2[2], xyz3[2], xyz4[2], xyz5[2], xyz6[2], xyz7[2], xyz8[2]])
                        ax.text(za, xa, ya, str(ele), None, size=fontsize, horizontalalignment='center')

                    co = 'turquoise'
                    MyMath.plotcube(ax, xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8, edgelineidth,co , fill,'gray', alpha=alpha)

            else:
                print('Are not supported')


        # ax.scatter(Zzero, Xzero, Yzero, c='r', s=linewidth * 2, alpha=0.7)
        # Tzero.append(ele)

    ax.axis('equal')
def __plotrestraint(ops, ax,  cnodes, fac):
    for nod, valls in cnodes.items():
        xyz = ops.nodeCoord(int(nod))
        dirs = [int(x) for x in valls]
        for dir in dirs:
            if dir == 1:
                x = [xyz[0], xyz[0] - fac, xyz[0] - fac]
                y = [xyz[1], xyz[1] - fac*0.75, xyz[1] + fac*0.75]
                z = [xyz[2], xyz[2], xyz[2]]
                co = 'r'
            elif dir == 2:
                x = [xyz[0], xyz[0] + fac*0.75, xyz[0] - fac*0.75]
                y = [xyz[1], xyz[1] - fac, xyz[1] - fac]
                z = [xyz[2], xyz[2], xyz[2]]
                co = 'g'
            elif dir == 3:
                x = [xyz[0], xyz[0], xyz[0]]
                y = [xyz[1], xyz[1] + fac*0.75, xyz[1] - fac*0.75]
                z = [xyz[2], xyz[2] - fac, xyz[2] - fac]
                co = 'b'
            elif dir == 4:
                x = [xyz[0], xyz[0], xyz[0] - fac, xyz[0] - fac, xyz[0]]
                y = [xyz[1] - fac*1.5, xyz[1] , xyz[1], xyz[1] - fac*1.5, xyz[1] - fac*1.5]
                z = [xyz[2], xyz[2], xyz[2], xyz[2]]
                co = 'r'
            elif dir == 5:
                x = [xyz[0] - fac*1.5, xyz[0] , xyz[0] , xyz[0] - fac*1.5, xyz[0] - fac*1.5]
                y = [xyz[1], xyz[1], xyz[1] - fac, xyz[1] - fac, xyz[1]]
                z = [xyz[2], xyz[2], xyz[2], xyz[2], xyz[2]]
                co = 'g'
            elif dir == 6:
                x = [xyz[0], xyz[0], xyz[0], xyz[0], xyz[0]]
                y = [xyz[1], xyz[1], xyz[1] - fac*1.5, xyz[1] - fac*1.5, xyz[1]]
                z = [xyz[2], xyz[2] - fac, xyz[2] - fac, xyz[2], xyz[2]]
                co = 'b'

            vertices = [list(zip(z, x, y))]
            poly = Poly3DCollection(vertices, alpha=0.5, linewidth=0.0, color=co, edgecolor='gray')
            ax.add_collection3d(poly)

def __plotrigiddiaph(ops, ax, rnodes):
    for rnod, valls in rnodes.items():
        xi, yi, zi = ops.nodeCoord(int(rnod))
        for cnode in valls:
            xj, yj, zj = ops.nodeCoord(int(cnode))
            x = [xi, xj]
            y = [yi, yj]
            z = [zi, zj]
            ax.plot(z, x, y, lw=0.5, color='0.7', linestyle='dashed')

def plotdeformedshape(ops, ax,scale=10, lineelements='y', quadtrielements='y', brickelements='y', linewidth=0.7, edgelineidth=0.3,
                 fill='y', xlim=[], ylim=[],zlim=[], alpha=0.9):

    for arg in [fill, lineelements]:
        if arg not in ['yes', 'y', 'no', 'n']:
            raise ValueError("name and subdivisions can "
                             "be \"yes\", \"y\",  \"no\" or \"n\" ")

    if len(xlim) not in [0, 2]:
        print('xlim must be an empty list(default) or a list with two float number. default will be used ')
        xlim = []

    if len(zlim) not in [0, 2]:
        print('zlim must be an empty list(default) or a list with two float number. default will be used ')
        zlim = []

    if len(ylim) not in [0, 2]:
        print('ylim must be an empty list(default) or a list with two float number. default will be used ')
        ylim = []

        ### Plot Elements
    # if elements.lower() in ['y', 'yes']:
    for ele in ops.getEleTags():
        elenodes = ops.eleNodes(ele)
        if lineelements.lower() in ['y', 'yes']:
            if len(elenodes) == 2:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                dispi = ops.nodeDisp(elenodes[0])
                dispj = ops.nodeDisp(elenodes[1])
                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    dispi[2] = 0.0
                    dispj[2] = 0.0

                plot_ele = True
                if len(xlim) != 0:
                    for xx in [xyzi[0], xyzj[0]]:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in [xyzi[1], xyzj[1]]:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in [xyzi[2], xyzj[2]]:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0]]
                    y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1]]
                    z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2]]
                    co = 'r'
                    ax.plot(z, x, y, lw=linewidth, color=co)

        if quadtrielements.lower() in ['y', 'yes']:
            if len(elenodes) == 3:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                xyzk = ops.nodeCoord(elenodes[2])
                dispi = ops.nodeDisp(elenodes[0])
                dispj = ops.nodeDisp(elenodes[1])
                dispk = ops.nodeDisp(elenodes[2])
                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    xyzk.append(0.0)
                    dispi[2] = 0.0
                    dispj[2] = 0.0
                    dispk[2] = 0.0
                plot_ele = True
                if len(xlim) != 0:
                    for xx in [xyzi[0], xyzj[0], xyzk[0]]:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in [xyzi[1], xyzj[1], xyzk[1]]:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in [xyzi[2], xyzj[2], xyzk[2]]:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    co = 'r'
                    if fill.lower() in ['y', 'yes']:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2]]
                        vertices = [list(zip(z, x, y))]
                        poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelineidth, color=co, edgecolor='gray')
                        ax.add_collection3d(poly)
                    else:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0], xyzi[0] + scale * dispi[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1],xyzi[1] + scale * dispi[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2],xyzi[2] + scale * dispi[2]]
                        ax.plot(z, x, y, lw=edgelineidth, color='silver')

            elif len(elenodes) in [4, 9]:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                xyzk = ops.nodeCoord(elenodes[2])
                xyzl = ops.nodeCoord(elenodes[3])
                dispi = ops.nodeDisp(elenodes[0])
                dispj = ops.nodeDisp(elenodes[1])
                dispk = ops.nodeDisp(elenodes[2])
                displ = ops.nodeDisp(elenodes[3])
                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    xyzk.append(0.0)
                    xyzl.append(0.0)
                    dispi[2] = 0.0
                    dispj[2] = 0.0
                    dispk[2] = 0.0
                    displ[2] = 0.0
                plot_ele = True
                if len(xlim) != 0:
                    for xx in [xyzi[0], xyzj[0], xyzk[0], xyzl[0]]:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in [xyzi[1], xyzj[1], xyzk[1], xyzl[1]]:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in [xyzi[2], xyzj[2], xyzk[2], xyzl[2]]:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    co = 'turquoise'
                    if fill.lower() in ['y', 'yes']:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0], xyzl[0] + scale * displ[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1], xyzl[1] + scale * displ[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2], xyzl[2] + scale * displ[2]]
                        vertices = [list(zip(z, x, y))]
                        poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelineidth, color=co, edgecolor='gray')
                        ax.add_collection3d(poly)
                    else:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0],
                             xyzl[0] + scale * displ[0], xyzi[0] + scale * dispi[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1],
                             xyzl[1] + scale * displ[1], xyzi[1] + scale * dispi[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2],
                             xyzl[2] + scale * displ[2], xyzi[2] + scale * dispi[2]]
                        ax.plot(z, x, y, lw=edgelineidth, color='r')

        if brickelements.lower() in ['y', 'yes']:
            if len(elenodes) == 8:
                xyz = []
                disp = []
                xyz.append(ops.nodeCoord(elenodes[0]))
                xyz.append(ops.nodeCoord(elenodes[1]))
                xyz.append(ops.nodeCoord(elenodes[2]))
                xyz.append(ops.nodeCoord(elenodes[3]))
                xyz.append(ops.nodeCoord(elenodes[4]))
                xyz.append(ops.nodeCoord(elenodes[5]))
                xyz.append(ops.nodeCoord(elenodes[6]))
                xyz.append(ops.nodeCoord(elenodes[7]))
                disp.append(ops.nodeDisp(elenodes[0]))
                disp.append(ops.nodeDisp(elenodes[1]))
                disp.append(ops.nodeDisp(elenodes[2]))
                disp.append(ops.nodeDisp(elenodes[3]))
                disp.append(ops.nodeDisp(elenodes[4]))
                disp.append(ops.nodeDisp(elenodes[5]))
                disp.append(ops.nodeDisp(elenodes[6]))
                disp.append(ops.nodeDisp(elenodes[7]))
                XX = []
                YY = []
                ZZ = []
                for cords in xyz:
                    XX.append(cords[0])
                    YY.append(cords[1])
                    ZZ.append(cords[2])
                plot_ele = True
                if len(xlim) != 0:
                    for xx in XX:
                        if xx < xlim[0] or xx > xlim[1]:
                            plot_ele = False
                if len(ylim) != 0:
                    for yy in YY:
                        if yy < ylim[0] or yy > ylim[1]:
                            plot_ele = False
                if len(zlim) != 0:
                    for zz in ZZ:
                        if zz < zlim[0] or zz > zlim[1]:
                            plot_ele = False

                if plot_ele != False:
                    xyzd =[]
                    for i in range(len(xyz)):
                        x = xyz[i][0] + scale * disp[i][0]
                        y = xyz[i][1] + scale * disp[i][1]
                        z = xyz[i][2] + scale * disp[i][2]
                        xyzd.append([x, y, z])
                    co = 'gray'
                    MyMath.plotcube(ax, xyzd[0], xyzd[1], xyzd[2], xyzd[3], xyzd[4], xyzd[5], xyzd[6], xyzd[7], edgelineidth,co , fill,'r', alpha=alpha)

def plotmodeshape(ops, ax, modenumber=1, scale=10, lineelements='y', quadtrielements='y', brickelements='y', linewidth=0.7, edgelineidth=0.3,
                 fill='y', alpha=0.9):

    for arg in [fill, lineelements]:
        if arg not in ['yes', 'y', 'no', 'n']:
            raise ValueError("name and subdivisions can "
                             "be \"yes\", \"y\",  \"no\" or \"n\" ")

    for ele in ops.getEleTags():
        elenodes = ops.eleNodes(ele)
        if lineelements.lower() in ['y', 'yes']:
            if len(elenodes) == 2:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                dispi = ops.nodeEigenvector(elenodes[0], modenumber)
                dispj = ops.nodeEigenvector(elenodes[1], modenumber)
                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    dispi[2] = 0.0
                    dispj[2] = 0.0

                plot_ele = True

                if plot_ele != False:
                    x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0]]
                    y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1]]
                    z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2]]
                    co = 'r'
                    ax.plot(z, x, y, lw=linewidth, color=co)

        if quadtrielements.lower() in ['y', 'yes']:
            if len(elenodes) == 3:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                xyzk = ops.nodeCoord(elenodes[2])
                dispi = ops.nodeEigenvector(elenodes[0], modenumber)
                dispj = ops.nodeEigenvector(elenodes[1], modenumber)
                dispk = ops.nodeEigenvector(elenodes[2], modenumber)
                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    xyzk.append(0.0)
                    dispi[2] = 0.0
                    dispj[2] = 0.0
                    dispk[2] = 0.0
                plot_ele = True
                if plot_ele != False:
                    co = 'r'
                    if fill.lower() in ['y', 'yes']:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2]]
                        vertices = [list(zip(z, x, y))]
                        poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelineidth, color=co, edgecolor='gray')
                        ax.add_collection3d(poly)
                    else:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0], xyzi[0] + scale * dispi[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1],xyzi[1] + scale * dispi[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2],xyzi[2] + scale * dispi[2]]
                        ax.plot(z, x, y, lw=edgelineidth, color='silver')

            elif len(elenodes) in [4, 9]:
                xyzi = ops.nodeCoord(elenodes[0])
                xyzj = ops.nodeCoord(elenodes[1])
                xyzk = ops.nodeCoord(elenodes[2])
                xyzl = ops.nodeCoord(elenodes[3])
                dispi = ops.nodeEigenvector(elenodes[0], modenumber)
                dispj = ops.nodeEigenvector(elenodes[1], modenumber)
                dispk = ops.nodeEigenvector(elenodes[2], modenumber)
                displ = ops.nodeEigenvector(elenodes[3], modenumber)
                if ndm == 2:
                    xyzi.append(0.0)
                    xyzj.append(0.0)
                    xyzk.append(0.0)
                    xyzl.append(0.0)
                    dispi[2] = 0.0
                    dispj[2] = 0.0
                    dispk[2] = 0.0
                    displ[2] = 0.0
                plot_ele = True
                if plot_ele != False:
                    co = 'turquoise'
                    if fill.lower() in ['y', 'yes']:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0], xyzl[0] + scale * displ[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1], xyzl[1] + scale * displ[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2], xyzl[2] + scale * displ[2]]
                        vertices = [list(zip(z, x, y))]
                        poly = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelineidth, color=co, edgecolor='gray')
                        ax.add_collection3d(poly)
                    else:
                        x = [xyzi[0] + scale * dispi[0], xyzj[0] + scale * dispj[0], xyzk[0] + scale * dispk[0],
                             xyzl[0] + scale * displ[0], xyzi[0] + scale * dispi[0]]
                        y = [xyzi[1] + scale * dispi[1], xyzj[1] + scale * dispj[1], xyzk[1] + scale * dispk[1],
                             xyzl[1] + scale * displ[1], xyzi[1] + scale * dispi[1]]
                        z = [xyzi[2] + scale * dispi[2], xyzj[2] + scale * dispj[2], xyzk[2] + scale * dispk[2],
                             xyzl[2] + scale * displ[2], xyzi[2] + scale * dispi[2]]
                        ax.plot(z, x, y, lw=edgelineidth, color='r')

        if brickelements.lower() in ['y', 'yes']:
            if len(elenodes) == 8:
                xyz = []
                disp = []
                xyz.append(ops.nodeCoord(elenodes[0]))
                xyz.append(ops.nodeCoord(elenodes[1]))
                xyz.append(ops.nodeCoord(elenodes[2]))
                xyz.append(ops.nodeCoord(elenodes[3]))
                xyz.append(ops.nodeCoord(elenodes[4]))
                xyz.append(ops.nodeCoord(elenodes[5]))
                xyz.append(ops.nodeCoord(elenodes[6]))
                xyz.append(ops.nodeCoord(elenodes[7]))
                disp.append(ops.nodeEigenvector(elenodes[0], modenumber))
                disp.append(ops.nodeEigenvector(elenodes[1], modenumber))
                disp.append(ops.nodeEigenvector(elenodes[2], modenumber))
                disp.append(ops.nodeEigenvector(elenodes[3], modenumber))
                disp.append(ops.nodeEigenvector(elenodes[4], modenumber))
                disp.append(ops.nodeEigenvector(elenodes[5], modenumber))
                disp.append(ops.nodeEigenvector(elenodes[6], modenumber))
                disp.append(ops.nodeEigenvector(elenodes[7], modenumber))
                XX = []
                YY = []
                ZZ = []
                for cords in xyz:
                    XX.append(cords[0])
                    YY.append(cords[1])
                    ZZ.append(cords[2])
                plot_ele = True
                if plot_ele != False:
                    xyzd =[]
                    for i in range(len(xyz)):
                        x = xyz[i][0] + scale * disp[i][0]
                        y = xyz[i][1] + scale * disp[i][1]
                        z = xyz[i][2] + scale * disp[i][2]
                        xyzd.append([x, y, z])
                    co = 'gray'
                    MyMath.plotcube(ax, xyzd[0], xyzd[1], xyzd[2], xyzd[3], xyzd[4], xyzd[5], xyzd[6], xyzd[7], edgelineidth,co , fill,'r', alpha=alpha)

def plotcoordaxis(ax, linewidth=0.2, length=0, fontsize=2):

    if length <= 0:
        xl = ax.get_xlim()
        yl = ax.get_ylim()
        dx = xl[1] - xl[0]
        dy = yl[1] - yl[0]
        h = min((dx,dy))
        length = h/15

    ax.quiver([0], [0], [0], [0], [2], [0], color='red',length=length, normalize=True, linewidth=linewidth)
    ax.quiver([0], [0], [0], [0], [0], [2], color='g', length=length, normalize=True, linewidth=linewidth)
    ax.quiver([0], [0], [0], [2], [0], [0], color='b',length=length, normalize=True, linewidth=linewidth)
    ax.text(0, 1.05 * length, 0, 'X', None, fontsize=fontsize, color='red',verticalalignment='center')
    ax.text(0, 0, 1.05 * length, 'Y', None, fontsize=fontsize, color='g')
    ax.text(1.05 * length, 0, 0, 'Z', None, fontsize=fontsize, color='b',verticalalignment='center')

def nodeexist(ops,xyz):
    nodes = ops.getNodeTags()
    if ndm == 3:
        x, y, z = xyz
    elif ndm == 2:
        x, y = xyz[0], xyz[1]
        z = 0
    exist = False

    for nod in nodes:
        if ndm == 3:
            xn, yn, zn = ops.nodeCoord(nod)
        elif ndm == 2:
            xn, yn = ops.nodeCoord(nod)
            zn = 0

        if (abs(x - xn) + abs(y - yn) + abs(z - zn)) < tolerance:
            exist = nod
            break
    return exist

def __quadnodalloads(xyzi, xyzj, xyzk, xyzl, w):
    xi, yi, zi = xyzi
    xj, yj, zj = xyzj
    xk, yk, zk = xyzk
    xl, yl, zl = xyzl

    # midpoint coords

    xm, ym, zm = (xj + xi) / 2, (yj + yi) / 2, (zj + zi) / 2
    xn, yn, zn = (xj + xk) / 2, (yj + yk) / 2, (zj + zk) / 2
    xo, yo, zo = (xk + xl) / 2, (yk + yl) / 2, (zk + zl) / 2
    xp, yp, zp = (xl + xi) / 2, (yl + yi) / 2, (zl + zi) / 2
    xq, yq, zq = (xo + xm) / 2,  (yo + ym) / 2,  (zo + zm) / 2

    # node i
    im = [xm - xi, ym - yi, zm - zi]
    iq = [xq - xi, yq - yi, zq - zi]
    ip = [xp - xi, yp - yi, zp - zi]
    a1 = np.cross(im, iq)
    ar1 = np.sqrt(a1[0] ** 2 + a1[1] ** 2 + a1[2] ** 2) / 2
    a2 = np.cross(iq, ip)
    ar2 = np.sqrt(a2[0] ** 2 + a2[1] ** 2 + a2[2] ** 2) / 2
    ari = ar1 + ar2

    # node j
    jm = [xm - xj, ym - yj, zm - zj]
    jq = [xq - xj, yq - yj, zq - zj]
    jn = [xn - xj, yn - yj, zn - zj]
    a1 = np.cross(jn, jq)
    ar1 = np.sqrt(a1[0] ** 2 + a1[1] ** 2 + a1[2] ** 2) / 2
    a2 = np.cross(jq, jm)
    ar2 = np.sqrt(a2[0] ** 2 + a2[1] ** 2 + a2[2] ** 2) / 2
    arj = ar1 + ar2

    # node k
    kn = [xn - xk, yn - yk, zn - zk]
    kq = [xq - xk, yq - yk, zq - zk]
    ko = [xo - xk, yo - yk, zo - zk]
    a1 = np.cross(kn, kq)
    ar1 = np.sqrt(a1[0] ** 2 + a1[1] ** 2 + a1[2] ** 2) / 2
    a2 = np.cross(kq, ko)
    ar2 = np.sqrt(a2[0] ** 2 + a2[1] ** 2 + a2[2] ** 2) / 2
    ark = ar1 + ar2

    # node l
    lo = [xo - xl, yo - yl, zo - zl]
    lq = [xq - xl, yq - yl, zq - zl]
    lp = [xp - xl, yp - yl, zp - zl]
    a1 = np.cross(lo, lq)
    ar1 = np.sqrt(a1[0] ** 2 + a1[1] ** 2 + a1[2] ** 2) / 2
    a2 = np.cross(lq, lp)
    ar2 = np.sqrt(a2[0] ** 2 + a2[1] ** 2 + a2[2] ** 2) / 2
    arl = ar1 + ar2

    return [w * ari, w * arj, w * ark, w * arl]

def __trinodalloads(xyzi, xyzj, xyzk, w):
    xi, yi, zi = xyzi
    xj, yj, zj = xyzj
    xk, yk, zk = xyzk

    ij = [xj - xi, yj - yi, zj - zi]
    ik = [xk - xi, yk - yi, zk - zi]

    a = np.cross(ij, ik)
    ar = np.sqrt(a[0] ** 2 + a[1] ** 2 + a[2] ** 2) / 2
    # node i
    return [w * ar / 3, w * ar / 3, w * ar / 3]

def eigen(ops, num_Modes, solver='-genBandArpack'):
    lambdaN = ops.eigen(solver, num_Modes)
    omega = []
    Tn = []
    for i in range(num_Modes):
        lambdaI = lambdaN[i]
        omega.append(pow(lambdaI, 0.5))
        Tn.append((2 * np.pi) / pow(lambdaI, 0.5))

    return lambdaN, omega, Tn

def damping(ops, xDamp, T1=0, T2=0, factor_betaK = 0.0, factor_betaKinit= 0.0, factor_betaKcomm= 1.0,
            xlim=[], ylim=[], zlim=[], solver='-genBandArpack'):

    if T1 == 0 or T2 == 0:
        lambdaN, omega, Tn = eigen(ops, 2, solver=solver)
        omegaI, omegaJ = omega
    else:
        omegaI, omegaJ = (2 * np.pi) / T1, (2 * np.pi) / T2
        lambdaN = [omegaI ** 2, omegaJ ** 2]
        Tn = [T1, T2]
        omega = [omegaI, omegaJ]

    alphaM = xDamp * (2 * omegaI * omegaJ) / (omegaI + omegaJ)
    betaSt = 2 * (xDamp / (omegaI + omegaJ))

    if len(xlim) == 0 and len(ylim) == 0 and len(zlim) == 0:
        ops.rayleigh(alphaM, factor_betaK * betaSt, factor_betaKinit * betaSt, factor_betaKcomm * betaSt)
    else:
        dnodes = findnodes(ops, xlim, ylim, zlim)
        if dnodes == False:
            return

        delements = findelements(ops, xlim, ylim, zlim)
        if delements == False:
            return

        ops.region(1, '-ele', *delements, '-rayleigh', 0.0, factor_betaK * betaSt,
                   factor_betaKinit * betaSt, factor_betaKcomm * betaSt)
        ops.region(2, '-node', *dnodes, '-rayleigh', alphaM, 0.0, 0.0, 0.0)

    return alphaM, betaSt, lambdaN, omega, Tn

def findnode(ops, xyz):
    nodes = ops.getNodeTags()
    if ndm == 3:
        x, y, z = xyz
    elif ndm == 2:
        x, y = xyz[0], xyz[1]
        z = 0

    nodeTags = []
    for nod in nodes:
        if ndm == 3:
            xn, yn, zn = ops.nodeCoord(nod)
        elif ndm == 2:
            xn, yn = ops.nodeCoord(nod)
            zn = 0

        if (abs(x - xn) + abs(y - yn) + abs(z - zn)) < tolerance:
            nodeTags.append(nod)
    if len(nodeTags) == 0:
        return False
    elif len(nodeTags) == 1:
        return nodeTags[0]
    else:
        return nodeTags

def findnodes(ops, xlim=[], ylim=[], zlim=[]):

    if len(xlim) not in [0, 2]:
        print('xlim must be an empty list(default) or a list with two float number. default will be used ')
        xlim = []

    if len(zlim) not in [0, 2]:
        print('zlim must be an empty list(default) or a list with two float number. default will be used ')
        zlim = []

    if len(ylim) not in [0, 2]:
        print('ylim must be an empty list(default) or a list with two float number. default will be used ')
        ylim = []

    nodeTags = []
    for nod in ops.getNodeTags():
        xyz = ops.nodeCoord(nod)
        if ndm == 2:
            xyz.append(0.0)

        add_node = True
        if len(xlim) != 0:
            for xx in [xyz[0]]:
                if xx < xlim[0] or xx > xlim[1]:
                    add_node = False
        if len(ylim) != 0:
            for yy in [xyz[1]]:
                if yy < ylim[0] or yy > ylim[1]:
                    add_node = False
        if len(zlim) != 0:
            for zz in [xyz[2]]:
                if zz < zlim[0] or zz > zlim[1]:
                    add_node = False

        if add_node != False:
            nodeTags.append(nod)

    if len(nodeTags) == 0:
            return False
    else:
        return nodeTags


def findelements(ops, xlim=[], ylim=[], zlim=[]):
    if len(xlim) not in [0, 2]:
        print('xlim must be an empty list(default) or a list with two float number. default will be used ')
        xlim = []

    if len(zlim) not in [0, 2]:
        print('zlim must be an empty list(default) or a list with two float number. default will be used ')
        zlim = []

    if len(ylim) not in [0, 2]:
        print('ylim must be an empty list(default) or a list with two float number. default will be used ')
        ylim = []

    eleTags = []
    for ele in ops.getEleTags():
        elenodes = ops.eleNodes(ele)
        XX = []
        YY = []
        ZZ = []
        for nod in elenodes:
            xyz = ops.nodeCoord(nod)
            XX.append(xyz[0])
            YY.append(xyz[1])
            if ndm == 2:
                ZZ.append(0.0)
            else:
                ZZ.append(xyz[2])

        add_ele = True
        if len(xlim) != 0:
            for xx in [XX]:
                if xx < xlim[0] or xx > xlim[1]:
                    add_ele = False
        if len(ylim) != 0:
            for yy in [YY]:
                if yy < ylim[0] or yy > ylim[1]:
                    add_ele = False
        if len(zlim) != 0:
            for zz in [ZZ]:
                if zz < zlim[0] or zz > zlim[1]:
                    add_ele = False

        if add_ele != False:
            eleTags.append(ele)

    if len(eleTags) == 0:
        return False
    else:
        return eleTags


def converttoline(xyz, length, dir, lineprop, numDiv=1, number=1):
    name = 'line'
    if ndm == 2:
        ux, uy, uz = dir[0], dir[1], 0
        lu = np.sqrt(ux ** 2 + uy ** 2 + uz ** 2)
        ux, uy, uz = ux * length / lu, uy * length / lu, uz * length / lu
        x, y, z = xyz[0], xyz[1], 0
    else:
        ux, uy, uz = dir
        lu = np.sqrt(ux ** 2 + uy ** 2 + uz ** 2)
        ux, uy, uz = ux * length / lu, uy * length / lu, uz * length / lu
        x, y, z = xyz

    lines = []
    for n in range(number):
        lname = name + "_" + str(n+1)
        xyzi = [x + n * ux, y + n * uy, z + n * uz]
        xyzj = [x + (n + 1) * ux, y + (n + 1) * uy, z + (n + 1) * uz]
        lines.append(Line(lname, lineprop, xyzi, xyzj, numDiv))

    return lines

def converttoquad(line, length, dir, quadprop, numDivij=1, numDivjk=1, number=1):
    name = 'quad'
    xyzi_l = line.XYZi
    xyzj_l = line.XYZj
    if ndm == 2:
        ux, uy, uz = dir[0], dir[1], 0
        lu = np.sqrt(ux ** 2 + uy ** 2 + uz ** 2)
        ux, uy, uz = ux * length / lu, uy * length / lu, uz * length / lu
        xi_l, yi_l, zi_l = xyzi_l[0], xyzi_l[1], 0
        xj_l, yj_l, zj_l = xyzj_l[0], xyzj_l[1], 0
    else:
        ux, uy, uz = dir
        lu = np.sqrt(ux ** 2 + uy ** 2 + uz ** 2)
        ux, uy, uz = ux * length / lu, uy * length / lu, uz * length / lu
        xi_l, yi_l, zi_l = xyzi_l
        xj_l, yj_l, zj_l = xyzj_l
    quads = []
    for n in range(number):
        qname = name + "_" + str(n+1)
        xyzi = [xi_l + n * ux, yi_l + n * uy, zi_l + n * uz]
        xyzj = [xi_l + (n + 1) * ux, yi_l + (n + 1) * uy, zi_l + (n + 1) * uz]
        xyzk = [xj_l + (n + 1) * ux, yj_l + (n + 1) * uy, zj_l + (n + 1) * uz]
        xyzl = [xj_l + n * ux, yj_l + n * uy, zj_l + n * uz]

        quads.append(Quad(qname, quadprop, xyzi, xyzj, xyzk, xyzl,
             Nij=numDivij, Njk=numDivjk))

    return quads

def __divideline(xyzi,xyzj,N,staruum):

    xi, yi, zi = xyzi
    xj, yj, zj = xyzj
    XX = np.linspace(xi, xj, num=N + 1)
    YY = np.linspace(yi, yj, num=N + 1)
    ZZ = np.linspace(zi, zj, num=N + 1)
    numbering = np.linspace(staruum, staruum + N, num=N + 1,dtype=int)
    return XX, YY, ZZ, numbering

def propcommand(eletag,nodes,eleprops):
    strcommand = 'element('
    args = list(eleprops.keys())
    eletype = eleprops[args[0]]
    str_nodes = ""
    for n in nodes:
        str_nodes = str_nodes + str(n) + ", "

    str_params = ''
    for i in range(3, len(args)):
        if type(eleprops[args[i]]) == list:
            if type(eleprops[args[i]][0]) == str and eleprops[args[i]][0][0] == "-":
                paramname = eleprops[args[i]][0]
                str_param_ = "'" + paramname + "', "
                paramvals = eleprops[args[i]][1]
                if type(paramvals) == list:
                    for val in paramvals:
                        if type(val) == str:
                            str_param_ = str_param_ + "'" + val + "', "
                        else:
                            str_param_ = str_param_ + str(val) + ", "
                else:
                    if type(paramvals) == str:
                        str_param_ = str_param_ + "'" + paramvals + "', "
                    else:
                        str_param_ = str_param_ + str(paramvals) + ", "

            else:
                str_param_ = ""
                paramvals = eleprops[args[i]]
                for val in paramvals:
                    if type(val) == str:
                        str_param_ = str_param_ + "'" + val + "', "
                    else:
                        str_param_ = str_param_ + str(val) + ", "
        else:
            if type(eleprops[args[i]]) == str:
                str_param_ = "'" + str(eleprops[args[i]]) + "', "
            else:
                str_param_ = str(eleprops[args[i]]) + ", "

        str_params = str_params + str_param_

    strcommand = strcommand + "'" + eletype + "', " + str(eletag) + ", " + str_nodes + str_params
    strcommand = strcommand.strip()

    if strcommand[-1] == ",":
        strcommand = ")".join(strcommand.rsplit(strcommand[-1:], 1))
    else:
        strcommand = strcommand + ")"

    return strcommand

def findnodepairs(ops,masternodes,slavenodes):
    pairs = {}
    for n in masternodes:
        pairs[n] = []
        x, y, z = ops.nodeCoord(n)
        for s in slavenodes:
            xs, ys, zs = ops.nodeCoord(s)
            if (abs(x - xs) + abs(y - ys) + abs(z - zs)) < tolerance:
                val = pairs[n]
                val.append(s)

    up_pairs = {key: val for key, val in pairs.items() if val != []}
    return up_pairs

def addzerolength(ops,masternodes,slavenodes,zerprop,printcommand='y'):
    masternodes = list(masternodes)
    slavenodes = list(slavenodes)
    if len(ops.getEleTags()) == 0:
        eleTag = 0
    else:
        eleTag = int(np.max(ops.getEleTags()))
    elecount = 1
    nodepairs = findnodepairs(ops, masternodes, slavenodes)
    file_elements = open("file_elements.txt", "a")
    for mnode in nodepairs.keys():
        snodes = nodepairs[mnode]
        for snode in snodes:
            str_elecommand = propcommand(elecount + eleTag, [mnode, snode], zerprop)
            str_command = "ops." + str_elecommand

            file_elements.write(str_command + '\n')

            if printcommand.lower() in ['y', 'yes']:
                print(str_command)

            eval(str_command)

            # elements_[ele + eleTag] = nodes
            elecount += 1

    file_elements.close()

def deletefiles():
    if os.path.exists("file_nodes.txt"):
        os.remove("file_nodes.txt")

    if os.path.exists("file_elements.txt"):
        os.remove("file_elements.txt")

    if os.path.exists("file_fix.txt"):
        os.remove("file_fix.txt")

    if os.path.exists("file_constraint.txt"):
        os.remove("file_constraint.txt")

    if os.path.exists("file_mass.txt"):
        os.remove("file_mass.txt")

def readrecord(filename, sum_=False, startcolumn=2, factor=1.0):
    x = filename.rfind(".")
    sheatname = filename[:x]
    filename_excel = sheatname + '.xlsx'
    datalist = []
    with open(filename) as f:
        lines = f.readlines()
        count = 1
    for line in lines:
        line2 = line.split(" ")
        data_row = [float(x) for x in line2]
        data_row.insert(0, count)
        count += 1
        if sum_:
            s = sum(data_row[startcolumn:]) * factor
            data_row.append(s)

        datalist.append(data_row)

    f.close()
    dfd = pd.DataFrame(datalist)
    with pd.ExcelWriter(filename_excel) as writer:
        dfd.to_excel(writer, sheet_name=sheatname, index=False, header=False)
    return np.array(datalist)

class MyMath:
        @staticmethod
        def dividecube(xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8, N12, N14, N15):
            x1, y1, z1 = xyz1
            x2, y2, z2 = xyz2
            x3, y3, z3 = xyz3
            x4, y4, z4 = xyz4

            x5, y5, z5 = xyz5
            x6, y6, z6 = xyz6
            x7, y7, z7 = xyz7
            x8, y8, z8 = xyz8

            xrow15 = np.linspace(x1, x5, num=N15 + 1)
            yrow15 = np.linspace(y1, y5, num=N15 + 1)
            zrow15 = np.linspace(z1, z5, num=N15 + 1)

            xrow26 = np.linspace(x2, x6, num=N15 + 1)
            yrow26 = np.linspace(y2, y6, num=N15 + 1)
            zrow26 = np.linspace(z2, z6, num=N15 + 1)

            xrow37 = np.linspace(x3, x7, num=N15 + 1)
            yrow37 = np.linspace(y3, y7, num=N15 + 1)
            zrow37 = np.linspace(z3, z7, num=N15 + 1)

            xrow48 = np.linspace(x4, x8, num=N15 + 1)
            yrow48 = np.linspace(y4, y8, num=N15 + 1)
            zrow48 = np.linspace(z4, z8, num=N15 + 1)
            coords = []
            Noderange = []
            Nodes = {}
            for i in range(N15 + 1):
                nodenum = (N14 + 1) * (N12 + 1) * i
                xyz15 = [xrow15[i], yrow15[i], zrow15[i]]
                xyz26 = [xrow26[i], yrow26[i], zrow26[i]]
                xyz37 = [xrow37[i], yrow37[i], zrow37[i]]
                xyz48 = [xrow48[i], yrow48[i], zrow48[i]]
                coords_pl, Noderange_pl, nnodes = MyMath.dividequad(xyz15, xyz26, xyz37, xyz48, N12, N14, nodenum)
                for n in nnodes:
                    Nodes[n[0]] = [n[1], n[2], n[3]]
                coords.append(coords_pl)
                Noderange.append(Noderange_pl)

            return coords, np.array(Noderange), Nodes


        @staticmethod
        def dividequad(xyz1, xyz2, xyz3, xyz4, N12, N14, nodenum):
            x1, y1, z1 = xyz1
            x2, y2, z2 = xyz2
            x3, y3, z3 = xyz3
            x4, y4, z4 = xyz4
            coords = {}

            XX = np.zeros((N14 + 1, N12 + 1))
            YY = np.zeros((N14 + 1, N12 + 1))
            ZZ = np.zeros((N14 + 1, N12 + 1))
            Noderange = np.zeros((N14 + 1, N12 + 1))

            Xst = np.linspace(x1, x4, num=N14 + 1)
            Xen = np.linspace(x2, x3, num=N14 + 1)

            Yst = np.linspace(y1, y4, num=N14 + 1)
            Yen = np.linspace(y2, y3, num=N14 + 1)

            Zst = np.linspace(z1, z4, num=N14 + 1)
            Zen = np.linspace(z2, z3, num=N14 + 1)
            nodes = []
            for i in range(0, N14 + 1):
                xrow = np.linspace(Xst[i], Xen[i], num=N12 + 1)
                yrow = np.linspace(Yst[i], Yen[i], num=N12 + 1)
                zrow = np.linspace(Zst[i], Zen[i], num=N12 + 1)
                nraw = np.linspace(i * (N12 + 1) + 1, i * (N12 + 1) + 1 + N12, num=N12 + 1)
                nrawn = [int(x + nodenum) for x in nraw]
                for k in range(len(xrow)):
                    nodes.append([nrawn[k], xrow[k], yrow[k], zrow[k]])

                XX[i, :] = xrow
                YY[i, :] = yrow
                ZZ[i, :] = zrow
                Noderange[i, :] = nrawn
                for j in range(N12 + 1):
                    coords[nrawn[j]] = [xrow[j], yrow[j], zrow[j]]

            return coords, Noderange, nodes

        @staticmethod
        def extractbricknodesets(Noderange):
            # 12
            nodeset_12 = Noderange[0, 0, 0:]

            # 23
            nodeset_23 = Noderange[0, 0:, -1]

            # 43
            nodeset_43 = Noderange[0, -1, 0:]

            # 14
            nodeset_14 = Noderange[0, 0:, 0]

            # 15
            nodeset_15 = Noderange[0:, 0, 0]

            # 26
            nodeset_26 = Noderange[0:, 0, -1]

            # 37
            nodeset_37 = Noderange[0:, -1, -1]

            # 48
            nodeset_48 = Noderange[0:, -1, 0]
            # print(nodeset_48)

            # 56
            nodeset_56 = Noderange[-1, 0, 0:]

            # 67
            nodeset_67 = Noderange[-1, 0:, -1]

            # 87
            nodeset_87 = Noderange[-1, -1, 0:]

            # 58
            nodeset_58 = Noderange[-1, 0:, 0]

            nodeste = {1: {'Nodes': Noderange[0],
                           'ij': nodeset_12,
                           'jk': nodeset_23,
                           'kl': np.flip(nodeset_43),
                           'li': np.flip(nodeset_14)
                           },
                       2: {'Nodes': np.transpose(Noderange[0:, 0:, -1]),
                           'ij': nodeset_26,
                           'jk': nodeset_67,
                           'kl': np.flip(nodeset_37),
                           'li': np.flip(nodeset_23)
                           },
                       3: {'Nodes': Noderange[-1],
                           'ij': nodeset_56,
                           'jk': nodeset_67,
                           'kl': np.flip(nodeset_87),
                           'li': np.flip(nodeset_58)
                           },
                       4: {'Nodes': np.transpose(Noderange[0:, 0:, 0]),
                           'ij': nodeset_15,
                           'jk': nodeset_58,
                           'kl': np.flip(nodeset_48),
                           'li': np.flip(nodeset_14)
                           },
                       5: {'Nodes': Noderange[0:, 0, 0:],
                           'ij': nodeset_12,
                           'jk': nodeset_26,
                           'kl': np.flip(nodeset_56),
                           'li': np.flip(nodeset_15)
                           },
                       6: {'Nodes': Noderange[0:, -1, 0:],
                           'ij': nodeset_43,
                           'jk': nodeset_37,
                           'kl': np.flip(nodeset_87),
                           'li': np.flip(nodeset_48)
                           }
                       }

            return nodeste

        @staticmethod
        def extractbrickelements(coords, N12, N14):
            elements = {}
            elecount = 1
            for i in range(len(coords) - 1):
                pl1 = coords[i]
                pl2 = coords[i + 1]
                nodenum1 = (N14 + 1) * (N12 + 1) * i
                nodenum2 = (N14 + 1) * (N12 + 1) * (i + 1)
                for j in range(1, N14 + 1):
                    for k in range(1, N12 + 1):
                        nodes = {}
                        n1 = k + (j - 1) * (N12 + 1)
                        n2 = n1 + 1
                        n3 = n2 + N12 + 1
                        n4 = n1 + N12 + 1

                        nodes[n1 + nodenum1] = pl1[n1 + nodenum1]
                        nodes[n2 + nodenum1] = pl1[n2 + nodenum1]
                        nodes[n3 + nodenum1] = pl1[n3 + nodenum1]
                        nodes[n4 + nodenum1] = pl1[n4 + nodenum1]
                        nodes[n1 + nodenum2] = pl2[n1 + nodenum2]
                        nodes[n2 + nodenum2] = pl2[n2 + nodenum2]
                        nodes[n3 + nodenum2] = pl2[n3 + nodenum2]
                        nodes[n4 + nodenum2] = pl2[n4 + nodenum2]
                        elements[elecount] = nodes
                        elecount += 1
            return elements

        @staticmethod
        def plotbrickmember(ax, member, name, propname, subdivisions, edgelinewidth, fill, color, fontsize, facenumber,
                              alpha):
            xyz1 = member.XYZ1
            xyz2 = member.XYZ2
            xyz3 = member.XYZ3
            xyz4 = member.XYZ4
            xyz5 = member.XYZ5
            xyz6 = member.XYZ6
            xyz7 = member.XYZ7
            xyz8 = member.XYZ8
            N12 = member.N12
            N14 = member.N14
            N15 = member.N15
            xyz = [xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8]
            XX = []
            YY = []
            ZZ = []

            for coords in xyz:
                XX.append(coords[0])
                YY.append(coords[1])
                ZZ.append(coords[2])

            if name.lower() in ['y', 'yes']:
                xa = np.average(XX)
                ya = np.average(YY)
                za = np.average(ZZ)
                ax.text(za, xa, ya, member.Name, 'y', size=fontsize, horizontalalignment='center')

            if propname.lower() in ['y', 'yes']:
                prname = member.EleProps['Name']
                xa = np.average(XX)
                ya = np.average(YY)
                za = np.average(ZZ)
                ax.text(za, xa, ya, prname, 'y', size=fontsize, horizontalalignment='center')

            if facenumber in ['y', 'yes']:
                # face 1
                xa = np.average([xyz1[0], xyz2[0], xyz3[0], xyz4[0]])
                ya = np.average([xyz1[1], xyz2[1], xyz3[1], xyz4[1]])
                za = np.average([xyz1[2], xyz2[2], xyz3[2], xyz4[2]])
                ax.text(za, xa, ya, 1, 'y', size=fontsize, horizontalalignment='center')
                # face 2
                xa = np.average([xyz6[0], xyz2[0], xyz3[0], xyz7[0]])
                ya = np.average([xyz6[1], xyz2[1], xyz3[1], xyz7[1]])
                za = np.average([xyz6[2], xyz2[2], xyz3[2], xyz7[2]])
                ax.text(za, xa, ya, 2, 'y', size=fontsize, horizontalalignment='center')
                # face 3
                xa = np.average([xyz6[0], xyz5[0], xyz8[0], xyz7[0]])
                ya = np.average([xyz6[1], xyz5[1], xyz8[1], xyz7[1]])
                za = np.average([xyz6[2], xyz5[2], xyz8[2], xyz7[2]])
                ax.text(za, xa, ya, 3, 'y', size=fontsize, horizontalalignment='center')
                # face 4
                xa = np.average([xyz1[0], xyz5[0], xyz8[0], xyz4[0]])
                ya = np.average([xyz1[1], xyz5[1], xyz8[1], xyz4[1]])
                za = np.average([xyz1[2], xyz5[2], xyz8[2], xyz4[2]])
                ax.text(za, xa, ya, 4, 'y', size=fontsize, horizontalalignment='center')
                # face 5
                xa = np.average([xyz1[0], xyz5[0], xyz2[0], xyz6[0]])
                ya = np.average([xyz1[1], xyz5[1], xyz2[1], xyz6[1]])
                za = np.average([xyz1[2], xyz5[2], xyz2[2], xyz6[2]])
                ax.text(za, xa, ya, 5, 'y', size=fontsize, horizontalalignment='center')
                # face 6
                xa = np.average([xyz3[0], xyz7[0], xyz8[0], xyz4[0]])
                ya = np.average([xyz3[1], xyz7[1], xyz8[1], xyz4[1]])
                za = np.average([xyz3[2], xyz7[2], xyz8[2], xyz4[2]])
                ax.text(za, xa, ya, 6, 'y', size=fontsize, horizontalalignment='center')

                # plot faces
            if fill in ['y', 'yes']:
                # face 1
                xa = [xyz1[0], xyz2[0], xyz3[0], xyz4[0]]
                ya = [xyz1[1], xyz2[1], xyz3[1], xyz4[1]]
                za = [xyz1[2], xyz2[2], xyz3[2], xyz4[2]]
                vertices = [list(zip(za, xa, ya))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=color,
                                         edgecolor='silver')
                ax.add_collection3d(poly1)
                # face 2
                xa = [xyz6[0], xyz2[0], xyz3[0], xyz7[0]]
                ya = [xyz6[1], xyz2[1], xyz3[1], xyz7[1]]
                za = [xyz6[2], xyz2[2], xyz3[2], xyz7[2]]
                vertices = [list(zip(za, xa, ya))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=color,
                                         edgecolor='silver')
                ax.add_collection3d(poly1)
                # face 3
                xa = [xyz6[0], xyz5[0], xyz8[0], xyz7[0]]
                ya = [xyz6[1], xyz5[1], xyz8[1], xyz7[1]]
                za = [xyz6[2], xyz5[2], xyz8[2], xyz7[2]]
                vertices = [list(zip(za, xa, ya))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=color,
                                         edgecolor='silver')
                ax.add_collection3d(poly1)
                # face 4
                xa = [xyz1[0], xyz5[0], xyz8[0], xyz4[0]]
                ya = [xyz1[1], xyz5[1], xyz8[1], xyz4[1]]
                za = [xyz1[2], xyz5[2], xyz8[2], xyz4[2]]
                vertices = [list(zip(za, xa, ya))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=color,
                                         edgecolor='silver')
                ax.add_collection3d(poly1)
                # face 5
                xa = [xyz1[0], xyz5[0], xyz6[0], xyz2[0]]
                ya = [xyz1[1], xyz5[1], xyz6[1], xyz2[1]]
                za = [xyz1[2], xyz5[2], xyz6[2], xyz2[2]]
                vertices = [list(zip(za, xa, ya))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=color,
                                         edgecolor='silver')
                ax.add_collection3d(poly1)
                # face 6
                xa = [xyz3[0], xyz7[0], xyz8[0], xyz4[0]]
                ya = [xyz3[1], xyz7[1], xyz8[1], xyz4[1]]
                za = [xyz3[2], xyz7[2], xyz8[2], xyz4[2]]
                vertices = [list(zip(za, xa, ya))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=edgelinewidth, color=color,
                                         edgecolor='silver')
                ax.add_collection3d(poly1)

                # plot lines
            if subdivisions in ['y', 'yes']:
                coords, noderange, nodes = MyMath.dividecube(xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8, N12, N14, N15)
                nodesets = MyMath.extractbricknodesets(noderange)
                for face in nodesets.keys():
                    nodes_ = nodesets[face]['Nodes']
                    njk = len(nodes_)
                    nij = len(nodes_[0])

                    for j in range(njk):
                        n1 = nodes_[j, 0]
                        n2 = nodes_[j, nij - 1]
                        xyz1 = nodes[n1]
                        xyz2 = nodes[n2]
                        x = [xyz1[0], xyz2[0]]
                        y = [xyz1[1], xyz2[1]]
                        z = [xyz1[2], xyz2[2]]
                        ax.plot(z, x, y, lw=edgelinewidth, color='gray')
                    for j in range(nij):
                        n1 = nodes_[0, j]
                        n2 = nodes_[njk - 1, j]
                        xyz1 = nodes[n1]
                        xyz2 = nodes[n2]
                        x = [xyz1[0], xyz2[0]]
                        y = [xyz1[1], xyz2[1]]
                        z = [xyz1[2], xyz2[2]]
                        ax.plot(z, x, y, lw=edgelinewidth, color='gray')

            # face 1
            x = XX[0:4]
            x.append(x[0])
            y = YY[0:4]
            y.append(y[0])
            z = ZZ[0:4]
            z.append(z[0])
            ax.plot(z, x, y, lw=edgelinewidth, color='gray')

            # face 3
            x = XX[4:8]
            x.append(x[0])
            y = YY[4:8]
            y.append(y[0])
            z = ZZ[4:8]
            z.append(z[0])
            ax.plot(z, x, y, lw=edgelinewidth, color='gray')

            # face 2
            x = [XX[1], XX[5]]
            y = [YY[1], YY[5]]
            z = [ZZ[1], ZZ[5]]
            ax.plot(z, x, y, lw=edgelinewidth, color='gray')

            # face 4
            x = [XX[2], XX[6]]
            y = [YY[2], YY[6]]
            z = [ZZ[2], ZZ[6]]
            ax.plot(z, x, y, lw=edgelinewidth, color='gray')

            # face 5
            x = [XX[0], XX[4]]
            y = [YY[0], YY[4]]
            z = [ZZ[0], ZZ[4]]
            ax.plot(z, x, y, lw=edgelinewidth, color='gray')

            # face 6
            x = [XX[3], XX[7]]
            y = [YY[3], YY[7]]
            z = [ZZ[3], ZZ[7]]
            ax.plot(z, x, y, lw=edgelinewidth, color='gray')

        @staticmethod
        def plotcube(ax, xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8, lw, color, fill, edgecolor, alpha):
            # face 1
            x = [xyz1[0], xyz2[0], xyz3[0], xyz4[0], xyz1[0]]
            y = [xyz1[1], xyz2[1], xyz3[1], xyz4[1], xyz1[1]]
            z = [xyz1[2], xyz2[2], xyz3[2], xyz4[2], xyz1[2]]
            ax.plot(z, x, y, linewidth=lw, color=edgecolor)

            # face 3
            x = [xyz5[0], xyz6[0], xyz7[0], xyz8[0], xyz5[0]]
            y = [xyz5[1], xyz6[1], xyz7[1], xyz8[1], xyz5[1]]
            z = [xyz5[2], xyz6[2], xyz7[2], xyz8[2], xyz5[2]]
            ax.plot(z, x, y, linewidth=lw, color=edgecolor)

            # 1- 5
            x = [xyz1[0], xyz5[0]]
            y = [xyz1[1], xyz5[1]]
            z = [xyz1[2], xyz5[2]]
            ax.plot(z, x, y, linewidth=lw, color=edgecolor)

            # 2- 6
            x = [xyz2[0], xyz6[0]]
            y = [xyz2[1], xyz6[1]]
            z = [xyz2[2], xyz6[2]]
            ax.plot(z, x, y, linewidth=lw, color=edgecolor)

            # 3- 7
            x = [xyz3[0], xyz7[0]]
            y = [xyz3[1], xyz7[1]]
            z = [xyz3[2], xyz7[2]]
            ax.plot(z, x, y, linewidth=lw, color=edgecolor)

            # 4- 8
            x = [xyz4[0], xyz8[0]]
            y = [xyz4[1], xyz8[1]]
            z = [xyz4[2], xyz8[2]]
            ax.plot(z, x, y, linewidth=lw, color=edgecolor)

            if fill in ['y', 'yes']:
                # face 1
                x = [xyz1[0], xyz2[0], xyz3[0], xyz4[0]]
                y = [xyz1[1], xyz2[1], xyz3[1], xyz4[1]]
                z = [xyz1[2], xyz2[2], xyz3[2], xyz4[2]]
                vertices = [list(zip(z, x, y))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=lw, color=color, edgecolor=edgecolor)
                ax.add_collection3d(poly1)
                # face 2
                x = [xyz5[0], xyz6[0], xyz7[0], xyz8[0]]
                y = [xyz5[1], xyz6[1], xyz7[1], xyz8[1]]
                z = [xyz5[2], xyz6[2], xyz7[2], xyz8[2]]
                vertices = [list(zip(z, x, y))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=lw, color=color, edgecolor=edgecolor)
                ax.add_collection3d(poly1)

                # face 3
                x = [xyz1[0], xyz2[0], xyz6[0], xyz5[0]]
                y = [xyz1[1], xyz2[1], xyz6[1], xyz5[1]]
                z = [xyz1[2], xyz2[2], xyz6[2], xyz5[2]]
                vertices = [list(zip(z, x, y))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=lw, color=color, edgecolor=edgecolor)
                ax.add_collection3d(poly1)

                # face 4
                x = [xyz4[0], xyz3[0], xyz7[0], xyz8[0]]
                y = [xyz4[1], xyz3[1], xyz7[1], xyz8[1]]
                z = [xyz4[2], xyz3[2], xyz7[2], xyz8[2]]
                vertices = [list(zip(z, x, y))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=lw, color=color, edgecolor=edgecolor)
                ax.add_collection3d(poly1)

                # face 5
                x = [xyz4[0], xyz1[0], xyz5[0], xyz8[0]]
                y = [xyz4[1], xyz1[1], xyz5[1], xyz8[1]]
                z = [xyz4[2], xyz1[2], xyz5[2], xyz8[2]]
                vertices = [list(zip(z, x, y))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=lw, color=color, edgecolor=edgecolor)
                ax.add_collection3d(poly1)

                # face 6
                x = [xyz2[0], xyz6[0], xyz7[0], xyz3[0]]
                y = [xyz2[1], xyz6[1], xyz7[1], xyz3[1]]
                z = [xyz2[2], xyz6[2], xyz7[2], xyz3[2]]
                vertices = [list(zip(z, x, y))]
                poly1 = Poly3DCollection(vertices, alpha=alpha, linewidth=lw, color=color, edgecolor=edgecolor)
                ax.add_collection3d(poly1)

        @staticmethod
        def brickvolume(xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8):
            V = 0
            xa = np.average([xyz1[0], xyz2[0], xyz3[0], xyz4[0], xyz5[0], xyz6[0], xyz7[0], xyz8[0]])
            ya = np.average([xyz1[1], xyz2[1], xyz3[1], xyz4[1], xyz5[1], xyz6[1], xyz7[1], xyz8[1]])
            za = np.average([xyz1[2], xyz2[2], xyz3[2], xyz4[2], xyz5[2], xyz6[2], xyz7[2], xyz8[2]])
            ## face 1
            x1, y1, z1 = xyz1
            x2, y2, z2 = xyz2
            x3, y3, z3 = xyz4
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            x1, y1, z1 = xyz4
            x2, y2, z2 = xyz2
            x3, y3, z3 = xyz3
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            ## face 2
            x1, y1, z1 = xyz2
            x2, y2, z2 = xyz6
            x3, y3, z3 = xyz3
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            x1, y1, z1 = xyz3
            x2, y2, z2 = xyz6
            x3, y3, z3 = xyz7
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            ## face 3
            x1, y1, z1 = xyz5
            x2, y2, z2 = xyz6
            x3, y3, z3 = xyz8
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            x1, y1, z1 = xyz8
            x2, y2, z2 = xyz6
            x3, y3, z3 = xyz7
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            ## face 4
            x1, y1, z1 = xyz4
            x2, y2, z2 = xyz1
            x3, y3, z3 = xyz5
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            x1, y1, z1 = xyz4
            x2, y2, z2 = xyz5
            x3, y3, z3 = xyz8
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            ## face 5
            x1, y1, z1 = xyz1
            x2, y2, z2 = xyz2
            x3, y3, z3 = xyz5
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            x1, y1, z1 = xyz5
            x2, y2, z2 = xyz2
            x3, y3, z3 = xyz6
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            ## face 6
            x1, y1, z1 = xyz4
            x2, y2, z2 = xyz3
            x3, y3, z3 = xyz8
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)

            x1, y1, z1 = xyz8
            x2, y2, z2 = xyz3
            x3, y3, z3 = xyz7
            A = np.array([[1, x1, y1, z1], [1, x2, y2, z2], [1, x3, y3, z3], [1, xa, ya, za]])
            V1 = np.linalg.det(A) / 6
            V += abs(V1)
            return V

        @staticmethod
        def bricknodeshare(xyz1, xyz2, xyz3, xyz4, xyz5, xyz6, xyz7, xyz8):
            xc = np.average([xyz1[0], xyz2[0], xyz3[0], xyz4[0], xyz5[0], xyz6[0], xyz7[0], xyz8[0]])
            yc = np.average([xyz1[1], xyz2[1], xyz3[1], xyz4[1], xyz5[1], xyz6[1], xyz7[1], xyz8[1]])
            zc = np.average([xyz1[2], xyz2[2], xyz3[2], xyz4[2], xyz5[2], xyz6[2], xyz7[2], xyz8[2]])
            cc = [xc, yc, zc]

            x12 = np.average([xyz1[0], xyz2[0]])
            y12 = np.average([xyz1[1], xyz2[1]])
            z12 = np.average([xyz1[2], xyz2[2]])
            c12 = [x12, y12, z12]

            x14 = np.average([xyz1[0], xyz4[0]])
            y14 = np.average([xyz1[1], xyz4[1]])
            z14 = np.average([xyz1[2], xyz4[2]])
            c14 = [x14, y14, z14]

            x15 = np.average([xyz1[0], xyz5[0]])
            y15 = np.average([xyz1[1], xyz5[1]])
            z15 = np.average([xyz1[2], xyz5[2]])
            c15 = [x15, y15, z15]

            x23 = np.average([xyz2[0], xyz3[0]])
            y23 = np.average([xyz2[1], xyz3[1]])
            z23 = np.average([xyz2[2], xyz3[2]])
            c23 = [x23, y23, z23]

            x26 = np.average([xyz2[0], xyz6[0]])
            y26 = np.average([xyz2[1], xyz6[1]])
            z26 = np.average([xyz2[2], xyz6[2]])
            c26 = [x26, y26, z26]

            x34 = np.average([xyz3[0], xyz4[0]])
            y34 = np.average([xyz3[1], xyz4[1]])
            z34 = np.average([xyz3[2], xyz4[2]])
            c34 = [x34, y34, z34]

            x37 = np.average([xyz3[0], xyz7[0]])
            y37 = np.average([xyz3[1], xyz7[1]])
            z37 = np.average([xyz3[2], xyz7[2]])
            c37 = [x37, y37, z37]

            x48 = np.average([xyz4[0], xyz8[0]])
            y48 = np.average([xyz4[1], xyz8[1]])
            z48 = np.average([xyz4[2], xyz8[2]])
            c48 = [x48, y48, z48]

            x56 = np.average([xyz5[0], xyz6[0]])
            y56 = np.average([xyz5[1], xyz6[1]])
            z56 = np.average([xyz5[2], xyz6[2]])
            c56 = [x56, y56, z56]

            x58 = np.average([xyz5[0], xyz8[0]])
            y58 = np.average([xyz5[1], xyz8[1]])
            z58 = np.average([xyz5[2], xyz8[2]])
            c58 = [x58, y58, z58]

            x67 = np.average([xyz6[0], xyz7[0]])
            y67 = np.average([xyz6[1], xyz7[1]])
            z67 = np.average([xyz6[2], xyz7[2]])
            c67 = [x67, y67, z67]

            x78 = np.average([xyz7[0], xyz8[0]])
            y78 = np.average([xyz7[1], xyz8[1]])
            z78 = np.average([xyz7[2], xyz8[2]])
            c78 = [x78, y78, z78]

            x = np.average([xyz1[0], xyz2[0], xyz3[0], xyz4[0]])
            y = np.average([xyz1[1], xyz2[1], xyz3[1], xyz4[1]])
            z = np.average([xyz1[2], xyz2[2], xyz3[2], xyz4[2]])
            cf1 = [x, y, z]

            x = np.average([xyz2[0], xyz6[0], xyz7[0], xyz3[0]])
            y = np.average([xyz2[1], xyz6[1], xyz7[1], xyz3[1]])
            z = np.average([xyz2[2], xyz6[2], xyz7[2], xyz3[2]])
            cf2 = [x, y, z]

            x = np.average([xyz5[0], xyz6[0], xyz7[0], xyz8[0]])
            y = np.average([xyz5[1], xyz6[1], xyz7[1], xyz8[1]])
            z = np.average([xyz5[2], xyz6[2], xyz7[2], xyz8[2]])
            cf3 = [x, y, z]

            x = np.average([xyz5[0], xyz1[0], xyz4[0], xyz8[0]])
            y = np.average([xyz5[1], xyz1[1], xyz4[1], xyz8[1]])
            z = np.average([xyz5[2], xyz1[2], xyz4[2], xyz8[2]])
            cf4 = [x, y, z]

            x = np.average([xyz5[0], xyz1[0], xyz2[0], xyz6[0]])
            y = np.average([xyz5[1], xyz1[1], xyz2[1], xyz6[1]])
            z = np.average([xyz5[2], xyz1[2], xyz2[2], xyz6[2]])
            cf5 = [x, y, z]

            x = np.average([xyz3[0], xyz4[0], xyz7[0], xyz8[0]])
            y = np.average([xyz3[1], xyz4[1], xyz7[1], xyz8[1]])
            z = np.average([xyz3[2], xyz4[2], xyz7[2], xyz8[2]])
            cf6 = [x, y, z]

            V1 = MyMath.brickvolume(xyz1, c12, cf1, c14, c15, cf5, cc, cf4)
            V2 = MyMath.brickvolume(c12, xyz2, c23, cf1, cf5, c26, cf2, cc)
            V3 = MyMath.brickvolume(cf1, c23, xyz3, c34, cc, cf2, c37, cf6)
            V4 = MyMath.brickvolume(c14, cf1, c34, xyz4, cf4, cc, cf6, c48)
            V5 = MyMath.brickvolume(c15, cf5, cc, cf4, xyz5, c56, cf3, c58)
            V6 = MyMath.brickvolume(cf5, c26, cf2, cc, c56, xyz6, c67, cf3)
            V7 = MyMath.brickvolume(cc, cf2, c37, cf6, cf3, c67, xyz7, c78)
            V8 = MyMath.brickvolume(cf4, cc, cf6, c48, c58, cf3, c78, xyz8)

            V = V1 + V2 + V3 + V4 + V5 + V6 + V7 + V8

            return V1 / V, V2 / V, V3 / V, V4 / V, V5 / V, V6 / V, V7 / V, V8 / V

        @staticmethod
        def mirrorpoint(xyz, xyz1, xyz2, xyz3):
            for value in [xyz1, xyz2, xyz3]:
                value = list(value)
                if len(value) not in [2, 3]:
                    raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

                for i in range(len(value)):
                    if type(value[i]) is int:
                        value[i] = float(value[i])

                    if isinstance(value[i], numbers.Number) == False:
                        raise ValueError("Coordinates must be numeric values")

            x1, y1, z1 = xyz1
            x2, y2, z2 = xyz2
            x3, y3, z3 = xyz3
            x, y, z = xyz
            a, b, c = np.cross([(x2 - x1), (y2 - y1), (z2 - z1)], [(x3 - x1), (y3 - y1), (z3 - z1)])
            d = -1 * (a * x1 + b * y1 + c * z1)

            k = (-a * x - b * y - c * z - d) / (a * a + b * b + c * c)
            x2, y2, z2 = a * k + x, b * k + y, c * k + z
            symx, symy, symz = 2 * x2 - x, 2 * y2 - y, 2 * z2 - z
            return [symx, symy, symz]

        @staticmethod
        def rotatepoint(xyz, xyz1, xyz2, teta):
            for value in [xyz1, xyz2]:
                value = list(value)
                if len(value) not in [2, 3]:
                    raise ValueError("xyz must be a list contains coordinates [x, y, z] or [x, y]")

                for i in range(len(value)):
                    if type(value[i]) is int:
                        value[i] = float(value[i])

                    if isinstance(value[i], numbers.Number) == False:
                        raise ValueError("Coordinates must be numeric values")

            if isinstance(teta, numbers.Number) == False:
                raise ValueError('teta must be a numeric value')

            x1, y1, z1 = xyz1
            x2, y2, z2 = xyz2
            t = np.deg2rad(teta)
            ux, uy, uz = x2 - x1, y2 - y1, z2 - z1
            l = np.sqrt(ux ** 2 + uy ** 2 + uz ** 2)
            ux, uy, uz = ux / l, uy / l, uz / l
            cost, sint = np.cos(t), np.sin(t)
            R = np.array(
                [[cost + ux * ux * (1 - cost), ux * uy * (1 - cost) - uz * sint, ux * uz * (1 - cost) + uy * sint],
                 [uy * ux * (1 - cost) + uz * sint, cost + uy * uy * (1 - cost), uy * uz * (1 - cost) - ux * sint],
                 [uz * ux * (1 - cost) - uy * sint, uz * uy * (1 - cost) + ux * sint, cost + uz * uz * (1 - cost)]])

            xp, yp, zp = xyz
            xq, yq, zq = xp - x1, yp - y1, zp - z1
            A = list(np.matmul(R, np.array([xq, yq, zq]).transpose()).transpose())
            # print(A)
            A[0] += x1
            A[1] += y1
            A[2] += z1

            return A

        @staticmethod
        def dividetriangle(N, ele_numnodes, xyzi, xyzj, xyzk):

            Elements = {}
            Nodes = {}
            staruum = 1
            dictnodes = {}
            count = 1
            xc = (xyzi[0] + xyzj[0] + xyzk[0]) / 3
            yc = (xyzi[1] + xyzj[1] + xyzk[1]) / 3
            zc = (xyzi[2] + xyzj[2] + xyzk[2]) / 3
            centernode = [xc, yc, zc]
            Ndiv = N
            ##################  4 node elements
            if ele_numnodes == 4:
                if N <= 1 or np.remainder(Ndiv, 2) != 0:
                    raise ValueError(
                        "Triangle area with four node quadrilateral element: Number of divisions must be even positive integer value "
                        "greater than 1")

                while Ndiv >= 2:

                    XXij, YYij, ZZij, numberingij = __divideline(xyzi, xyzj, Ndiv, staruum)
                    staruum = numberingij[-1]
                    XXjk, YYjk, ZZjk, numberingjk = __divideline(xyzj, xyzk, Ndiv, staruum)
                    staruum = numberingjk[-1]
                    XXki, YYki, ZZki, numberingki = __divideline(xyzk, xyzi, Ndiv, staruum)
                    numberingki[-1] = numberingij[0]
                    staruum = numberingki[-2] + 1

                    for i in range(len(XXij)):
                        xx, yy, zz = XXij[i], YYij[i], ZZij[i]
                        nnum = int(numberingij[i])
                        Nodes[nnum] = [xx, yy, zz]

                    for i in range(len(XXij)):
                        xx, yy, zz = XXjk[i], YYjk[i], ZZjk[i]
                        nnum = int(numberingjk[i])
                        Nodes[nnum] = [xx, yy, zz]

                    for i in range(len(XXij)):
                        xx, yy, zz = XXki[i], YYki[i], ZZki[i]
                        nnum = int(numberingki[i])
                        Nodes[nnum] = [xx, yy, zz]

                    dictnodes[count] = {'ij': numberingij,
                                        'jk': numberingjk,
                                        'ki': numberingki}

                    count += 1

                    xyzij1 = [XXij[1], YYij[1], ZZij[1]]
                    xyzij2 = [XXij[-2], YYij[-2], ZZij[-2]]
                    xyzjk1 = [XXjk[1], YYjk[1], ZZjk[1]]
                    xyzjk2 = [XXjk[-2], YYjk[-2], ZZjk[-2]]
                    xyzki1 = [XXki[1], YYki[1], ZZki[1]]
                    xyzki2 = [XXki[-2], YYki[-2], ZZki[-2]]

                    xxx, yyy, zzz, numberi = __divideline(xyzij1, xyzjk2, Ndiv - 1, staruum)
                    xyzi = [xxx[1], yyy[1], zzz[1]]
                    xxx, yyy, zzz, numberi = __divideline(xyzjk1, xyzki2, Ndiv - 1, staruum)
                    xyzj = [xxx[1], yyy[1], zzz[1]]
                    xxx, yyy, zzz, numberi = __divideline(xyzki1, xyzij2, Ndiv - 1, staruum)
                    xyzk = [xxx[1], yyy[1], zzz[1]]
                    Ndiv -= 2

                count = 1
                edgeNodes = dictnodes[1]
                if N > 2:
                    for i in range(1, len(dictnodes.keys())):
                        nodes_ij_1 = dictnodes[i]['ij']
                        nodes_ij_2 = dictnodes[i + 1]['ij']
                        nodes_jk_1 = dictnodes[i]['jk']
                        nodes_jk_2 = dictnodes[i + 1]['jk']
                        nodes_ki_1 = dictnodes[i]['ki']
                        nodes_ki_2 = dictnodes[i + 1]['ki']

                        for j in range(len(nodes_ij_1) - 1):
                            nodei = nodes_ij_1[j]
                            nodej = nodes_ij_1[j + 1]
                            if j == len(nodes_ij_1) - 2:
                                nodek = nodes_jk_1[1]
                            else:
                                nodek = nodes_ij_2[j]

                            if j == 0:
                                nodel = nodes_ki_1[-2]
                            else:
                                nodel = nodes_ij_2[j - 1]
                            Elements[count] = [nodei, nodej, nodek, nodel]

                            count += 1

                        for j in range(1, len(nodes_jk_1) - 1):
                            nodei = nodes_jk_1[j]
                            nodej = nodes_jk_1[j + 1]
                            if j == len(nodes_jk_1) - 2:
                                nodek = nodes_ki_1[1]
                            else:
                                nodek = nodes_jk_2[j]

                            nodel = nodes_jk_2[j - 1]

                            Elements[count] = [nodei, nodej, nodek, nodel]
                            count += 1
                        for j in range(1, len(nodes_ki_1) - 2):
                            nodei = nodes_ki_1[j]
                            nodej = nodes_ki_1[j + 1]
                            nodek = nodes_ki_2[j]
                            nodel = nodes_ki_2[j - 1]
                            Elements[count] = [nodei, nodej, nodek, nodel]

                            count += 1

                        if i == len(dictnodes.keys()) - 1:
                            if np.remainder(N, 2) == 0:
                                cnodtag = int(nodel + 1)
                                Nodes[cnodtag] = centernode
                                nodei = nodes_ij_2[0]
                                nodej = nodes_ij_2[1]
                                nodek = cnodtag
                                nodel = nodes_ki_2[1]
                                Elements[count] = [nodei, nodej, nodek, nodel]
                                count += 1

                                nodei = nodes_ij_2[1]
                                nodej = nodes_ij_2[2]
                                nodek = nodes_jk_2[1]
                                nodel = cnodtag
                                Elements[count] = [nodei, nodej, nodek, nodel]
                                count += 1

                                nodei = nodes_jk_2[1]
                                nodej = nodes_jk_2[2]
                                nodek = nodes_ki_2[1]
                                nodel = cnodtag
                                Elements[count] = [nodei, nodej, nodek, nodel]
                                count += 1
                            else:
                                pass
                else:
                    count = 1
                    nodes_ij = edgeNodes['ij']
                    nodes_jk = edgeNodes['jk']
                    nodes_ki = edgeNodes['ki']
                    cnodtag = 7
                    Nodes[cnodtag] = centernode
                    nodei = nodes_ij[0]
                    nodej = nodes_ij[1]
                    nodek = cnodtag
                    nodel = nodes_ki[1]
                    Elements[count] = [nodei, nodej, nodek, nodel]
                    count += 1

                    nodei = nodes_ij[1]
                    nodej = nodes_ij[2]
                    nodek = nodes_jk[1]
                    nodel = cnodtag
                    Elements[count] = [nodei, nodej, nodek, nodel]
                    count += 1

                    nodei = nodes_jk[1]
                    nodej = nodes_jk[2]
                    nodek = nodes_ki[1]
                    nodel = cnodtag
                    Elements[count] = [nodei, nodej, nodek, nodel]

            ##################  9 node elements
            elif ele_numnodes == 9:
                if N <= 1 or np.remainder(Ndiv, 2) != 0:
                    raise ValueError(
                        "Triangle area with nine node quadrilateral element: Number of divisions must be even positive integer"
                        " value greater than 1")
                dictnodes2 = {}
                while Ndiv >= 2:

                    XXij, YYij, ZZij, numberingij = __divideline(xyzi, xyzj, 2 * Ndiv, staruum)
                    staruum = numberingij[-1]
                    XXjk, YYjk, ZZjk, numberingjk = __divideline(xyzj, xyzk, 2 * Ndiv, staruum)
                    staruum = numberingjk[-1]
                    XXki, YYki, ZZki, numberingki = __divideline(xyzk, xyzi, 2 * Ndiv, staruum)
                    numberingki[-1] = numberingij[0]
                    staruum = numberingki[-2] + 1

                    for i in range(len(XXij)):
                        xx, yy, zz = XXij[i], YYij[i], ZZij[i]
                        nnum = int(numberingij[i])
                        Nodes[nnum] = [xx, yy, zz]

                    for i in range(len(XXij)):
                        xx, yy, zz = XXjk[i], YYjk[i], ZZjk[i]
                        nnum = int(numberingjk[i])
                        Nodes[nnum] = [xx, yy, zz]

                    for i in range(len(XXij)):
                        xx, yy, zz = XXki[i], YYki[i], ZZki[i]
                        nnum = int(numberingki[i])
                        Nodes[nnum] = [xx, yy, zz]

                    dictnodes[count] = {'ij': numberingij,
                                        'jk': numberingjk,
                                        'ki': numberingki}

                    count += 1
                    xyzij1 = [XXij[2], YYij[2], ZZij[2]]
                    xyzij2 = [XXij[-3], YYij[-3], ZZij[-3]]
                    xyzjk1 = [XXjk[2], YYjk[2], ZZjk[2]]
                    xyzjk2 = [XXjk[-3], YYjk[-3], ZZjk[-3]]
                    xyzki1 = [XXki[2], YYki[2], ZZki[2]]
                    xyzki2 = [XXki[-3], YYki[-3], ZZki[-3]]

                    xxx, yyy, zzz, numberi = __divideline(xyzij1, xyzjk2, Ndiv - 1, staruum)
                    xyzi = [xxx[1], yyy[1], zzz[1]]
                    xxx, yyy, zzz, numberi = __divideline(xyzjk1, xyzki2, Ndiv - 1, staruum)
                    xyzj = [xxx[1], yyy[1], zzz[1]]
                    xxx, yyy, zzz, numberi = __divideline(xyzki1, xyzij2, Ndiv - 1, staruum)
                    xyzk = [xxx[1], yyy[1], zzz[1]]
                    Ndiv -= 2

                edgeNodes = dictnodes[1]
                if N > 2:
                    for i in range(len(dictnodes.keys()) - 1):
                        nodes_ij_1 = dictnodes[i + 1]['ij']
                        nodes_jk_1 = dictnodes[i + 1]['jk']
                        nodes_ki_1 = dictnodes[i + 1]['ki']
                        nodes_ij_2 = dictnodes[i + 2]['ij']
                        nodes_jk_2 = dictnodes[i + 2]['jk']
                        nodes_ki_2 = dictnodes[i + 2]['ki']
                        numberingij = []
                        numberingjk = []
                        numberingki = []
                        for j in range(2, len(nodes_ij_1) - 2, 2):
                            node1 = nodes_ij_1[j]
                            node2 = nodes_ij_2[j - 2]
                            x1, y1, z1 = Nodes[node1]
                            x2, y2, z2 = Nodes[node2]
                            x3, y3, z3 = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
                            Nodes[staruum] = [x3, y3, z3]
                            numberingij.append(staruum)
                            staruum += 1

                        for j in range(2, len(nodes_jk_1) - 2, 2):
                            node1 = nodes_jk_1[j]
                            node2 = nodes_jk_2[j - 2]
                            x1, y1, z1 = Nodes[node1]
                            x2, y2, z2 = Nodes[node2]
                            x3, y3, z3 = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
                            Nodes[staruum] = [x3, y3, z3]
                            numberingjk.append(staruum)
                            staruum += 1

                        for j in range(2, len(nodes_ki_1) - 2, 2):
                            node1 = nodes_ki_1[j]
                            node2 = nodes_ki_2[j - 2]
                            x1, y1, z1 = Nodes[node1]
                            x2, y2, z2 = Nodes[node2]
                            x3, y3, z3 = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
                            Nodes[staruum] = [x3, y3, z3]
                            numberingki.append(staruum)
                            staruum += 1

                        dictnodes2[i + 1] = {'ij': numberingij,
                                             'jk': numberingjk,
                                             'ki': numberingki}

                    count = 1
                    for i in range(1, len(dictnodes.keys())):
                        nodes_ij_1 = dictnodes[i]['ij']
                        nodes_ij_2 = dictnodes[i + 1]['ij']
                        nodes_jk_1 = dictnodes[i]['jk']
                        nodes_jk_2 = dictnodes[i + 1]['jk']
                        nodes_ki_1 = dictnodes[i]['ki']
                        nodes_ki_2 = dictnodes[i + 1]['ki']

                        nodes_ij_m = dictnodes2[i]['ij']
                        nodes_jk_m = dictnodes2[i]['jk']
                        nodes_ki_m = dictnodes2[i]['ki']

                        for j in range(0, len(nodes_ij_1) - 1, 2):
                            node1 = nodes_ij_1[j]
                            node2 = nodes_ij_1[j + 2]
                            if j == len(nodes_ij_1) - 3:
                                node3 = nodes_jk_1[2]
                            else:
                                node3 = nodes_ij_2[j]

                            if j == 0:
                                node4 = nodes_ki_1[-3]
                            else:
                                node4 = nodes_ij_2[j - 2]

                            node5 = nodes_ij_1[j + 1]

                            if j == len(nodes_ij_1) - 3:
                                node6 = nodes_jk_1[1]
                            else:
                                # print(j / 2)
                                node6 = nodes_ij_m[int(j / 2)]

                            if j == 0:
                                node7 = nodes_ki_m[-1]
                            elif j == len(nodes_ij_1) - 3:
                                node7 = nodes_jk_m[0]
                            else:
                                node7 = nodes_ij_2[j - 1]

                            if j == 0:
                                node8 = nodes_ki_1[-2]
                            else:
                                node8 = nodes_ij_m[int(j / 2 - 1)]

                            node9 = staruum
                            x5, y5, z5 = Nodes[node5]
                            x7, y7, z7 = Nodes[node7]
                            x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                            Nodes[node9] = [x9, y9, z9]
                            Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                            count += 1
                            staruum += 1

                        for j in range(2, len(nodes_jk_1) - 1, 2):
                            node1 = nodes_jk_2[j - 2]
                            node2 = nodes_jk_1[j]
                            node3 = nodes_jk_1[j + 2]
                            if j == len(nodes_jk_1) - 3:
                                node4 = nodes_ki_1[2]
                            else:
                                node4 = nodes_jk_2[j]

                            node5 = nodes_jk_m[int(j / 2 - 1)]
                            node6 = nodes_jk_1[j + 1]

                            if j == len(nodes_ij_1) - 3:
                                node7 = nodes_ki_1[1]
                            else:
                                node7 = nodes_jk_m[int(j / 2)]

                            if j == len(nodes_ij_1) - 3:
                                node8 = nodes_ki_m[0]
                            else:
                                node8 = nodes_jk_2[j - 1]

                            node9 = staruum
                            x5, y5, z5 = Nodes[node5]
                            x7, y7, z7 = Nodes[node7]
                            x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                            Nodes[node9] = [x9, y9, z9]
                            Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                            count += 1
                            staruum += 1

                        for j in range(2, len(nodes_ki_1) - 3, 2):
                            node1 = nodes_ki_1[j + 2]
                            node2 = nodes_ki_2[j]
                            node3 = nodes_ki_2[j - 2]
                            node4 = nodes_ki_1[j]
                            node5 = nodes_ki_m[int(j / 2)]
                            node6 = nodes_ki_2[j - 1]
                            node7 = nodes_ki_m[int(j / 2 - 1)]
                            node8 = nodes_ki_1[j + 1]

                            node9 = staruum
                            x5, y5, z5 = Nodes[node5]
                            x7, y7, z7 = Nodes[node7]
                            x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                            Nodes[node9] = [x9, y9, z9]
                            Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                            count += 1
                            staruum += 1

                        if i == len(dictnodes.keys()) - 1:
                            if np.remainder(N, 2) == 0:
                                cnodtag = staruum
                                staruum += 1
                                Nodes[cnodtag] = centernode

                                node1 = nodes_ij_2[0]
                                node2 = nodes_ij_2[2]
                                node3 = cnodtag
                                node4 = nodes_ki_2[2]
                                node5 = nodes_ij_2[1]

                                x2, y2, z2 = Nodes[node2]
                                x3, y3, z3 = Nodes[node3]
                                x4, y4, z4 = Nodes[node4]
                                x5, y5, z5 = Nodes[node5]

                                x6, y6, z6 = (x2 + x3) / 2, (y2 + y3) / 2, (z2 + z3) / 2
                                x7, y7, z7 = (x3 + x4) / 2, (y3 + y4) / 2, (z3 + z4) / 2
                                node6 = staruum
                                no1 = node6
                                staruum += 1
                                node7 = staruum
                                no2 = node7
                                staruum += 1
                                Nodes[node6] = [x6, y6, z6]
                                Nodes[node7] = [x7, y7, z7]

                                node8 = nodes_ki_2[3]

                                node9 = staruum
                                staruum += 1
                                x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                                Nodes[node9] = [x9, y9, z9]
                                Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                                count += 1

                                node1 = nodes_ij_2[2]
                                node2 = nodes_ij_2[4]
                                node3 = nodes_jk_2[2]
                                node4 = cnodtag

                                node5 = nodes_ij_2[3]
                                node6 = nodes_jk_2[1]

                                x3, y3, z3 = Nodes[node3]
                                x4, y4, z4 = Nodes[node4]
                                x5, y5, z5 = Nodes[node5]

                                x7, y7, z7 = (x3 + x4) / 2, (y3 + y4) / 2, (z3 + z4) / 2
                                node7 = staruum
                                no3 = node7
                                staruum += 1
                                Nodes[node7] = [x7, y7, z7]

                                node8 = no1
                                node9 = staruum
                                staruum += 1
                                x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                                Nodes[node9] = [x9, y9, z9]

                                Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                                count += 1

                                node1 = nodes_jk_2[2]
                                node2 = nodes_jk_2[4]
                                node3 = nodes_ki_2[2]
                                node4 = cnodtag
                                node5 = nodes_jk_2[3]
                                node6 = nodes_ki_2[1]
                                node7 = no2
                                node8 = no3

                                x5, y5, z5 = Nodes[node5]
                                x7, y7, z7 = Nodes[node7]
                                node9 = staruum
                                staruum += 1
                                x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                                Nodes[node9] = [x9, y9, z9]
                                Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                                count += 1
                            else:
                                pass
                else:
                    count = 1
                    nodes_ij = edgeNodes['ij']
                    nodes_jk = edgeNodes['jk']
                    nodes_ki = edgeNodes['ki']
                    staruum = 13
                    cnodtag = staruum
                    staruum += 1
                    Nodes[cnodtag] = centernode

                    node1 = nodes_ij[0]
                    node2 = nodes_ij[2]
                    node3 = cnodtag
                    node4 = nodes_ki[2]
                    node5 = nodes_ij[1]

                    x2, y2, z2 = Nodes[node2]
                    x3, y3, z3 = Nodes[node3]
                    x4, y4, z4 = Nodes[node4]
                    x5, y5, z5 = Nodes[node5]

                    x6, y6, z6 = (x2 + x3) / 2, (y2 + y3) / 2, (z2 + z3) / 2
                    x7, y7, z7 = (x3 + x4) / 2, (y3 + y4) / 2, (z3 + z4) / 2
                    node6 = staruum
                    no1 = node6
                    staruum += 1
                    node7 = staruum
                    no2 = node7
                    staruum += 1
                    Nodes[node6] = [x6, y6, z6]
                    Nodes[node7] = [x7, y7, z7]

                    node8 = nodes_ki[3]

                    node9 = staruum
                    staruum += 1
                    x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                    Nodes[node9] = [x9, y9, z9]
                    Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                    count += 1

                    node1 = nodes_ij[2]
                    node2 = nodes_ij[4]
                    node3 = nodes_jk[2]
                    node4 = cnodtag

                    node5 = nodes_ij[3]
                    node6 = nodes_jk[1]

                    x3, y3, z3 = Nodes[node3]
                    x4, y4, z4 = Nodes[node4]
                    x5, y5, z5 = Nodes[node5]

                    x7, y7, z7 = (x3 + x4) / 2, (y3 + y4) / 2, (z3 + z4) / 2
                    node7 = staruum
                    no3 = node7
                    staruum += 1
                    Nodes[node7] = [x7, y7, z7]

                    node8 = no1
                    node9 = staruum
                    staruum += 1
                    x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                    Nodes[node9] = [x9, y9, z9]

                    Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]
                    count += 1

                    node1 = nodes_jk[2]
                    node2 = nodes_jk[4]
                    node3 = nodes_ki[2]
                    node4 = cnodtag
                    node5 = nodes_jk[3]
                    node6 = nodes_ki[1]
                    node7 = no2
                    node8 = no3

                    x5, y5, z5 = Nodes[node5]
                    x7, y7, z7 = Nodes[node7]
                    node9 = staruum
                    staruum += 1
                    x9, y9, z9 = (x5 + x7) / 2, (y5 + y7) / 2, (z5 + z7) / 2
                    Nodes[node9] = [x9, y9, z9]
                    Elements[count] = [node1, node2, node3, node4, node5, node6, node7, node8, node9]

            ##################  3 node elements
            elif ele_numnodes == 3:
                if N < 1:
                    raise ValueError(
                        "Triangle area with three node triangular element: Number of divisions must be positive integer value")

                XXij, YYij, ZZij, numberingij = __divideline(xyzi, xyzj, Ndiv, staruum)
                staruum = numberingij[-1]
                XXjk, YYjk, ZZjk, numberingjk = __divideline(xyzj, xyzk, Ndiv, staruum)
                staruum = numberingjk[-1]
                XXki, YYki, ZZki, numberingki = __divideline(xyzk, xyzi, Ndiv, staruum)
                numberingki[-1] = numberingij[0]
                staruum = numberingki[-2]

                for i in range(len(XXij)):
                    xx, yy, zz = XXij[i], YYij[i], ZZij[i]
                    nnum = int(numberingij[i])
                    Nodes[nnum] = [xx, yy, zz]

                for i in range(len(XXij)):
                    xx, yy, zz = XXjk[i], YYjk[i], ZZjk[i]
                    nnum = int(numberingjk[i])
                    Nodes[nnum] = [xx, yy, zz]

                for i in range(len(XXij)):
                    xx, yy, zz = XXki[i], YYki[i], ZZki[i]
                    nnum = int(numberingki[i])
                    Nodes[nnum] = [xx, yy, zz]

                dictnodes = {'ij': numberingij,
                             'jk': numberingjk,
                             'ki': numberingki}

                dictnodes2 = {}
                dictnodes2[0] = numberingij
                numberingik = list(numberingki)
                numberingik.reverse()

                for i in range(1, Ndiv - 1):
                    nodei = numberingik[i]
                    nodej = numberingjk[i]

                    xyzi = Nodes[nodei]
                    xyzj = Nodes[nodej]

                    XXij, YYij, ZZij, numbering = __divideline(xyzi, xyzj, Ndiv - i, staruum)

                    numbering[0] = nodei
                    numbering[-1] = nodej
                    staruum = numbering[-2]

                    dictnodes2[i] = numbering

                    for i in range(len(XXij)):
                        xx, yy, zz = XXij[i], YYij[i], ZZij[i]
                        nnum = int(numbering[i])
                        Nodes[nnum] = [xx, yy, zz]

                dictnodes2[Ndiv - 1] = [numberingki[1], numberingjk[-2]]
                dictnodes2[Ndiv] = [numberingjk[-1]]
                edgeNodes = dictnodes
                count = 1

                for i in range(len(dictnodes2) - 1):
                    nodes_ij_1 = dictnodes2[i]
                    nodes_ij_2 = dictnodes2[i + 1]
                    for j in range(len(nodes_ij_2)):
                        nodei = nodes_ij_1[j]
                        nodej = nodes_ij_1[j + 1]
                        nodek = nodes_ij_2[j]
                        Elements[count] = [nodei, nodej, nodek]
                        count += 1
                        if j != len(nodes_ij_2) - 1:
                            nodei = nodes_ij_1[j + 1]
                            nodej = nodes_ij_2[j + 1]
                            nodek = nodes_ij_2[j]
                            Elements[count] = [nodei, nodej, nodek]
                            count += 1

            return Nodes, Elements, edgeNodes
