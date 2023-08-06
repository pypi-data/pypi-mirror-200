from ml2_util.MLModel import MLModel, Event_Batch_End, Init_Func, DefaultTrainConfig
import os, time
from code_util.file import create_folder_if_not_exsited
from code_util.markdown import markdowndoc
from code_util.plot import draw_line_chart
from code_util.structures import iter_idx
import numpy as np


class train_report_process():

    def _write_report_for_metrics_state(self, mkd: markdowndoc):
        if len(self.metrics_result) == 0:
            return
        chart_path = os.path.join(self.base_folder, "charts")  # os.path.join(train_model_folder, 'docs', 'charts')

        mkd.write_title("评估值", 1)
        for key in self.metrics_result.keys():
            mkd.write_title(key, 2)
            min_value_index = np.argmin(self.metrics_result[key])
            max_value_index = np.argmax(self.metrics_result[key])

            filename = f"{key}_img.jpg"
            draw_line_chart(os.path.join(chart_path, filename), ["epoch", key],
                            [x for x in self.metrics_result[key]])
            mkd.write_img(os.path.join("charts", filename))

            mkd.write_table(["", "epoch index", "value"], [
                ['最小值', str(min_value_index), str(self.metrics_result[key][min_value_index])],
                ['最大值', str(max_value_index), str(self.metrics_result[key][max_value_index])],
                ['最新值', str(len(self.metrics_result[key]) - 1), str(self.metrics_result[key][-1])]
            ])

    def _write_report_for_train_state(self, mkd: markdowndoc):
        mkd.write_title("训练参数", 1)

        mkd.write_title("训练迭代参数", 2)
        mkd.write_line(
            f"- 总训练轮数： {self.train_options['epoch_count']}次")
        if self.train_options['epoch_count'] != 0:
            mkd.write_line(
                f"- 平均每轮训练的时间： {self.train_options['epoch_cost'] / self.train_options['epoch_count']}秒")
            mkd.write_line(
                f"- 平均每个batch的训练时间： {self.train_options['batch_cost'] / self.train_options['batch_count']}秒")

    def _write_report_for_loss_state(self, mkd: markdowndoc):
        chart_path = os.path.join(self.base_folder, 'charts')
        mkd.write_title("损失值", 1)

        mkd.write_title("损失值曲线", 2)
        filename = f"chart_epoch_loss.jpg"
        draw_line_chart(os.path.join(chart_path, filename), ["epoch", "loss"],
                        [x for x in self.train_options['epoch_loss']])
        mkd.write_img(os.path.join("charts", filename))

        # 打印若干loss
        mkd.write_title("损失值详情", 2)
        if len(self.train_options['epoch_loss']) < 10:
            mkd.write_table(['epoch index', 'loss'], [[x, y] for y, x in iter_idx(self.train_options['epoch_loss'])])
        else:
            alph = len(self.train_options['epoch_loss']) / 10
            select_list = [round(x * alph) for x in range(10)]
            if select_list[-1] != len(self.train_options['epoch_loss']) - 1:
                select_list.append(len(self.train_options['epoch_loss']) - 1)
            select_loss = [[i, self.train_options['epoch_loss'][i]] for i in select_list]
            mkd.write_table(['epoch index', 'loss'], select_loss)

        mkd.write_title("损失值统计", 2)
        if len(self.train_options['epoch_loss']) > 0:
            mkd.write_title("最小损失", 3)
            min_index = np.argmin(self.train_options['epoch_loss'])
            mkd.write_line(f"- epoch index: {min_index}")
            mkd.write_line(f"- loss value: {self.train_options['epoch_loss'][min_index]}")

    @Event_Batch_End
    def report_generation(self, loss, model: MLModel, process_bar, train_obj):
        doc_path = os.path.join(self.base_folder, 'report.md')
        chart_path = os.path.join(self.base_folder, 'charts')
        create_folder_if_not_exsited(chart_path)

        mk = markdowndoc(doc_path)

        self._write_report_for_train_state(mk)
        self._write_report_for_loss_state(mk)
        self._write_report_for_metrics_state(mk)
        mk.flush()
