import numpy as np
import utils
from gaussians import Gaussian

class GaussianClassifier:
	def __init__(self, samplesz=None):
		self.data = utils.loaddata()
		self.samplesz = samplesz
	def _sampleImages(mat):
    	idx = np.random.choice(mat.shape[0], size=SAMPLESZ, replace=False)
    	sampled = mat[:SAMPLESZ,:]
    	return sampled
    # Read files from each movement
	def makedata():
		movement_data = []
		for movement in ['Neoclassicism', 'Rococo']:
	    	subset = data[data['movement'] == movement]
	    	files = utils.readfiles(subset)
	    	movement_data.append(files)
	    	self.nworks = len(files)
	    self.movement_data = movement_data
	# Run LOOCV on Olga's Gallery data to evaluate accuracy
	def evaluate():
		ncorrect = 0.0
		nclassified = 0.0
		for i in range(self.nworks):
		    train_gs = []
		    test_gs = []
		    for m in movement_data:
		        train_xy = np.concatenate(m[:i] + m[i+1:])
		        if self.samplesz is not None: train_xy = sampleImages(train_xy)
		        test_xy = np.array(m[i+1])
		        if self.samplesz is not None: test_xy = sampleImages(test_xy)
		        try:
		            _, _, train_g = Gaussian(train_xy).compute()
		            _, _, test_g = Gaussian(test_xy).compute()
		        except: continue # to avoid singular matrix errors with small samplesz
		        train_gs.append(train_g)
		        test_gs.append(test_g)
		    if len(train_gs) < 2: continue # to catch the exception above
		    # Compare to both movements
		    for j in range(2):
		        test_g = test_gs[j]
		        neo_sim = np.linalg.norm(train_gs[0] - test_g)
		        roc_sim = np.linalg.norm(train_gs[1] - test_g)
		        if neo_sim > roc_sim and j == 0: ncorrect += 1
		        if neo_sim < roc_sim and j == 1: ncorrect += 1
		    	nclassified += 1
		return ncorrect/nclassified