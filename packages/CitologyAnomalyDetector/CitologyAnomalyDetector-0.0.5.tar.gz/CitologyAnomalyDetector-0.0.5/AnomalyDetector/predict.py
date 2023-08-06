from fastai.vision.all import *
import dill
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Download model
from tqdm import tqdm
import urllib.request

thresh = 0.047
learnPath = str(Path.home())+f"{os.sep}.anomalydetection{os.sep}"+ "anomalydetector.pkl"

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

url = "https://dl.dropboxusercontent.com/s/q6ktdm5yh2y1vvu/anomalydetector.pkl?dl=0"


def get_dls(path, bs:int, size:int):
  "Generates two `GAN` DataLoaders"
  dblock = DataBlock(blocks=(ImageBlock, ImageBlock),
                   get_items=get_image_files,
                   get_y = lambda x: path/x.parent.name/x.name,
                   splitter=FuncSplitter(lambda x: Path(x).parent.name == 'valid'),
                   item_tfms=Resize(size),
                   batch_tfms=[*aug_transforms(max_zoom=2.),
                               Normalize.from_stats(*imagenet_stats)])
  dls = dblock.dataloaders(path, bs=bs, path=path)
  dls.c = 3 # For 3 channel image
  return dls

def predict(path):
    if  not os.path.exists(learnPath):
        with DownloadProgressBar(unit="B", unit_scale=True,
                                 miniters=1, desc=url.split("/")[-1]) as t:
            os.makedirs(os.path.dirname(learnPath), exist_ok=True)
            urllib.request.urlretrieve(url, filename=learnPath, reporthook=t.update_to)

    
    learn1 = load_learner(learnPath,pickle_module=dill)
    pathI = Path(path)
    dls_gen = get_dls(pathI, 64, 64)
    dlValid = dls_gen.valid.new(shuffle=False, drop_last=False, 
                       after_batch=[IntToFloatTensor, Normalize.from_stats(*imagenet_stats)])
    preds,real = learn1.get_preds(dl=dlValid)

    

    errors = []
    for (image, recon) in zip(real, preds):
        # compute the mean squared error between the ground-truth image
        # and the reconstructed image, then add it to our list of errors
        mse = np.mean(np.array((image - recon) ** 2))
        errors.append(mse)

    idxs = np.where(np.array(errors) >= thresh)[0]

    names = dlValid.dataset.items

    res = []
    for idx in idxs:
        res.append([names[idx],Path(str(names[idx]).split(' ')[0]).name,str(names[idx]).split('_')[-1].split('.')[0],errors[idx]])
    df = pd.DataFrame(res,columns=['path','imageName','roi','error'])
    df.to_csv(path+'result.csv',index=None)




