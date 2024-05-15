from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .models import ChatBot
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import markdown
from Lassie.models import OwnerProfile, PetProfile, DogBreed

# Create your views here.
# add here to your generated API key
_ = load_dotenv('api_keys.env')
genai.configure(api_key=os.environ.get('gemini_api_key'))


@method_decorator(csrf_exempt, name='dispatch')
class asklassiechat(View):
    def post(self, request):
        ownerName = request.user.ownerprofile.firstName
        
        petsInfo = PetProfile.objects.filter(ownerprofile=request.user.ownerprofile)
        if petsInfo:
            pets = f'Hi, my name is {ownerName} and I currently have the following pets:'
            for pet in petsInfo:
                n = 1
                pet_name = pet.namePet
                pet_breed = pet.breed
                pet_age = pet.age
                pet_weight = pet.weight
                pet_size = pet.size
                pet_allergies = pet.allergies
                pets += f'\n\n#{n}.Pet Name: {pet_name}\nBreed: {pet_breed}\nAge: {pet_age}\nWeight: {pet_weight}\nSize: {pet_size}\nAllergies: {pet_allergies}'
                n += 1
            
        text = 'I have a question about my pets: '
        text += request.POST.get('message')
        prompt = f'{pets}\n\n{text}'
        
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        chat
        response = chat.send_message(prompt)
        lassie_response = markdown.markdown(response.text)
        return JsonResponse({'message': lassie_response})
    
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'chat_bot.html')

        