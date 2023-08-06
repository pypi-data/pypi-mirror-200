from mb_utils.src.logging import logger
from torch import nn
import torch
from torch.nn import functional as F
import torchvision
import torchvision.models as models

__all__ = ['ModelLoader']


class ModelLoader(nn.Module):
    def __init__(self, data : dict,logger=None):
        super().__init__()
        self._data= data 
        self._use_torchvision_models=self._data['use_torchvision_models']
        self._model_name=self._data['model_name']
        self._model_version=self._data['model_version']
        self._model_path=self._data['model_path']
        self._model_pretrained=self._data['model_pretrained']

    def model_type(self):
        """
        Function to get default model resnet, vgg, densenet, googlenet, inception, mobilenet, mnasnet, shufflenet_v2, squeezenet
        """
        model_final = self._model_name + self._model_version
        model_out = getattr(models.model_name,model_final)(pretrained=self._model_pretrained)            
        return model_out

    def model_params(self):
        pass        

    def get_model(self):
        """
        FUnction to get the model
        """
        # Check if the model is available in torchvision models

        if self._use_torchvision_models:
            try:
                # Try to load the model from the specified path
                if hasattr(models, self._model_name):
                    model_class = getattr(models, self._model_name)
                    if self._model_name in ['resnet', 'vgg', 'densenet', 'googlenet', 'inception', 'mobilenet', 'mnasnet', 'shufflenet_v2', 'squeezenet']:
                        # These models have pretrained weights available
                        self.model = self.model_type()  
            except FileNotFoundError:
                raise ValueError(f"Model {self._model_name} not found in torchvision.models.")

        else:
            self.model = self.model_params()
    
    def forward(self,x):
        return self.model(x)