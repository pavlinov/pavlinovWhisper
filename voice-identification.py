import os

from pyannote.audio import Model
model = Model.from_pretrained("pyannote/embedding",
        use_auth_token="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") 

from pyannote.audio import Inference
inference = Inference(model, window="whole")
embedding1 = inference("Sounds/long-trump-2.wav")
embedding2 = inference("Sounds/long-trump-1.wav")
# `embeddingX` is (1 x D) numpy array extracted from the file as a whole.

embedding1_2d = embedding1.reshape(1, -1)
embedding2_2d = embedding2.reshape(1, -1)


from scipy.spatial.distance import cdist
distance = cdist(embedding1_2d, embedding2_2d, metric="cosine")[0,0]
print(distance)
# `distance` is a `float` describing how dissimilar speakers 1 and 2 are.
