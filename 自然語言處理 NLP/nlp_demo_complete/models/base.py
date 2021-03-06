import string
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle


class BaseModel:
    def __init__(self):
        self.lematizer = WordNetLemmatizer()
        self.stop = stopwords.words('english')
        self.transtbl = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

        self.model = None
        self.vec = None

    # Load Vec
    def load_vec(self, vec_path, mode='rb'):
        with open(vec_path, mode) as pkl_file:
            self.vec = pickle.load(pkl_file)

    # Load Model
    def load_model(self, model_path, mode='rb'):
        with open(model_path, mode) as pkl_file:
            self.model = pickle.load(pkl_file)

    # Preprocessing
    def preprocessing(self, line:str) -> str:
        line = line.translate(self.transtbl)

        tokens = [self.lematizer.lemmatize(t.lower(), 'v')
                for t in word_tokenize(line)
                if t.lower() not in self.stop]

        return ' '.join(tokens)

    # Predict
    def predict(self, line):
        if not self.model or not self.vec:
            print('Model / Vec is not loaded')
            return ""
        
        line = self.preprocessing(line)
        features = self.vec.transform([line])
        return self.model.predict(features)[0]
