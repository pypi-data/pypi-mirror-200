def early_stoping(min_delta = 0.001, patience=20):
    from tensorflow.keras import callbacks

    early_stopping = callbacks.EarlyStopping(
        min_delta=min_delta, # minimium amount of change to count as an improvement
        patience=patience, # how many epochs to wait before stopping
        restore_best_weights=True,
)

def save_model(model, model_name):
    # serialize model to JSON
    model_json = model.to_json()
    with open(f"{model_name}.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(f"{model_name}.h5")
    print("Saved model to disk")