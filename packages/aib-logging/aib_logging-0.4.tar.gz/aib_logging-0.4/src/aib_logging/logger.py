class aib_logger:
    from enum import Enum
    
    class Categories(Enum):
        MODEL = "Model"
        DATA = "Data"
        METRIC = "Metric"
        MODEL_SCORE = "Model_Score"
        OTHER = "Other"

    class Actions(Enum):
        CREATE="Create"
        UPDATE="Update"
        DELETE="Delete"
        UPLOAD="Upload"
        TRAINING_SCORE=0
        VALIDATION_SCORE=0
        TEST_SCORE=0
        OTHER="Other"
    
    class Severities(Enum):
        INFO="INFO"
        WARNING="WARNING"
        ERROR="ERROR"

    def __init__(self, project:str, pipeline_name:str="", logger_name:str="aib_custom_logger"):
        import logging
        import google.cloud.logging
        self.project=project
        self.pipeline_name=pipeline_name
        client = google.cloud.logging.Client(project=project)
        self.logger = client.logger(name=logger_name)

    def log(
        self,
        msg:str,
        category:Categories=Categories.OTHER,
        action:Actions=Actions.OTHER,
        training_score:Actions=Actions.TRAINING_SCORE,
        validation_score:Actions=Actions.VALIDATION_SCORE,
        test_score:Actions=Actions.TEST_SCORE,
        severity:Severities=Severities.INFO,
        extra_labels:list=[],
        object:dict={}
           ):
        import inspect
        payload={
            "pipeline_run_name":self.pipeline_name,
            "component_name": inspect.stack()[1].function,
            "project":self.project,
            "category":category.value,
            "action":action.value,
            "training_score":training_score.value,
            "validation_score":validation_score.value,
            "test_score":test_score.value,
            "extra_labels":extra_labels,
            "message":msg,
            "object":object
        }
        # Send the Log request
        self.logger.log_struct(payload, severity=severity.value)
