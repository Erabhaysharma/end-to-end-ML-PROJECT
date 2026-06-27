import sys
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprosessor_obj_file=os.path.join('artifacts',"preprosessor.pkl")

class DataTransformer:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    
    def get_data_transformer(self):
        try:
            numerical_columns=["reading_score","writing_score"]
            categorical_columns=["gender","parental_level_of_education","lunch","test_preparation_course","race_ethnicity"]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]

            )
            cat_pipline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                
                ]
            )
            logging.info("categorical encodeing complited")
            logging.info("numerical columns scaling complited")

            preprosessor=ColumnTransformer(
                [
                   ("num_pipline",num_pipeline,numerical_columns),
                   ("cat_pipeline",cat_pipline,categorical_columns)
                ]
            )

            return preprosessor
        except Exception as e:
            raise CustomException(e,sys)
            


    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("read train and test complited")
            logging.info(" obtaining preprocessing object")

            preprosessing_obj=self.get_data_transformer()
            target_columns_name="math_score"
            numerical_columns=["reading_score","writing_score"]
            input_feature_train_df=train_df.drop(columns=[target_columns_name])
            target_feature_train_df=train_df[target_columns_name]
            input_feature_test_df=test_df.drop(columns=[target_columns_name])
            target_feature_test_df=test_df[target_columns_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprosessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprosessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprosessor_obj_file,
                obj=preprosessing_obj

            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprosessor_obj_file,
            )
        except Exception as e:


            raise CustomException(e,sys)
        




