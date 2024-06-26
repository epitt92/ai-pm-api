from rest_framework.decorators import api_view
from .models import Skill
from django.http import JsonResponse

from bson import ObjectId

def convertDBDataToJson(data):
    data_dict = data.to_mongo().to_dict()
    for key, value in data_dict.items():
        if isinstance(value, ObjectId):
            data_dict[key] = str(value)
    return data_dict

# Create your views here.
@api_view(['GET'])
def get_skills(request):
    skills = Skill.objects.all()
    # Serialize documents to JSON
    serialized_documents = [convertDBDataToJson(doc) for doc in skills]

    # Return JSON response
    return JsonResponse(serialized_documents, safe=False)