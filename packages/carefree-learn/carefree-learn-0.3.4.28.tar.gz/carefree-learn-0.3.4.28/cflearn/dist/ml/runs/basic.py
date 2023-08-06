import os
import cflearn

from cflearn.data.ml import MLCarefreeData
from cflearn.api.ml.pipeline import MLPipeline
from cflearn.api.ml.pipeline import MLCarefreePipeline

from ._utils import get_info


if __name__ == "__main__":
    info = get_info()
    kwargs = info.kwargs
    data = info.data
    assert data is not None
    cuda = info.meta["cuda"]
    carefree = isinstance(data, MLCarefreeData)
    m_base = MLCarefreePipeline if carefree else MLPipeline
    config = m_base.config_base(**kwargs)
    m = m_base(config).fit(data, cuda=cuda)
    m.save(os.path.join(info.workplace, cflearn.ML_PIPELINE_SAVE_NAME))
