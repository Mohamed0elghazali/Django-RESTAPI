from django.http import Http404
from django.shortcuts import render
from django.http.response import JsonResponse

from rest_framework import status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Guest, Movie, Reservation, Post
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer, PostSerializer
from .permissions import IsAuthorReadOnly

## 1- without rest framework and no model query --> static data
## FBV --> function based view
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'Name': 'Omar',
            'Mobile':  '01091174566',
        },
        {
            'id': 2,
            'Name': 'mohamed',
            'Mobile':  '010123456878', 
        }
    ]
    
    # safe = false ---> as data is not hashable
    return JsonResponse(guests, safe=False)


## 2- without rest framework and with model
## FBV 
def no_rest_with_model(request):
    data = Guest.objects.all()
    response = {
        "guests": list(data.values("name", "mobile"))
    }
    return JsonResponse(response)


# List --> GET
# Create --> POST
# pk query --> GET with a key
# Update --> PUT
# Delete --> DELETE

##3- FBV --> Function Based View
# 3.1 GET POST 

@api_view(['GET', 'POST'])
def FBV_List(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 3.2 GET PUT DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExists:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE 
    if request.method == 'DELETE':
        guest.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


## 4- CBV ---> class based view
# 4.1 GET - POST
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
    
# 4.2 GET - PUT - DELETE
class CBV_pk(APIView):

    def get_object(self, pk):
        try:
            return Guest.objects.get(pk = pk)
        except Guest.DoesNotExists:
            raise Http404
    
    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

## 5- Mixins ---> extention for class based view 
# 5.1 Mixins List GET - POST
class mixins_list(
    mixins.ListModelMixin,     # for listing ---> get method 
    mixins.CreateModelMixin,   # for creating ---> post method
    generics.GenericAPIView,   # it reply as the api 
):
    # query set must be written like this questset
    # serializer class set must be written like this serializer_class
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    # the mixins List and Create do every thing to us.
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


    ## adding authentication and permissions for that views only.
    # authentication_classes  = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    ## adding authentication using TokenAuthentication
    authentication_classes = [TokenAuthentication]

# 5.2 Mixins GET - PUT - DELETE
class mixins_pk(
    mixins.RetrieveModelMixin,  # retrieve ---> get by pk
    mixins.UpdateModelMixin,    # update ---> put method
    mixins.DestroyModelMixin,   # destroy ---> delete method
    generics.GenericAPIView,
):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)
    
    def put(self, request, pk):
        return self.update(request)
    
    def delete(self, request, pk):
        return self.destroy(request)


## 6- Generics  (CBV) 
# 6.1 GET - POST
class generics_list(generics.ListCreateAPIView):
    # it has a predefined methods for list or list create .... etc.
    # list and create APIView.
    # it create GET and POST methods automatically.
    # it write the code of mixins for list and create.
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 6.2 GET - PUT - DELETE
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

## 7.viewsets (CBV)
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie', 'hall']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


## 8. Find a movie using (FBV)
@api_view(['GET'])
def find_moive(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )

    serializer = MovieSerializer(movies, many = True)
    return Response(serializer.data)

## 9. Create a new reservation using (FBV)
@api_view(['POST'])
def create_reservation(request):
    # in case of a new guest
    guest = Guest(name = request.data['name'],
                mobile = request.data['mobile'])
    guest.save()

    movie = Movie.objects.get(
        hall = request.data['hall'], 
        movie = request.data['movie']
        )
    
    reservation = Reservation(guest = guest, movie = movie)
    reservation.save()

    serializer = ReservationSerializer(reservation)
    return Response(serializer.data, status = status.HTTP_201_CREATED)

## 10 Post Author Editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorReadOnly]

    queryset = Post.objects.all()
    serializer_class = PostSerializer















