class Graph_data:
    def __init__(self,pdbfile,dcdfiles,outputfiles):
        self.pdbfile = pdbfile
        self.dcdfiles = dcdfiles
        self.outputfiles = outputfiles
        self.graphs = []
        self.graph_banners = []
        self.graph_data = []
        