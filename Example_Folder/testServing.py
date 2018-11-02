from keras.models import load_model

class testServing(object): # The file is called MnistClassifier.py

    def __init__(self):
        # You can load your pre-trained model in here. The instance will be created once when the docker container starts running on the cluster.
        self.model = load_model('./test_model.h5')

    def predict(self,X,feature_names):
		 # X is a 2-dimensional numpy array, feature_names is a list of strings. This methods needs to return a numpy array of predictions.
        return self.model.predict(X)
