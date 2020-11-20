import numpy as np
import imageutils
import utils
from gaussians import Gaussian

era = 'Neoclassicism'
space = 'hsl'

class TimeGaussians:
    def __init__(self, samplesz=None):
        self.samplesz = samplesz
        self.data = utils.loaddata()
        self.eraGaussians = self._storeGaussians()
        self.schools = []
    def _eraImages(self, era, space):
        eradata = self.data[self.data['era'] == era]
        files = list(eradata.index)
        allimages = utils.loadimages(files)
        if space == 'hsl': allimages = imageutils.converthsl(allimages)
        if space == 'xy': allimages = imageutils.convertxy(allimages)
        return allimages
    def _sample(self, images):
        idx = np.random.choice(images.shape[0], size=self.samplesz, replace=False)
        sampled = images[:self.samplesz,:]
        return sampled
    def _computeGaussian(self, images, normed=True):
        _, _, G = Gaussian(images).compute()
        if normed: G = (G - np.mean(G))/np.std(G)
        return G
    def _storeGaussians(self):
        stored = {}
        for era in ['Rococo', 'Neoclassicism']:
            images = self._eraImages(era, 'xy')
            if self.samplesz is not None: images = self._sample(images)
            gaussian = self._computeGaussian(images)
            stored[era] = gaussian
        return stored
    def _concatImages(self, subset):
        images_concat = {}
        for year in subset:
            concat = subset[year]
            concat = np.concatenate(concat)
            images_concat[year] = concat
        return images_concat
    def generateSample(self, fname, space):
        sampledata = imageutils.parseimage(fname)
        sampledata = imageutils.reshapergb(sampledata)
        if space == 'hsl': sampledata = imageutils.converthsl(sampledata)
        if space == 'xy': sampledata = imageutils.convertxy(sampledata)
        return sampledata
    def compareSample(self, sample, plot=False, verbose=False):
        samplegaussian = self._computeGaussian(sample)
        if plot: utils.plot2D(samplegaussian)
        results = []
        for era in ['Rococo', 'Neoclassicism']:
            diffmatrix = stored[era]
            samplediff = diffmatrix - samplegaussian
            samplediff = np.linalg.norm(samplediff)
            if verbose: print(era, samplediff)
            results.append(samplediff)
        return results[0], results[1]
    def loadCorpus(self, byschool=False):
        imagespath = './../images/wga/images/'
        imagesbyyear = {}
        imagesbyschool = {}
        for school in os.listdir(imagespath):
            if school[0] == '.': continue
            self.schools.append(school)
            imagesbyschool[school] = {}
            for f in os.listdir(imagespath + school):
                if f[0] == '.': continue
                fname = imagespath + school + '/' + f
                year = int(f.split('-')[0])
                if year not in imagesbyyear:
                    imagesbyyear[year] = []
                    imagesbyschool[school][year] = []
                imagedata = self.generateSample(fname, 'xy')
                imagesbyyear[year].append(imagedata)
                imagesbyschool[school][year].append(imagedata)
        self.corpus = self._concatImages(imagesbyyear)
        self.school_raw = imagesbyschool
    def _makeCorrelations(self, corpus=None):
        if corpus is None: corpus = self.corpus
        min_year = min(list(corpus.keys()))
        max_year = max(list(corpus.keys()))
        xs = range(min_year, max_year+1)
        rcorrs = []
        ncorrs = []
        for year in xs:
            if year not in corpus: continue
            year_sample = corpus[year]
            if self.samplesz is not None: year_sample = self._sample(year_sample)
            comparison = self.compareSample(year_sample)
            rcorrs.append(comparison[0])
            ncorrs.append(comparison[1])
        return rcorrs, ncorrs
    def plotDiff(self, y0, y1, minyear, rollingn=10, save=None):
        diff = [y0[x] - y1[x] for x in range(len(y0))]
        meandiff = sum(diff)/len(diff)
        diff_adj = [x-meandiff for x in diff]
        plt.scatter(range(minyear+rollingn, minyear+len(y0)+rollingn), diff_adj)
        if save is not None: plt.savefig(save)
        plt.show()
    def rollingCorrs(self, rcorrs, ncorrs, rollingn=10):
        xs = range(len(ncorrs))
        rollingxs = xs[rollingn:-rollingn]
        ncorrs_rolling = []
        rcorrs_rolling = []
        for year in range(rollingn, len(xs)-rollingn):
            nrelevant = ncorrs[year-rollingn:year+rollingn]
            rrelevant = rcorrs[year-rollingn:year+rollingn]
            ncorr = sum(nrelevant)/len(nrelevant)
            rcorr = sum(rrelevant)/len(rrelevant)
            ncorrs_rolling.append(ncorr)
            rcorrs_rolling.append(rcorr)
        return ncorrs_rolling, rcorrs_rolling
    def correlationPlot(self, fname=None):
        ncorrs_rolling, rcorrs_rolling = self.rollingCorrs(self._makeCorrelations())
        self.plotDiff(ncorrs_rolling, rcorrs_rolling,
            min(list(self.corpus.keys())), save=fname)
    def byschool(self, schools=None, fname=None):
        if schools is None: schools = self.schools
        for school in schools:
            s_imagesbyyear = self.school_raw[school]
            s_images_concat = self._concatImages(s_imagesbyyear)
            s_rcorrs, s_ncorrs = self._makeCorrelations(corpus=s_images_concat)
            rcorrs, ncorrs = self._makeCorrelations(corpus=s_images_concat)
            s_ncorrs_rolling, s_rcorrs_rolling = self.rollingCorrs(rcorrs, ncorrs)
            self.plotDiff(s_ncorrs_rolling, s_rcorrs_rolling,
                min(list(s_images_concat.keys())), save=fname)


if __name__ == '__main__':
    tg = TimeGaussians()
    # Test on single image
    sampleimage = './../images/samples/Neoclassical/oath-of-the-horatii.jpg'
    sampledata = tg.generateSample(sampleimage, 'xy')
    similarity = tg.compareSample(sampledata, plot=True)
    # Generate plot for entire corpus
    tg.correlationPlot()









