from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# ==========================================
# LOAD TRAINED MODEL
# ==========================================

with open("house_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# ==========================================
# LOAD MODEL PERFORMANCE
# ==========================================

with open("model_performance.pkl", "rb") as file:
    performance = pickle.load(file)

# ==========================================
# HISTORY
# ==========================================

prediction_history = []
comparison_history = []


# ==========================================
# PRICE PREDICTION FUNCTION
# ==========================================

def predict_price(
    location,
    area,
    bedrooms,
    bathrooms,
    floor,
    total_floors,
    parking,
    furnishing,
    property_type,
    amenities,
    age
):

    age_depreciation = age

    data = pd.DataFrame([{
        "location": location,
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "floor": floor,
        "total_floors": total_floors,
        "parking": parking,
        "furnishing": furnishing,
        "property_type": property_type,
        "amenities": amenities,
        "age_depreciation": age_depreciation
    }])

    result = model.predict(data)[0]

    return round(result, 2)


# ==========================================
# SMART PROPERTY INSIGHTS
# ==========================================

def get_property_insights(price, area, age):

    price_per_sqft = (price * 100000) / area
    price_per_sqft = round(price_per_sqft, 2)

    # ------------------------------------------
    # Age impact
    # ------------------------------------------

    if age <= 5:
        age_status = "Excellent"
        age_message = "This is a relatively new property with low age depreciation."

    elif age <= 10:
        age_status = "Good"
        age_message = "This property has moderate age and depreciation."

    elif age <= 20:
        age_status = "Average"
        age_message = "The property is older, so age has a noticeable impact on value."

    else:
        age_status = "Older"
        age_message = "Higher property age may significantly reduce estimated value."

    # ------------------------------------------
    # Value rating
    # ------------------------------------------

    if price_per_sqft >= 7000:
        value_rating = "Premium"

    elif price_per_sqft >= 4500:
        value_rating = "Good Value"

    else:
        value_rating = "Budget Friendly"

    # ------------------------------------------
    # Smart recommendation
    # ------------------------------------------

    if age <= 5 and price_per_sqft < 7000:

        recommendation = (
            "Strong option: newer property with comparatively reasonable pricing."
        )

    elif age <= 10:

        recommendation = (
            "Good option: check location, construction quality and amenities before buying."
        )

    elif age <= 20:

        recommendation = (
            "Consider renovation cost and maintenance before making a decision."
        )

    else:

        recommendation = (
            "Carefully inspect property condition and future maintenance expenses."
        )

    return {
        "price_per_sqft": price_per_sqft,
        "age_status": age_status,
        "age_message": age_message,
        "value_rating": value_rating,
        "recommendation": recommendation
    }


# ==========================================
# PROPERTY INVESTMENT SCORE
# ==========================================

def get_investment_score(
    price,
    area,
    age,
    bedrooms,
    bathrooms,
    parking,
    amenities
):

    score = 50

    # ------------------------------------------
    # Property age
    # ------------------------------------------

    if age <= 5:
        score += 15

    elif age <= 10:
        score += 8

    elif age <= 20:
        score -= 5

    else:
        score -= 12

    # ------------------------------------------
    # Size
    # ------------------------------------------

    if area >= 2000:
        score += 10

    elif area >= 1200:
        score += 6

    elif area >= 800:
        score += 3

    # ------------------------------------------
    # Bedrooms
    # ------------------------------------------

    if bedrooms >= 4:
        score += 7

    elif bedrooms == 3:
        score += 5

    elif bedrooms == 2:
        score += 2

    # ------------------------------------------
    # Bathrooms
    # ------------------------------------------

    if bathrooms >= 3:
        score += 5

    elif bathrooms == 2:
        score += 3

    # ------------------------------------------
    # Parking
    # ------------------------------------------

    if parking >= 2:
        score += 5

    elif parking == 1:
        score += 3

    # ------------------------------------------
    # Amenities
    # ------------------------------------------

    if amenities >= 7:
        score += 8

    elif amenities >= 4:
        score += 5

    elif amenities >= 2:
        score += 2

    # ------------------------------------------
    # Keep score between 0 and 100
    # ------------------------------------------

    score = max(0, min(100, score))

    # ------------------------------------------
    # Investment category
    # ------------------------------------------

    if score >= 80:

        category = "Strong Buy"
        message = (
            "This property has strong overall characteristics for consideration."
        )

    elif score >= 65:

        category = "Consider"
        message = (
            "This property looks reasonably attractive, but compare it with alternatives."
        )

    else:

        category = "Caution"
        message = (
            "Check price, property condition, location and future maintenance carefully."
        )

    return {
        "score": score,
        "category": category,
        "message": message
    }


# ==========================================
# PROPERTY DECISION SUMMARY
# ==========================================

def get_decision_summary(
    price,
    area,
    age,
    investment
):

    price_per_sqft = (price * 100000) / area
    price_per_sqft = round(price_per_sqft, 2)

    # ------------------------------------------
    # Age impact
    # ------------------------------------------

    if age <= 5:
        age_impact = "Low"
        age_impact_message = "Property age has a low negative impact on the estimated value."

    elif age <= 10:
        age_impact = "Moderate"
        age_impact_message = "Property age has a moderate impact on the estimated value."

    elif age <= 20:
        age_impact = "High"
        age_impact_message = "Property age has a noticeable negative impact on the estimated value."

    else:
        age_impact = "Very High"
        age_impact_message = "Higher age can significantly affect property value and maintenance."

    # ------------------------------------------
    # Overall decision
    # ------------------------------------------

    score = investment["score"]

    if score >= 80 and age <= 10:

        decision = "Recommended"
        decision_icon = "✅"
        decision_message = (
            "This property shows strong overall characteristics "
            "based on the selected features."
        )

    elif score >= 65:

        decision = "Worth Considering"
        decision_icon = "🟡"
        decision_message = (
            "This property can be considered, but compare price, "
            "location, condition and alternatives."
        )

    else:

        decision = "Needs Careful Review"
        decision_icon = "⚠️"
        decision_message = (
            "Review the property condition, pricing, age, "
            "maintenance and other alternatives carefully."
        )

    return {
        "estimated_price": price,
        "price_per_sqft": price_per_sqft,
        "age_impact": age_impact,
        "age_impact_message": age_impact_message,
        "value_rating": (
            "Premium"
            if price_per_sqft >= 7000
            else "Good Value"
            if price_per_sqft >= 4500
            else "Budget Friendly"
        ),
        "investment_score": investment["score"],
        "investment_category": investment["category"],
        "decision": decision,
        "decision_icon": decision_icon,
        "decision_message": decision_message
    }


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    comparison = None
    insights = None
    investment = None
    decision = None

    if request.method == "POST":

        # ==========================================
        # NORMAL PRICE PREDICTION
        # ==========================================

        if "predict" in request.form:

            location = request.form["location"]

            area = float(request.form["area"])
            bedrooms = int(request.form["bedrooms"])
            bathrooms = int(request.form["bathrooms"])

            floor = int(request.form["floor"])
            total_floors = int(request.form["total_floors"])

            parking = int(request.form["parking"])
            furnishing = int(request.form["furnishing"])

            property_type = int(request.form["property_type"])
            amenities = int(request.form["amenities"])

            age = float(request.form["age"])

            # ------------------------------------------
            # Predict price
            # ------------------------------------------

            prediction = predict_price(
                location,
                area,
                bedrooms,
                bathrooms,
                floor,
                total_floors,
                parking,
                furnishing,
                property_type,
                amenities,
                age
            )

            # ------------------------------------------
            # Smart insights
            # ------------------------------------------

            insights = get_property_insights(
                prediction,
                area,
                age
            )

            # ------------------------------------------
            # Investment score
            # ------------------------------------------

            investment = get_investment_score(
                prediction,
                area,
                age,
                bedrooms,
                bathrooms,
                parking,
                amenities
            )

            # ------------------------------------------
            # Property decision summary
            # ------------------------------------------

            decision = get_decision_summary(
                prediction,
                area,
                age,
                investment
            )

            # ------------------------------------------
            # Save prediction history
            # ------------------------------------------

            prediction_history.append({
                "location": location,
                "area": area,
                "bedrooms": bedrooms,
                "bathrooms": bathrooms,
                "floor": floor,
                "total_floors": total_floors,
                "parking": parking,
                "furnishing": furnishing,
                "property_type": property_type,
                "amenities": amenities,
                "age": age,
                "price": prediction
            })

        # ==========================================
        # PROPERTY COMPARISON
        # ==========================================

        elif "compare" in request.form:

            # ==========================================
            # PROPERTY 1
            # ==========================================

            location1 = request.form["location1"]

            area1 = float(request.form["area1"])
            bedrooms1 = int(request.form["bedrooms1"])
            bathrooms1 = int(request.form["bathrooms1"])

            floor1 = int(request.form["floor1"])
            total_floors1 = int(request.form["total_floors1"])

            parking1 = int(request.form["parking1"])
            furnishing1 = int(request.form["furnishing1"])

            property_type1 = int(request.form["property_type1"])
            amenities1 = int(request.form["amenities1"])

            age1 = float(request.form["age1"])

            # ==========================================
            # PROPERTY 2
            # ==========================================

            location2 = request.form["location2"]

            area2 = float(request.form["area2"])
            bedrooms2 = int(request.form["bedrooms2"])
            bathrooms2 = int(request.form["bathrooms2"])

            floor2 = int(request.form["floor2"])
            total_floors2 = int(request.form["total_floors2"])

            parking2 = int(request.form["parking2"])
            furnishing2 = int(request.form["furnishing2"])

            property_type2 = int(request.form["property_type2"])
            amenities2 = int(request.form["amenities2"])

            age2 = float(request.form["age2"])

            # ==========================================
            # PREDICT PROPERTY 1
            # ==========================================

            price1 = predict_price(
                location1,
                area1,
                bedrooms1,
                bathrooms1,
                floor1,
                total_floors1,
                parking1,
                furnishing1,
                property_type1,
                amenities1,
                age1
            )

            # ==========================================
            # PREDICT PROPERTY 2
            # ==========================================

            price2 = predict_price(
                location2,
                area2,
                bedrooms2,
                bathrooms2,
                floor2,
                total_floors2,
                parking2,
                furnishing2,
                property_type2,
                amenities2,
                age2
            )

            # ==========================================
            # FIND BETTER PROPERTY
            # ==========================================

            if price1 > price2:

                winner = "Property 1"

            elif price2 > price1:

                winner = "Property 2"

            else:

                winner = "Both properties have similar estimated prices"

            # ==========================================
            # COMPARISON RESULT
            # ==========================================

            comparison = {
                "location1": location1,
                "area1": area1,
                "bedrooms1": bedrooms1,
                "bathrooms1": bathrooms1,
                "floor1": floor1,
                "total_floors1": total_floors1,
                "parking1": parking1,
                "furnishing1": furnishing1,
                "property_type1": property_type1,
                "amenities1": amenities1,
                "age1": age1,
                "price1": price1,

                "location2": location2,
                "area2": area2,
                "bedrooms2": bedrooms2,
                "bathrooms2": bathrooms2,
                "floor2": floor2,
                "total_floors2": total_floors2,
                "parking2": parking2,
                "furnishing2": furnishing2,
                "property_type2": property_type2,
                "amenities2": amenities2,
                "age2": age2,
                "price2": price2,

                "winner": winner
            }

            # ==========================================
            # SAVE COMPARISON HISTORY
            # ==========================================

            comparison_history.append({

                "property1": {
                    "location": location1,
                    "area": area1,
                    "bedrooms": bedrooms1,
                    "bathrooms": bathrooms1,
                    "floor": floor1,
                    "total_floors": total_floors1,
                    "parking": parking1,
                    "furnishing": furnishing1,
                    "property_type": property_type1,
                    "amenities": amenities1,
                    "age": age1,
                    "price": price1
                },

                "property2": {
                    "location": location2,
                    "area": area2,
                    "bedrooms": bedrooms2,
                    "bathrooms": bathrooms2,
                    "floor": floor2,
                    "total_floors": total_floors2,
                    "parking": parking2,
                    "furnishing": furnishing2,
                    "property_type": property_type2,
                    "amenities": amenities2,
                    "age": age2,
                    "price": price2
                },

                "winner": winner
            })

    # ==========================================
    # SEND DATA TO HTML
    # ==========================================

    return render_template(
        "index.html",
        prediction=prediction,
        history=prediction_history,
        comparison=comparison,
        comparison_history=comparison_history,
        insights=insights,
        investment=investment,
        decision=decision,
        mae=performance["mae"],
        r2=performance["r2"]
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)