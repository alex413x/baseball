import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from baseball.serializers import UserSerializer, GroupSerializer, MatchSerializer, PlayerSerializer, PlayerDetailSerializer, StatSerializer, PitchSerializer
from baseball.models import Match, Player, Stat, Pitch, Average
from baseball.src.load_assets import load


def index(request):
    return HttpResponse('BB Index')


@require_http_methods(['GET', 'POST'])
def throw_pitch(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            print 'That wasn\'t JSON!'
            return HttpResponse('This isn\'t JSON!  Error', status=400)
        print 'Data: %s' % data
        return HttpResponse('Wow, got a post!  Here it is: \n%s' % data, status=200)
    return HttpResponse('Got!')


@require_http_methods(['GET'])
def load_averages(request):
    return HttpResponse('Got!')


@require_http_methods(['GET', 'POST'])
def load_player(request, playerID):
    if request.method == 'GET':
        print playerID
        data = load(playerID).stats
        player = Player()
        player.stats = data
        player.first_name = data['Master']['nameGiven']
        player.last_name = data['Master']['nameLast']
        player.save()
        return HttpResponse(json.dumps(player.stats))
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            print 'That wasn\'t JSON!'
            return HttpResponse('This isn\'t JSON!  Error', status=400)
        print 'Data: %s' % data
        return HttpResponse('Wow, got a post!  Here it is: \n%s' % data, status=200)
    return HttpResponse('Got!')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MatchList(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerDetailSerializer


class PitchList(generics.ListCreateAPIView):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer


class PitchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer


class StatList(generics.ListCreateAPIView):

    # def perform_create(self, serializer):
    #     serializer.save(player_id=self.request.user)

    queryset = Stat.objects.all()
    serializer_class = StatSerializer


class StatDetail(generics.RetrieveUpdateDestroyAPIView):

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    queryset = Stat.objects.all()
    serializer_class = StatSerializer
