"""Place review endpoint and place API models."""

from flask_restx import Namespace, Resource, fields
from app.services import facade


api = Namespace("places", description="Place operations")


user_model = api.model("PlaceOwner", {
    "id": fields.String(description="User ID"),
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name"),
    "email": fields.String(description="Email")
})


amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Amenity name")
})


review_model = api.model("PlaceReview", {
    "id": fields.String(description="Review ID"),
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(
        description="Rating of the place (1-5)"
    ),
    "user_id": fields.String(description="ID of the user")
})


place_model = api.model("Place", {
    "title": fields.String(
        required=True,
        description="Title of the place"
    ),
    "description": fields.String(
        description="Description of the place"
    ),
    "price": fields.Float(
        required=True,
        description="Price per night"
    ),
    "latitude": fields.Float(
        required=True,
        description="Latitude"
    ),
    "longitude": fields.Float(
        required=True,
        description="Longitude"
    ),
    "owner_id": fields.String(
        required=True,
        description="ID of the owner"
    ),
    "owner": fields.Nested(
        user_model,
        description="Owner of the place"
    ),
    "amenities": fields.List(
        fields.Nested(amenity_model),
        description="List of amenities"
    ),
    "reviews": fields.List(
        fields.Nested(review_model),
        description="List of reviews"
    )
})


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):

    @api.response(
        200,
        "List of reviews for the place retrieved successfully"
    )
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place."""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {"error": "Place not found"}, 404

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating
            }
            for review in reviews
        ], 200
