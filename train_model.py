import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline


# ==========================================
# LOAD DATASET
# ==========================================

data = pd.read_csv("house_data.csv")


# ==========================================
# AGE DEPRECIATION FEATURE
# ==========================================

data["age_depreciation"] = data["age"]


# ==========================================
# FEATURES AND TARGET
# ==========================================

features = [
    "location",
    "area",
    "bedrooms",
    "bathrooms",
    "floor",
    "total_floors",
    "parking",
    "furnishing",
    "property_type",
    "amenities",
    "age_depreciation"
]

X = data[features]
y = data["price"]


# ==========================================
# CATEGORICAL FEATURES
# ==========================================

categorical_features = [
    "location"
]


# ==========================================
# NUMERIC FEATURES
# ==========================================

numeric_features = [
    "area",
    "bedrooms",
    "bathrooms",
    "floor",
    "total_floors",
    "parking",
    "furnishing",
    "property_type",
    "amenities",
    "age_depreciation"
]


# ==========================================
# PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "location",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# ==========================================
# MODEL
# ==========================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================================
# TRAIN MODEL
# ==========================================

model.fit(
    X_train,
    y_train
)


# ==========================================
# FORCE AGE COEFFICIENT TO BE NEGATIVE
# ==========================================

regressor = model.named_steps["regressor"]

feature_names = model.named_steps[
    "preprocessor"
].get_feature_names_out()

age_index = list(feature_names).index(
    "remainder__age_depreciation"
)

# Force age effect to always decrease price
regressor.coef_[age_index] = -abs(
    regressor.coef_[age_index]
)


# ==========================================
# TEST MODEL
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# MODEL PERFORMANCE
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("========================================")
print("     SMART HOME AI PRICE MODEL")
print("========================================")

print(
    "Mean Absolute Error:",
    round(mae, 2)
)

print(
    "R2 Score:",
    round(r2, 2)
)


print("\nModel Features:")

for feature in features:
    print("-", feature)


print("\nAge Logic:")
print("Newer property = Higher estimated price")
print("Older property = Lower estimated price")
print("Age coefficient forced to negative")


# ==========================================
# SAVE MODEL
# ==========================================

with open(
    "house_price_model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


# ==========================================
# SAVE PERFORMANCE
# ==========================================

model_performance = {
    "mae": round(mae, 2),
    "r2": round(r2, 2)
}


with open(
    "model_performance.pkl",
    "wb"
) as file:

    pickle.dump(
        model_performance,
        file
    )


print("\n========================================")
print("Model saved successfully!")
print("Performance data saved successfully!")
print("========================================")
