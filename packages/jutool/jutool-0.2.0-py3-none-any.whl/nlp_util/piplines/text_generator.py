import abc

from nlp_util.TFModelBase import TFModelBase


class generator_text(TFModelBase):

    @abc.abstractmethod
    def convert_input(self, sinput: str or [str]):
        pass

    @abc.abstractmethod
    def convert_output(self, logit):
        pass

    def execute(self, sinput: str or [str]):
        return self.convert_output(self.Model_Ref(self.convert_input(sinput)))

    def train(self):
        pass
