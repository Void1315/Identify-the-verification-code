from sklearn.svm import SVC
import numpy as np
from sklearn.externals import joblib
class ImgTostring:
    # params = [{'kernel' : 'linear'},
    #           {'kernel': 'poly','degree':'3'}
    #           ]
    params = {'kernel': 'poly', 'degree': 3}
    classifier = None
    X = []
    y = []
    model_file = "data/train_model.m"
    def __init__(self):
        self.classifier = SVC(**self.params)
        
    def load_model(self,file = "data/train_model.m"):
        self.classifier = joblib.load(file)
        return self
    
    def train_svm(self,X_train=None,y_train=None):
        if len(self.X)==0:self.get_svm_feature()
        if X_train is None:X_train = self.X
        if y_train is None:y_train = self.y
        the_x = np.array(X_train)
        the_y = np.array(y_train)
        print("********开始训练**************")
        self.classifier.fit(the_x,the_y)
        print("***********训练结束**************")
        return self
    
    def save_classifier(self,model_file="data/train_model.m"):
        joblib.dump(self.classifier, model_file)
        print("****************模型已保存********************")
        return self
    
    def predict(self,X):
        return self.classifier.predict(X)

    def get_svm_feature(self,src = "data/model.txt"):
        self.X = []
        self.y = []
        with open(src, 'r') as f:
            lines = f.readlines()
            for line in lines:
                the_list = line.split(" ")
                self.y.append(int(the_list[0]))
                self.X_ = line[2:-1].split(" ")
                xx = []
                for x in self.X_:
                    a = x.split(":")[1:]
                    if len(a) is not 0:
                        xx.append(int(a[0]))
                self.X.append(xx)
        return self.X, self.y
    def get_accuracy(self,test_size = 0.25,random_state = 5):
        """"""
        if len(self.X)==0:
            self.get_svm_feature()
        from sklearn import cross_validation
        from sklearn.metrics import classification_report
        target_name = [chr(a) if a>9 else str(a) for a in set(self.y)]
        X_train, X_text, y_train, y_test = cross_validation.train_test_split(self.X,self.y,test_size=test_size,random_state=random_state)
        self.train_svm(X_train,y_train)
        print(classification_report(y_test, self.predict(X_text),target_names=target_name))
        pass
        
if __name__=="__main__":
    the_obj = ImgTostring()
    the_obj.get_accuracy()