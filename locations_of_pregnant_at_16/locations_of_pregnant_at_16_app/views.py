import json
from django.shortcuts import render, redirect
from .forms import EpisodeForm
from .forms import HeroineForm
from .forms import FatherForm
from .forms import ChildForm
from .forms import MarkerForm
from .models import Marker
from .models import Episode


def home(request):
    return render(request, "home.html")


def map_view(request):
    markers = (
        Marker.objects.select_related("episode__heroine")
        .prefetch_related("episode__children", "episode__father")
        .all()
    )
    markers_data = []
    for marker in markers:
        season_number = (
            marker.episode.season_number if marker.episode else ""
        )
        episode_number = (
            marker.episode.episode_number if marker.episode else ""
        )
        heroine_name = (
            marker.episode.heroine.heroine_name
            if marker.episode and marker.episode.heroine
            else ""
        )
        heroine_age = (
            marker.episode.heroine.heroine_age
            if marker.episode and marker.episode.heroine
            else ""
        )
        children_names = [child.child_name for child in marker.episode.children.all()]
        created_at = marker.created_at.strftime("%Y-%m-%d %H:%M:%S")

        if marker.episode and hasattr(marker.episode, "father"):
            father_name = (
                marker.episode.father.father_name
                if marker.episode.father
                else ""
            )
            father_age = (
                marker.episode.father.father_age
                if marker.episode.father
                else ""
            )
            father_photo = (
                marker.episode.father.father_photo.url
                if marker.episode.father and marker.episode.father.father_photo
                else ""
            )
        else:
            father_name = ""
            father_age = ""
            father_photo = ""

        markers_data.append(
            {
                "season_number": season_number,
                "episode_number": episode_number,
                "latitude": marker.latitude,
                "longitude": marker.longitude,
                "heroine_name": heroine_name,
                "heroine_age": heroine_age,
                "children_names": children_names,
                "date_of_creation": created_at,
                "heroine_photo": (
                    marker.episode.heroine.heroine_photo.url
                    if marker.episode
                    and marker.episode.heroine
                    and marker.episode.heroine.heroine_photo
                    else ""
                ),
                "father_name": father_name,
                "father_age": father_age,
                "father_photo": father_photo,
            }
        )

    return render(request, "map.html", {"markers": json.dumps(markers_data)})
