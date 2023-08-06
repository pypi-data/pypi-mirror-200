import abc, time, inspect
from code_util.file import safe_pickle
import os.path
from sample_util.SampleSet import SampleSet
from code_util.log import process_status_bar
from sample_util.NLSampleSource import NLSampleSourceBase, LocalDisk_NLSampleSource
from ml2_util.metrics import MetricsBase


class MLModel(metaclass=abc.ABCMeta):
    """
    基于迭代训练模型的基类（抽象类）
    """

    def __init__(self, name: str, load_model=None):
        """
        初始化
        :param name: 模型名称
        """
        self._name = name
        self._model = self.init_model()

        if load_model is not None:
            self.load(load_model)

    def load_in_trainfolder(self, folder, epoch_num=-1, batch_num=-1):
        if not os.path.exists(os.path.join(folder, "models")):
            print(f"warning: no the train folder path of '{os.path.join(folder, 'models')}'")
            return
        sp = safe_pickle(os.path.join(folder, 'train_datas'), 'state.pickle')
        save_info = sp.load()

        ep = epoch_num if epoch_num >= 0 else max(save_info['save_model_list'].keys())
        bp = batch_num if batch_num >= 0 else max(save_info['save_model_list'][ep].keys())

        if (ep not in save_info['save_model_list']) or (bp not in save_info['save_model_list'][ep]):
            raise Exception("no the target save model.")

        load_path = save_info['save_model_list'][ep][bp]
        self.load(os.path.join(folder, "models", load_path))

    @abc.abstractmethod
    def init_model(self) -> object:
        pass

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

    def predict(self, input: [], return_logit=False):
        c_input = self.convert_in(input)
        logit = self.Model_Ref(c_input)
        c_output = self.convert_out(logit)
        if return_logit:
            return (c_output, logit)
        else:
            return c_output

    def _call(self, input: []):
        return self.Model_Ref(input)

    @abc.abstractmethod
    def convert_in(self, data, lable=None):
        pass

    @abc.abstractmethod
    def convert_out(self, logit):
        pass

    @abc.abstractmethod
    def load(self, path: str):
        """
        模型的加载
        :param model_key: 模型的标识key
        :return: 无返回
        """
        pass

    @abc.abstractmethod
    def save(self, path: str):
        """
        模型的存储
        :param model_key: 存储的标识key
        :return: 无返回
        """
        pass

    @abc.abstractmethod
    def backward_update(self, logit, convert_input, convert_output) -> float:
        pass


def Event_Batch_Begin(fn):
    fn.Event_Batch_Begin = True
    fn.is_wrapmethod = True
    return fn


def Event_Batch_End(fn):
    fn.Event_Batch_End = True
    fn.is_wrapmethod = True
    return fn


def Event_Epoch_Begin(fn):
    fn.Event_Epoch_Begin = True
    fn.is_wrapmethod = True
    return fn


def Event_Epoch_End(fn):
    fn.Event_Epoch_End = True
    fn.is_wrapmethod = True
    return fn


def Init_Func(fn):
    fn.init_func = True
    fn.is_wrapmethod = True
    return fn


class TrainConfig(metaclass=abc.ABCMeta):
    """
    训练过程的状态记录的处理类（抽象类）
    """

    def __init__(self, folderpath, sample_set_source: NLSampleSourceBase, sample_set_name: str,
                 batch_count: int,
                 testsample_set_source: NLSampleSourceBase = None, testsample_set_name: str = "",
                 epochs=1000, buffer_set_source: NLSampleSourceBase = None, ):
        self._max_epoch = epochs
        self._folder_path = folderpath
        self._buffer_set_samplesource = buffer_set_source
        self._sample_source = sample_set_source
        self._sample_set_name = sample_set_name
        self._testsample_source = testsample_set_source
        self._testsample_set_name = testsample_set_name

        self._batch_count = batch_count

        self.state = {}

        self._eventlist_batch_begin = []
        self._eventlist_batch_end = []
        self._eventlist_epoch_begin = []
        self._evnetlist_epoch_end = []
        self._init_functions = []
        self._metrics_fun_list = []

        if not os.path.exists(folderpath):
            raise Exception(f"Can't find the path of {folderpath}")

        self._log_file = open(os.path.join(folderpath, 'log.txt'), 'a')

        all_function = inspect.getmembers(type(self), inspect.isfunction)
        for a_method in all_function:
            if hasattr(a_method[1], "is_wrapmethod"):
                if hasattr(a_method[1], "Event_Batch_Begin"):
                    self._eventlist_batch_begin.append(a_method[1])
                if hasattr(a_method[1], "Event_Batch_End"):
                    self._eventlist_batch_end.append(a_method[1])
                if hasattr(a_method[1], "Event_Epoch_Begin"):
                    self._eventlist_epoch_begin.append(a_method[1])
                if hasattr(a_method[1], "Event_Epoch_End"):
                    self._evnetlist_epoch_end.append(a_method[1])
                if hasattr(a_method[1], "Evnet_Report_Loss"):
                    self._eventlist_loss_report.append(a_method[1])
                if hasattr(a_method[1], "init_func"):
                    self._init_functions.append(a_method[1])

        self._init_dict = {}
        for func in self._init_functions:
            func(self, self._init_dict)

        self._state_file = safe_pickle(os.path.join(folderpath, 'train_datas'), 'state.pickle')
        if not os.path.exists(os.path.join(folderpath, 'train_datas')):
            os.mkdir(os.path.join(folderpath, 'train_datas'))

        self._prepare()

    @property
    def base_folder(self):
        return self._folder_path

    @property
    def batch_count(self):
        return self._batch_count

    @property
    def epoch_num(self):
        return self.state['epoch_num']

    @epoch_num.setter
    def epoch_num(self, value):
        self.state['epoch_num'] = value

    @property
    def batch_num(self):
        return self.state['batch_num']

    @batch_num.setter
    def batch_num(self, value):
        self.state['batch_num'] = value

    @property
    def max_epoch_count(self):
        return self._max_epoch

    @property
    def ori_set_source(self):
        return self._sample_source

    @property
    def ori_set_name(self):
        return self._sample_set_name

    @property
    def ori_testset_source(self):
        return self._testsample_source

    @property
    def ori_testset_name(self):
        return self._testsample_set_name

    @property
    def buffer_set_source(self):
        return self._buffer_set_samplesource

    @property
    def buffer_set_name(self):
        return self.state['buffer_set_name']

    @property
    def buffer_testset_name(self):
        return self.state['buffer_test_set_name']

    @property
    def invoke_set_source(self):
        if self.buffer_set_source is not None:
            return self.buffer_set_source
        return self.ori_set_source

    @property
    def invoke_set_name(self):
        if self.buffer_set_source is not None:
            return self.buffer_set_name
        return self.ori_set_name

    @property
    def invoke_testset_source(self):
        if self.buffer_set_source is not None:
            return self.buffer_set_source
        return self.ori_testset_source

    @property
    def invoke_testset_name(self):
        if self.buffer_set_source is not None:
            return self.buffer_testset_name
        return self.ori_testset_name

    @property
    def use_buffer_set(self):
        if self.buffer_set_source is not None:
            return True
        return False

    @abc.abstractmethod
    def convert_set_to_input_and_lable(self, row_data) -> ():
        pass

    def Invoke_Batch_Begin(self, model: MLModel, process_bar: process_status_bar, train_obj):
        for ivm in self._eventlist_batch_begin:
            ivm(self, model, process_bar, train_obj)

    def Invoke_Batch_End(self, loss, model: MLModel, process_bar: process_status_bar,
                         train_obj):
        for ivm in self._eventlist_batch_end:
            ivm(self, loss, model, process_bar, train_obj)

    def Invoke_Epoch_Begin(self, model: MLModel, process_bar: process_status_bar, train_obj):
        for ivm in self._eventlist_epoch_begin:
            ivm(self, model, process_bar, train_obj)

    def Invoke_Epoch_End(self, model: MLModel, process_bar: process_status_bar, train_obj):
        for ivm in self._evnetlist_epoch_end:
            ivm(self, model, process_bar, train_obj)

    def log(self, logstr):
        self._log_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "：" + logstr + "\n")
        self._log_file.flush()

    @property
    def save_model_list(self):
        return self.state["save_model_list"]

    @save_model_list.setter
    def save_model_list(self, value):
        self.state["save_model_list"] = value

    @property
    def metrics_result(self):
        return self.state["metrics_result"]

    @metrics_result.setter
    def metrics_result(self, value):
        self.state["metrics_result"] = value

    def add_metrics(self, metrices_base: MetricsBase):
        self._metrics_fun_list.append(metrices_base)

    @Event_Epoch_End
    def _metrics_oper(self, model: MLModel, process_bar: process_status_bar, train_obj):
        if len(self._metrics_fun_list) == 0:
            return

        if self.use_buffer_set:
            invoke_sampleset = SampleSet(self.invoke_testset_source, self.invoke_testset_name) \
                .func(lambda x: x['data']) \
                .batch(self.batch_count)
        else:
            invoke_sampleset = SampleSet(self.invoke_testset_source, self.invoke_testset_name) \
                .func(self.convert_set_to_input_and_lable) \
                .batch(self.batch_count)

        result_dict = {
            'result': [],
            'logits': [],
            'labels': []
        }

        for sample in invoke_sampleset:
            m_input = [s[0] for s in sample]
            m_label = [s[1] for s in sample]

            result, logits = model.predict(m_input, return_logit=True)

            for r, l, lbs in zip(result, logits, m_label):
                result_dict['result'].append(r)
                result_dict['logits'].append(l)
                result_dict['labels'].append(lbs)

        for mv in self._metrics_fun_list:
            mv.call(self, result_dict['logits'], result_dict['labels'], result_dict['result'])

    def _prepare(self):

        if not self._state_file.exsite():
            self.state = {
                "init_completed": False,
                "epoch_num": 0,
                "batch_num": 0,
                "save_model_list": {},
                "metrics_result": {}
            }
        else:
            self.state = self._state_file.load()
            self.state['batch_num'] = 0

        if self.state['init_completed']:
            return

            # buffer
        if self.buffer_set_source is not None:

            self.buffer_set_source.create_new_set("train_set", "", [], ["data"], "")

            ori_sample_set = SampleSet(self.ori_set_source, self.ori_set_name).func(self.convert_set_to_input_and_lable)

            for item in ori_sample_set:
                self.buffer_set_source.add_row("train_set", [item])

            self.buffer_set_source.flush()
            self.state['buffer_set_name'] = "train_set"

            if self.ori_testset_source is not None:
                self.buffer_set_source.create_new_set("test_set", "", [], ["data"], "")

                ori_sample_set = SampleSet(self.ori_testset_source, self.ori_testset_name).func(
                    self.convert_set_to_input_and_lable)

                for item in ori_sample_set:
                    self.buffer_set_source.add_row("test_set", [item])

                self.buffer_set_source.flush()
                self.state['buffer_test_set_name'] = "test_set"

        self.state['init_completed'] = True
        self.update_state()

    def update_state(self):
        self._state_file.dump(self.state)

    def _pipline_str(self):
        return f"{self.epoch_num}_{self.batch_num}"


class DefaultTrainConfig(TrainConfig):
    """
    状态类的默认实现
    """

    def __init__(self, folderpath, sample_set_source: NLSampleSourceBase, sample_set_name: str, batch_count: int,
                 sample_testset_source: NLSampleSourceBase, sample_testset_name: str,
                 epochs=1000, use_buffer_set_source=False):
        """
        初始化
        """
        if use_buffer_set_source:
            buffer_set = LocalDisk_NLSampleSource(os.path.join(folderpath, "data"))
        else:
            buffer_set = None

        super().__init__(folderpath, sample_set_source, sample_set_name, batch_count, epochs=epochs,
                         testsample_set_source=sample_testset_source, testsample_set_name=sample_testset_name,
                         buffer_set_source=buffer_set)

        if "train_options" not in self.state:
            self.state['epoch_data'] = []
            self.state['epoch_current'] = []
            self.state['batch_current'] = {}

            self.state['train_options'] = {
                "batch_cost": 0,
                "batch_count": 0,
                "epoch_cost": 0,
                "epoch_count": 0,
                "epoch_loss": []
            }

    @property
    def train_options(self):
        return self.state['train_options']

    @train_options.setter
    def train_options(self, value):
        self.state['train_options'] = value

    @property
    def batch_current(self):
        return self.state['batch_current']

    @batch_current.setter
    def batch_current(self, value):
        self.state['batch_current'] = value

    @property
    def epoch_data(self):
        return self.state['epoch_data']

    @epoch_data.setter
    def epoch_data(self, value):
        self.state['epoch_data'] = value

    @property
    def epoch_current(self):
        return self.state['epoch_current']

    @epoch_current.setter
    def epoch_current(self, value):
        self.state['epoch_current'] = value

    @Event_Batch_Begin
    def begin_batch(self, model: MLModel, process_bar: process_status_bar, train_obj):
        self.batch_current = {}
        self.batch_current['start_time'] = time.time()
        self.batch_current['batch_index'] = self.batch_num

    @Event_Batch_End
    def end_batch(self, loss, model: MLModel,
                  process_bar: process_status_bar, train_obj):
        self.batch_current['loss'] = float(loss.numpy())

        log_str = f"batch loss: {self.batch_current['loss']}"

        process_bar.process_print(log_str)
        self.log(log_str)

        self.batch_current['end_time'] = time.time()

        self.train_options['batch_count'] += 1
        self.train_options['batch_cost'] += self.batch_current['end_time'] - self.batch_current['start_time']

        self.epoch_current.append(self.batch_current)

    @Event_Epoch_Begin
    def begin_epoch(self, model: MLModel, process_bar: process_status_bar, train_obj):
        self.epoch_current = []

    @Event_Epoch_End
    def end_epoch(self, model: MLModel, process_bar: process_status_bar, train_obj):
        all_loss = sum([item['loss'] for item in self.epoch_current])
        cost = time.time() - self.epoch_current[0]['start_time']

        out_log = f"Epoch {self.epoch_num} finished - loss [{all_loss}]  cost [{cost}]"

        self.log(out_log)

        process_bar.print_log(out_log)

        self.train_options['epoch_count'] += 1
        self.train_options['epoch_cost'] += cost
        self.train_options['epoch_loss'].append(all_loss)

        self.epoch_data.append(self.epoch_current)


class MLModelBatchTrain:
    """
    基于数据Batch的训练迭代
    """

    def __init__(self, model: MLModel,
                 config: TrainConfig
                 ):
        """
        初始化
        :param model: 需要迭代的模型
        :param config: 模型训练的Config
        """
        self._model = model
        self._config = config

    def train(self):
        """
        训练方法
        """

        ps_bar = process_status_bar()

        if self._config.use_buffer_set:
            invoke_sampleset = SampleSet(self._config.invoke_set_source, self._config.invoke_set_name) \
                .func(lambda x: x['data']) \
                .batch(self._config.batch_count)
        else:
            invoke_sampleset = SampleSet(self._config.invoke_set_source, self._config.invoke_set_name) \
                .func(self._config.convert_set_to_input_and_lable) \
                .batch(self._config.batch_count)

        for epoch in ps_bar.iter_bar(range(self._config.max_epoch_count), value=self._config.epoch_num, key="epoch",
                                     max=self._config.max_epoch_count):
            self._config.Invoke_Epoch_Begin(self._model, ps_bar, self)

            for sample in ps_bar.iter_bar(invoke_sampleset, key="batch",
                                          max=invoke_sampleset.count()):
                self._config.Invoke_Batch_Begin(self._model, ps_bar, self)

                m_input = [s[0] for s in sample]
                m_label = [s[1] for s in sample]

                input_data, label_data = self._model.convert_in(m_input, lable=m_label)
                loss = self._model.backward_update(input_data, label_data)

                self._config.Invoke_Batch_End(loss, self._model, ps_bar, self)
                self._config.batch_num += 1

            self._config.Invoke_Epoch_End(self._model, ps_bar, self)
            self._config.epoch_num += 1
            self._config.batch_num = 0
            self._config.update_state()
