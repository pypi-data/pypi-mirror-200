from ml2_util.MLModel import MLModel
import os, pickle


class tf_modelstorage():

    def load(self, path: str):
        """
        模型的加载
        :param model_key: 模型的标识key
        :return: 无返回
        """
        with open(path, "rb") as f:
            model_dict = pickle.load(f)

        self.Model_Ref.set_weights(model_dict['weight'])

    def save(self, path: str):
        """
        模型的存储
        :param model_key: 存储的标识key
        :return: 无返回
        """

        model_dict = {'weight': self.Model_Ref.trainable_weights}

        with open(path, "wb") as f:
            pickle.dump(model_dict, f)
