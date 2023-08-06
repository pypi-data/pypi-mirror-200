snippet

from baseten.training import finetune
from baseten.training import Dataset, PublicUrl
from baseten.training import DreamboothConfig

input_data = Dataset("ZWB5Lqk")
# OR input_data = PublicUrl("https://path-to-dataset.com")
config = DreamboothConfig(
    instance_prompt="photo of sks",
    input_dataset=input_data,
    wandb_api_key="83b673c1371752f6177aafc403be4663970505c1",
)

fr = finetune("sid-photo-model-12", config)
