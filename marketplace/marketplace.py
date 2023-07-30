import os
import random

from flask import Flask, render_template
import grpc

from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)
recommendations_client = RecommendationsStub(recommendations_channel)


@app.route("/")
def render_homepage():

    all_categories = list(BookCategory.values())
    random_category = random.choice(all_categories)

    recommendations_request = RecommendationRequest(
        user_id=1, category=random_category, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )

    return render_template(
        "homepage.html",
        recommendations=recommendations_response.recommendations,
        category=random_category,
    )