from __future__ import print_function
from nerm.neuroner import neuromodel
from mask import masking
from nerm.configuration import Configuration
from nerm import helper
import warnings
warnings.filterwarnings('ignore')

cf = Configuration()
TRAINED_MODEL = cf.trained_model
NER_OUTPUT = "data/mask_input/"
SPACY_LANGUAGE = "en_core_web_sm"

def call_nerm(upload_folder, download_folder, zip_file_required):
    perform_ner(upload_folder)
    mask()
    if(zip_file_required):
        return helper.get_zip_file(download_folder)
    else:
        return helper.get_masked_text(download_folder)

def perform_ner(upload_folder):
    nn = neuromodel.NeuroNER(train_model=False, use_pretrained_model=True, dataset_text_folder=upload_folder,
    pretrained_model_folder= TRAINED_MODEL, output_folder=NER_OUTPUT, spacylanguage=SPACY_LANGUAGE) 
    nn.fit()
    nn.close()

def mask():
    masking.main()
