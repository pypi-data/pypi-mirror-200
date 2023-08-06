import time
from ml_util.MetricsBase import confusion_dic_2_matrix, MetricsBase
from ml_util.TrainableProcessModelBase import TrainableProcessModelBase, TrainableProcessState
from ml_util.IterationProcess import IterationProcess
from sample_util.NLSampleSource import NLSampleSourceBase
from sample_util.SampleSet import SampleSet
from code_util.log import process_status_bar
from code_util.buffer import buffer_item, get_buffer_item, has_item_key
from ml_util.IterationProcessModelBase import IterationProcessModelBase


class _generate_tfmodel_input_buffer_set(IterationProcessModelBase):
    def __init__(self, model: TrainableProcessModelBase, source: NLSampleSourceBase, tar_set_name: str,
                 pre_item_oper):
        super().__init__("generate_tfmodel_input_buffer_set")
        self.source = source
        self.target_set = tar_set_name
        self.model = model
        self.pre_item_func = pre_item_oper

    def prepare(self):
        self.source.create_new_set(self.target_set, "generate_tfmodel_input_buffer_set",
                                   ['buffer'], ['input', 'label'])

    def call(self, item, process_bar: process_status_bar, state=None):
        input_data, label = self.pre_item_func(item)

        if input_data == None or input_data == "":
            return

        input = self.model.input_convert(input_data)
        self.source.add_row(self.target_set, [input, label])
        self.source.flush()
        # process_bar.print_log(f"{label}")



class BatchTrain:
    """
    基于数据Batch的训练迭代
    """

    def __init__(self, model: TrainableProcessModelBase,
                 state_obj: TrainableProcessState,
                 epochs=1000,
                 parse_batch_func=None,
                 create_buffer_set=None,
                 buffer_set_source: NLSampleSourceBase = None,
                 session_id=None
                 ):
        """
        初始化
        :param model: 需要迭代的模型
        :param epochs: 最大epoch次数
        :param parse_batch_func: 样本预处理function
        :param create_buffer_set: 是否创建样本缓存set，None为不创建，否则填写缓存名字，若存在则直接训练，不训练会递归创建
        :param buffer_set_source: 创建缓存set的source
        :param session_id: 缓存创建的session key
        """
        self._model = model
        self._epochs = epochs
        self._buffer_set = create_buffer_set
        self._buffer_source = buffer_set_source
        self._pre_parse_batch_func = parse_batch_func

        self._eva_dataset = None
        self._eva_metrix = None

        if session_id is not None:
            self._session_prebuffer_id = session_id + "_prebuffer"
            self._session_train_id = session_id + "_train"
            self._session_eva_id = session_id + "_eva_prebuffer"

            if has_item_key(self._session_train_id):
                self.epoch_num, self.batch_num, self._train_state_obj = get_buffer_item(self._session_train_id)
            else:
                self.epoch_num = 0
                self.batch_num = 0
                self._train_state_obj = state_obj
        else:
            self._session_prebuffer_id = None
            self._session_train_id = None
            self._session_eva_id = None
            self.epoch_num = 0
            self.batch_num = 0
            self._train_state_obj = state_obj

    def train(self, sampleset: SampleSet, **kwargs):
        """
        训练方法
        :param kwargs: 向model train传递的参数
        :param sampleset: 数据的dataset
        :param parse_batch_func: 每batch数据的预处理过程,返回（input_data, label_data）
        :return: 无返回
        """

        ps_bar = process_status_bar()

        invoke_sampleset = sampleset
        if self._buffer_set is not None:
            buffer_create = _generate_tfmodel_input_buffer_set(self._model, self._buffer_source, self._buffer_set,
                                                               self._pre_parse_batch_func)
            process_ = IterationProcess(buffer_create, sampleset, session_id=self._session_prebuffer_id)
            process_.execute()

            invoke_sampleset = SampleSet(self._buffer_source, self._buffer_set)

        for epoch in ps_bar.iter_bar(range(self._epochs), value=self.epoch_num, key="epoch", max=self._epochs):
            if self.batch_num == 0:
                self._train_state_obj.event_begin_epoch(self.epoch_num, self._model, ps_bar, self)
                skip_count = 0
            else:
                skip_count = self.batch_num

            for sample in ps_bar.iter_bar(invoke_sampleset, key="batch", max=invoke_sampleset.count()):

                if skip_count != 0:
                    skip_count -= 1
                    continue

                self._train_state_obj.event_begin_batch(self.batch_num, self.epoch_num, self._model, ps_bar, self)

                if self._buffer_set is None:
                    m_input, m_label = self._pre_parse_batch_func(sample)
                    m_input = self._model.input_convert(m_input)
                else:
                    m_input = sample['input']
                    m_label = sample['label']

                self._model.train(m_input, m_label, self._train_state_obj, **kwargs)

                self._train_state_obj.event_end_batch(self.batch_num, self.epoch_num, self._model, ps_bar, self)
                self.batch_num += 1

                buffer_item(self._session_train_id, (self.epoch_num, self.batch_num, self._train_state_obj))

            # self._model.save(f"_{epoch}")

            self._train_state_obj.event_end_epoch(self.epoch_num, self._model, ps_bar, self)
            self.epoch_num += 1
            self.batch_num = 0
            buffer_item(self._session_train_id, (self.epoch_num, self.batch_num, self._train_state_obj))

    def set_evaluate(self, sampleset: SampleSet, metrics_list: [MetricsBase]):
        self._eva_dataset = sampleset
        self._eva_metrix = metrics_list

    def evaluate(self):
        if self._eva_dataset is None:
            return None
        invoke_sampleset = self._eva_dataset
        if self._buffer_set is not None:
            buffer_create = _generate_tfmodel_input_buffer_set(self._model, self._buffer_source,
                                                               self._buffer_set + "_eva",
                                                               self._pre_parse_batch_func)
            process_ = IterationProcess(buffer_create, invoke_sampleset, session_id=self._session_eva_id)
            process_.execute()

            invoke_sampleset = SampleSet(self._buffer_source, self._buffer_set + "_eva")

        confusion_matrix_dic = {}

        for sample in invoke_sampleset:
            if self._buffer_set is None:
                m_input, m_label = self._pre_parse_batch_func(sample)
                m_input = self._model.input_convert(m_input)
            else:
                m_input = sample['input']
                m_label = sample['label']

            value = self._model.output_convert(self._model.model_call(m_input))

            for v, l in zip(value, m_label):
                if l not in confusion_matrix_dic:
                    confusion_matrix_dic[l] = {}
                if v not in confusion_matrix_dic[l]:
                    confusion_matrix_dic[l][v] = 0
                confusion_matrix_dic[l][v] += 1

        confusion_matrix = confusion_dic_2_matrix(confusion_matrix_dic)

        metrics_result = {}
        for m in self._eva_metrix:
            metrics_result[m.name] = m.call(confusion_matrix)
        return metrics_result
