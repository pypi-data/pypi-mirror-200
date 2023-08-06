# from nlp_util.TFModelBase import TFModelBase
# from nlp_util.default_process import default_process_setting, process_enum
# from Models.doc_classification.AttentionCustom import MultiHeadAttention_
# import tensorflow as tf
# import numpy as np
# import abc
#
#
# class Trainable_BertModelBase(TFModelBase):
#
#     def __init__(self, name: str, bert_token_maxlen=512, with_special_token=True):
#         pr_obj = default_process_setting.get_process_obj(process_enum.BertEmbedding)
#         self.tokenizer = pr_obj.tokenizer
#         self.model = pr_obj.model
#
#         self.setting_special_tokens = with_special_token
#         self.setting_max_doc_sentence = bert_token_maxlen
#
#         super().__init__(name)
#
#     def define_input(self):
#         return {
#             'input_ids': tf.keras.Input([self.setting_max_doc_sentence], dtype=tf.int32),
#             'token_type_ids': tf.keras.Input([self.setting_max_doc_sentence], dtype=tf.int32),
#             'attention_mask': tf.keras.Input([self.setting_max_doc_sentence], dtype=tf.int32)
#         }
#
#     def input_convert(self, input):
#         token_result = self.tokenizer(input, padding='max_length', max_length=self.setting_max_doc_sentence,
#                                       add_special_tokens=self.setting_special_tokens, truncation=True,
#                                       return_tensors='tf')
#
#         return token_result
#
#     def diagram(self, input_tensors):
#         embedding = self.model(input_tensors).last_hidden_state
#         return self.diagram_from_bert(embedding)
#
#     @abc.abstractmethod
#     def diagram_from_bert(self, bert_tensor):
#         pass
#
#
# class Nontrainable_BertModelBase(TFModelBase):
#
#     def __init__(self, name: str, bert_token_maxlen=512, with_special_token=True):
#         pr_obj = default_process_setting.get_process_obj(process_enum.BertEmbedding)
#         self.tokenizer = pr_obj.tokenizer
#         self.model = pr_obj.model
#
#         self.setting_special_tokens = with_special_token
#         self.setting_max_doc_sentence = bert_token_maxlen
#
#         super().__init__(name)
#
#     def define_input(self):
#         return {
#             'input_ids': tf.keras.Input([self.setting_max_doc_sentence], dtype=tf.int32),
#             'token_type_ids': tf.keras.Input([self.setting_max_doc_sentence], dtype=tf.int32),
#             'attention_mask': tf.keras.Input([self.setting_max_doc_sentence], dtype=tf.int32),
#             'embedding': tf.keras.Input([self.setting_max_doc_sentence, 256], dtype=tf.float32)
#         }
#
#     def input_convert(self, input):
#         token_result = self.tokenizer(input, padding='max_length', max_length=self.setting_max_doc_sentence,
#                                       add_special_tokens=self.setting_special_tokens, truncation=True,
#                                       return_tensors='tf')
#         embedding = self.model(**token_result).last_hidden_state
#         return {
#             'input_ids': token_result.data['input_ids'],
#             'token_type_ids': token_result.data['token_type_ids'],
#             'attention_mask': token_result.data['attention_mask'],
#             'embedding': embedding
#         }
#
#     def diagram(self, input_tensors):
#         return self.diagram_from_bert(input_tensors)
#
#     @abc.abstractmethod
#     def diagram_from_bert(self, bert_tensor):
#         pass
