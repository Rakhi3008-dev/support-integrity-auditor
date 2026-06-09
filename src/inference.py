import joblib

def load_model(
    path="models/xgb_pipeline.pkl"
):
    return joblib.load(path)

def predict_ticket(
    model,
    sample
):

    prediction = model.predict(sample)

    probability = None

    if hasattr(
        model,
        "predict_proba"
    ):
        probability = (
            model
            .predict_proba(sample)
            .max()
        )

    return {
        "prediction": int(prediction[0]),
        "confidence":
        round(
            float(probability) * 100,
            2
        )
        if probability
        else None
    }