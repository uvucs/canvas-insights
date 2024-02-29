from prototype_model import PrototypeModel
from warnings import filterwarnings
filterwarnings('ignore')

model = PrototypeModel()
raw_data = model.get_data('1012~stsFWORrXnz34ONuVDEDh9rWVnfPXaI4PSirXmb5L3hCeyIdn4s4HjYGgZIkz5PT')
training_data = model.clean_data(raw_data)
preprocessed_data = model.preprocess_data(training_data=training_data)
model.run(preprocessed_data)