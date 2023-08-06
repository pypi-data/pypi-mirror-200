import abc
import time
from code_util.markdown import markdowndoc
from sample_util.SampleSet import SampleSet
from code_util.log import log_error, process_status_bar, log, log_level_enum
from code_util.structures import iter_idx
from code_util.plot import draw_line_chart
from ml_util.TrainableProcessModelBase import TrainableProcessModelBase, TrainableProcessState
from code_util.env import train_model_folder
from code_util.file import create_folder_if_not_exsited
from code_util.num import convert_2f_num
import tensorflow as tf
import numpy as np
import pickle, os


class TFTrainableProcessState(TrainableProcessState):
    """
    基于TF框架的过程状态类的默认实现
    """

    def __init__(self, doc_out=None):
        """
        初始化
        """
        self.all_epoch_loss = []
        self.current_epoch_loss = []
        self.doc_out = doc_out

        self.batch_cost = 0
        self.batch_count = 0
        self._temp_batch_start = 0

        self.epoch_cost_list = []

        self.report_filename = f"tradoc_{time.time()}.md"
        self.loss_chart_filename = f"chart_{time.time()}.jpg"

        self.metrics_map = {}

    def _generator_report(self, epoch_index: int):
        if self.doc_out is None:
            return
        doc_path = os.path.join(train_model_folder, 'docs')
        chart_path = os.path.join(train_model_folder, 'docs', 'charts')
        create_folder_if_not_exsited(doc_path)
        create_folder_if_not_exsited(chart_path)

        file_name = self.report_filename

        mkd = markdowndoc(os.path.join(doc_path, file_name))
        self._write_report_for_train_state(epoch_index, mkd)
        self._write_report_for_loss_state(epoch_index, mkd)
        self._write_report_for_metrics_state(mkd)
        mkd.flush()

    def _write_report_for_metrics_state(self, mkd: markdowndoc):
        if len(self.metrics_map) == 0:
            return
        chart_path = os.path.join(train_model_folder, 'docs', 'charts')

        mkd.write_title("评估值", 1)
        for key in self.metrics_map.keys():
            mkd.write_title(key, 2)
            min_value_index = np.argmin(self.metrics_map[key])
            max_value_index = np.argmax(self.metrics_map[key])

            filename = f"{key}_{time.time()}.jpg"
            draw_line_chart(os.path.join(chart_path, filename), ["epoch", key],
                            [x for x in self.metrics_map[key]])
            mkd.write_img(os.path.join("charts", filename))

            mkd.write_table(["", "epoch index", "value"], [
                ['最小值', str(min_value_index), str(self.metrics_map[key][min_value_index])],
                ['最大值', str(max_value_index), str(self.metrics_map[key][max_value_index])],
                ['最新值', str(len(self.metrics_map[key]) - 1), str(self.metrics_map[key][-1])]
            ])

    def _write_report_for_train_state(self, epoch_index, mkd: markdowndoc):
        mkd.write_title("训练参数", 1)

        mkd.write_title("训练迭代参数", 2)
        mkd.write_line(
            f"- 总训练轮数： {epoch_index + 1}次")
        mkd.write_line(
            f"- 平均每次训练的时间： {(convert_2f_num(sum(self.epoch_cost_list))) if len(self.epoch_cost_list) != 0 else 0}秒")
        mkd.write_line(
            f"- 平均每个batch的训练时间： {convert_2f_num(self.batch_cost / self.batch_count) if self.batch_count != 0 else 0}秒")

    def _write_report_for_loss_state(self, epoch_index, mkd: markdowndoc):
        chart_path = os.path.join(train_model_folder, 'docs', 'charts')
        mkd.write_title("损失值", 1)

        mkd.write_title("损失值曲线", 2)
        filename = self.loss_chart_filename
        draw_line_chart(os.path.join(chart_path, filename), ["epoch", "loss"],
                        [x for x in self.all_epoch_loss])
        mkd.write_img(os.path.join("charts", filename))

        # 打印若干loss
        mkd.write_title("损失值详情", 2)
        if len(self.all_epoch_loss) < 10:
            mkd.write_table(['epoch index', 'loss'], [[x, y] for y, x in iter_idx(self.all_epoch_loss)])
        else:
            alph = len(self.all_epoch_loss) / 10
            select_list = [round(x * alph) for x in range(10)]
            if select_list[-1] != len(self.all_epoch_loss) - 1:
                select_list.append(len(self.all_epoch_loss) - 1)
            select_loss = [[i, self.all_epoch_loss[i]] for i in select_list]
            mkd.write_table(['epoch index', 'loss'], select_loss)

        mkd.write_title("损失值统计", 2)
        mkd.write_title("最小损失", 3)
        min_index = np.argmin(self.all_epoch_loss)
        mkd.write_line(f"- epoch index: {min_index}")
        mkd.write_line(f"- loss value: {self.all_epoch_loss[min_index]}")

    def event_begin_epoch(self, epoch_index: int,
                          model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        pass

    def event_end_epoch(self, epoch_index: int,
                        model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        self.all_epoch_loss.append(sum(self.current_epoch_loss))
        self.current_epoch_loss.clear()

        if len(self.all_epoch_loss) > 1:
            process_bar.print_log(f"Epoch Loss：{self.all_epoch_loss[-2]} -> {self.all_epoch_loss[-1]}")
        else:
            process_bar.print_log(f"Epoch Loss：{self.all_epoch_loss[-1]}")

        model.save(f"train_model_{epoch_index}")

        self.epoch_cost_list.clear()

        eva_result = train_obj.evaluate()

        if eva_result is not None:
            for eva_key in eva_result:
                if eva_key not in self.metrics_map:
                    self.metrics_map[eva_key] = []
                self.metrics_map[eva_key].append(eva_result[eva_key])

        self._generator_report(epoch_index)

    def event_begin_batch(self, batch_index: int, epoch_index: int,
                          model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        self._temp_batch_start = time.time()

    def event_end_batch(self, batch_index: int, epoch_index: int,
                        model: TrainableProcessModelBase, process_bar: process_status_bar, train_obj):
        process_bar.process_print(f"Batch Loss：{self.current_epoch_loss[-1]}")
        curr_cost = time.time() - self._temp_batch_start
        self.epoch_cost_list.append(curr_cost)
        self.batch_cost += curr_cost
        self.batch_count += 1

    def add_epoch_loss(self, loss_value):
        """
        累加epoch的loss
        :param loss_value: loss
        :return: 无返回
        """
        self.current_epoch_loss.append(loss_value)


class TFModelBase(TrainableProcessModelBase):
    """
    基于TF框架的Model的抽象类，继承自TrainableProcessModelBase
    """

    def __init__(self, name):

        self._input_tensors = self.define_input()
        self._output_tensor = self.diagram(self._input_tensors)

        self._model = tf.keras.Model(inputs=self._input_tensors, outputs=self._output_tensor)
        self._model.compile()
        self._model.summary()

        self._init_model = True

        super().__init__(name, self._model)

    @abc.abstractmethod
    def define_input(self):
        pass

    @abc.abstractmethod
    def optimizer_obj(self):
        pass

    @abc.abstractmethod
    def diagram(self, input_tensors):
        pass

    @abc.abstractmethod
    def cal_loss(self, intput, model_result, label):
        pass

    def train(self, input, lable, state_obj: TFTrainableProcessState, **kwargs):

        if kwargs['debug']:
            self.diagram(input)
            log_error("debug model finished.")

        with tf.GradientTape() as tape:
            pre_result = self._model(input)
            loss = self.cal_loss(input, pre_result, lable)

        trainable_weights = self._model.trainable_weights
        gradients = tape.gradient(loss, trainable_weights)
        self.optimizer_obj().apply_gradients(zip(gradients, trainable_weights))

        state_obj.add_epoch_loss(loss.numpy())

    def load(self, model_key: str):
        path = os.path.join(train_model_folder, f'{self.Name}_{model_key}.model')
        self.load_by_path(path)

    def load_by_path(self, path: str):
        if not os.path.exists(path):
            log_error("没有此模型")

        with open(path, "rb") as f:
            model_dict = pickle.load(f)

        self._model.set_weights(model_dict['weight'])

    def save(self, model_key: str):
        create_folder_if_not_exsited(train_model_folder)

        model_dict = {'weight': self._model.trainable_weights}

        with open(os.path.join(train_model_folder, f'{self.Name}_{model_key}.model'), "wb") as f:
            pickle.dump(model_dict, f)

    def load_last_model(self):
        last_file = None
        last_createtime = 0

        list_file = os.walk(train_model_folder)
        for root, dirs, files in list_file:
            for f in files:
                if f.startswith(self.Name):
                    file_fullpath = os.path.join(train_model_folder, f)
                    create_time = os.path.getctime(file_fullpath)
                    if create_time > last_createtime:
                        last_file = file_fullpath
                        last_createtime = create_time

        if last_file is not None:
            self.load_by_path(last_file)
            log(f"加载{last_file}模型")
