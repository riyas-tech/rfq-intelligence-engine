import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
import requests


CLOUD_RUN_RUL=""

#Call cloud run inference API

class CallInference(beam.DoFn):
    def process(self, element, *args, **kwargs):
        try:
            response = requests.post(CLOUD_RUN_RUL,
                                     json={"message": element},
                                     timeout=5
                                     )
            if response.status_code == 200:
                yield response.json()
            else:
                yield {"error" : element}

        except Exception as e:
            yield {"error": str(e), "input" : element}    

def run() :
    options = PipelineOptions(
        streaming = True,
        project = "project id",
        region = "us-central1",
        runner="DataflowRunner"
    )

    with beam.Pipeline(options=options) as p:
        (
            p
            | "Read From Pubsub" >> beam.io.ReadFromPubSub(
                topic="topic info"
            )
            | "Decod" >> beam.Map(lambda x: x.decode("utf-8"))
            | "CallInfrerenceService" >> beam.ParDo(CallInference())
            | "Print" >> beam.Map(print)
        )
        