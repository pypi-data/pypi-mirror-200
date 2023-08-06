from ml2_util.MLModel import MLModel, Event_Epoch_End, DefaultTrainConfig, Event_Batch_End
import os
from code_util.file import create_folder_if_not_exsited


class save_model_per_epoch():
    @Event_Epoch_End
    def save_model(self, model: MLModel, process_bar, train_obj):
        model_save_folder = os.path.join(self.base_folder, "models")
        create_folder_if_not_exsited(model_save_folder)

        file_name = f"model_{self._pipline_str()}.model"

        path = os.path.join(model_save_folder, file_name)
        model.save(path)

        if self.epoch_num not in self.state["save_model_list"]:
            self.state["save_model_list"][self.epoch_num] = {}

        self.state["save_model_list"][self.epoch_num][self.batch_num] = file_name
        self.log(f"Save model in {file_name}")


class save_model_per_batch():
    @Event_Batch_End
    def save_model(self, loss, model: MLModel, process_bar, train_obj):
        model_save_folder = os.path.join(self.base_folder, "models")
        create_folder_if_not_exsited(model_save_folder)

        file_name = f"model_{self._pipline_str()}.model"

        path = os.path.join(model_save_folder, f"model_{self._pipline_str()}.model")
        model.save(path)

        if self.epoch_num not in self.state["save_model_list"]:
            self.state["save_model_list"][self.epoch_num] = {}

        self.state["save_model_list"][self.epoch_num][self.batch_num] = file_name
        self.log(f"Save model in {file_name}")
