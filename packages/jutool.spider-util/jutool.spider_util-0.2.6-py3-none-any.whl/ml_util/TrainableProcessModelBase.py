import abc
from code_util.log import process_status_bar


class TrainableProcessModelBase(metaclass=abc.ABCMeta):
    """
    基于迭代训练模型的基类（抽象类）
    """

    def __init__(self, name: str, model):
        """
        初始化
        :param name: 模型名称
        """
        self._name = name
        self._model = model

    @property
    def Name(self):
        """
        属性——模型名称
        :return: 返回名称
        """
        return self._name

    @property
    def Model_Ref(self):
        return self._model

    def __call__(self, *args, **kwargs):
        """
        同predict方法
        :param args: 参数
        :param kwargs: 参数
        :return: 结果
        """
        return self._model(args, )

    @abc.abstractmethod
    def train(self, input, lable, state_obj, **kwargs):
        """
        训练过程
        :param input: 训练集的batch,其中input为convert_input后的Input
        :param lable: 训练集的label
        """
        pass

    @abc.abstractmethod
    def load(self, model_key: str):
        """
        模型的加载
        :param model_key: 模型的标识key
        :return: 无返回
        """
        pass

    @abc.abstractmethod
    def save(self, model_key: str):
        """
        模型的存储
        :param model_key: 存储的标识key
        :return: 无返回
        """
        pass


class TrainableProcessState(metaclass=abc.ABCMeta):
    """
    训练过程的状态记录的处理类（抽象类）
    """

    def event_begin_batch(self, batch_index: int, epoch_index: int,
                          model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        """
        每个batch训练开始前触发
        :param train_obj: 训练的过程引用
        :param epoch_index: epoch index
        :param batch_index: batch训练的index
        :param model: 训练的model
        :param process_bar: 训练的状态条
        :return: 无
        """
        pass

    def event_end_batch(self, batch_index: int, epoch_index: int,
                        model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        """
        每个batch训练后触发
        :param train_obj: 训练的过程引用
        :param epoch_index: epoch index
        :param batch_index: batch训练的index
        :param model: 训练的model
        :param process_bar: 训练的状态条
        :return: 无
        """
        pass

    def event_begin_epoch(self, epoch_index: int,
                          model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        """
        每个batch训练完成的Event
        :param train_obj: 训练的过程引用
        :param epoch_index: epoch index
        :param model: 训练的model
        :param process_bar: 训练的状态条
        :return: 无
        """
        pass

    def event_end_epoch(self, epoch_index: int,
                        model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        """
        每个epoch训练完成的Event
        :param train_obj: 训练的过程引用
        :param epoch_index: epoch index
        :param model: 训练的model
        :param process_bar: 训练的状态条
        :return: 无
        """
        pass
