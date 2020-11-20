import numpy as np
import imageutils
from gaussian import Gaussian

class Comparator:
    def __init__(self):
        self.era_gaussians = []
        for era in ['Neoclassicism', 'Rococo']:
            xy_file = './../images/values/xy/' + era + '-xy.csv'
            xy_data = readfile(xy_file)
            _, _, G = Gaussian(xy_data).compute()
            self.era_gaussians.append(G)
    # Generate a file of the similarity scores for each image in the FreeArt
    # database. Mode 'representative' returns most representative image;
    # mode 'distinctive' returns most distinctive image, in comparison to 
    # other movement
    def compare(self, era, mode='representative'):
        if era == 'Neoclassicism':
            G = self.era_gaussians[0]
            otherG = self.era_gaussians[1]
        else:
            G = self.era_gaussians[1]
            otherG = self.era_gaussians[0]
        with open('./' + era + '-xy.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['file', 'diff'])
            sample_files = './../images/freeart/images/'
            for fname in os.listdir(sample_files):
                if fname[0] == '.': continue
                sample_data = np.array(Image.open(sample_files + fname))
                sample_data = imageutils.reshapergb(sample_data)
                sample_data = imageutils.convertxy(sample_data)
                _, _, sG = Gaussian(sample_data).compute()
                diff = np.linalg.norm(G - sG)
                if mode == 'distinctive':
                    diff -= np.linalg.norm(otherG - sG)
                writer.writerow([fname.split('.')[0], diff]