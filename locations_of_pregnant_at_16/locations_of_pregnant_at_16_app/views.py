from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import modelformset_factory
from .models import Child, Episode, Heroine, Father, Marker
from .forms import (
    EpisodeForm,
    HeroineForm,
    FatherForm,
    MarkerForm,
    child_formset_factory,
)
from django.forms import inlineformset_factory
from django.utils import timezone
import json
from django.contrib import messages


def home(request):
    return render(request, "home.html")


def map_view(request):
    markers = (
        Marker.objects.select_related("episode__heroine")
        .prefetch_related("episode__children", "episode__father")
        .filter(is_deleted=False)
        .all()
    )
    markers_data = []
    for marker in markers:
        season_number = marker.episode.season_number if marker.episode else ""
        episode_number = marker.episode.episode_number if marker.episode else ""
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
                marker.episode.father.father_name if marker.episode.father else ""
            )
            father_age = (
                marker.episode.father.father_age if marker.episode.father else ""
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
                "id_marker": marker.id_marker,
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


def delete_marker(request, marker_id):
    if request.method == "POST":
        try:
            marker = Marker.objects.get(id_marker=marker_id)
            print(marker_id)
            marker.is_deleted = True
            marker.save()
            return JsonResponse({"success": True})
        except Marker.DoesNotExist:
            return JsonResponse({"success": False, "error": "Метка не найдена"})
    return JsonResponse({"success": False, "error": "Неверный метод"})


def edit_marker(request, marker_id):
    marker = get_object_or_404(Marker, id_marker=marker_id)
    episode = marker.episode
    heroine = episode.heroine
    father = episode.father if hasattr(episode, "father") else None
    children = episode.children.all()

    if request.method == "POST":
        episode_form = EpisodeForm(request.POST, instance=episode)
        heroine_form = HeroineForm(request.POST, request.FILES, instance=heroine)
        father_form = FatherForm(request.POST, request.FILES, instance=father)
        marker_form = MarkerForm(request.POST, instance=marker)

        ChildFormSet = child_formset_factory(len(children))
        child_formset = ChildFormSet(request.POST, queryset=children, prefix="child_set")

        if (
            episode_form.is_valid()
            and heroine_form.is_valid()
            and marker_form.is_valid()
            and child_formset.is_valid()
        ):
            episode_form.save()
            heroine_form.save()
            if father_form.is_valid() and father_form.cleaned_data.get("father_name"):
                father_form.save()

            marker_form.save()

            for child_form in child_formset:
                if child_form.is_valid():
                    child = child_form.save(commit=False)
                    child.episode = episode 
                    child.save()

            return redirect("map_view")

    else:
        episode_form = EpisodeForm(instance=episode)
        heroine_form = HeroineForm(instance=heroine)
        father_form = FatherForm(instance=father)
        marker_form = MarkerForm(instance=marker)

        ChildFormSet = child_formset_factory(len(children))
        child_formset = ChildFormSet(queryset=children, prefix="child_set")

    context = {
        "episode_form": episode_form,
        "heroine_form": heroine_form,
        "father_form": father_form,
        "marker_form": marker_form,
        "child_formset": child_formset,
        "marker_id": marker.id_marker,
    }

    return render(request, "edit_marker.html", context)


def create_marker(request):
    if request.method == "POST":
        episode_form = EpisodeForm(request.POST)
        heroine_form = HeroineForm(request.POST, request.FILES)
        father_form = FatherForm(request.POST, request.FILES)
        marker_form = MarkerForm(request.POST)

        child_count = int(request.POST.getlist("child_set-TOTAL_FORMS")[0])

        ChildFormSet = child_formset_factory(child_count)
        child_formset = ChildFormSet(
            request.POST, queryset=Child.objects.none(), prefix="child_set"
        )

        if (
            episode_form.is_valid()
            and heroine_form.is_valid()
            and marker_form.is_valid()
            and child_formset.is_valid()
        ):
            season_number = episode_form.cleaned_data["season_number"]
            episode_number = episode_form.cleaned_data["episode_number"]

            existing_episode = Episode.objects.filter(
                season_number=season_number, episode_number=episode_number
            ).last()
            print(existing_episode)

            if existing_episode:
                existing_marker = Marker.objects.filter(
                    episode=existing_episode, is_deleted=False
                ).last()
                if existing_marker:
                    messages.error(request, "Данные об этом эпизоде уже добавлены!")

                else:
                    episode = episode_form.save()

                    heroine = heroine_form.save(commit=False)
                    heroine.episode = episode
                    heroine.save()

                    if father_form.is_valid() and father_form.cleaned_data.get(
                        "father_name"
                    ):
                        father = father_form.save(commit=False)
                        father.episode = episode
                        father.save()

                    latitude = marker_form.cleaned_data["latitude"]
                    longitude = marker_form.cleaned_data["longitude"]

                    existing_marker = (
                        Marker.objects.filter(latitude=latitude, longitude=longitude)
                        .exclude(is_deleted=True)
                        .first()
                    )

                    if existing_marker:
                        messages.error(
                            request, "Метка с такими координатами уже существует!"
                        )

                    else:
                        marker = marker_form.save(commit=False)
                        marker.episode = episode
                        marker.save()

                        for child_form in child_formset:
                            if child_form.is_valid():
                                child = child_form.save(commit=False)
                                child.episode = episode
                                child.save()

                        return redirect("map_view")

            else:
                episode = episode_form.save()

                heroine = heroine_form.save(commit=False)
                heroine.episode = episode
                heroine.save()

                if father_form.is_valid() and father_form.cleaned_data.get(
                    "father_name"
                ):
                    father = father_form.save(commit=False)
                    father.episode = episode
                    father.save()

                latitude = marker_form.cleaned_data["latitude"]
                longitude = marker_form.cleaned_data["longitude"]

                existing_marker = (
                    Marker.objects.filter(latitude=latitude, longitude=longitude)
                    .exclude(is_deleted=True)
                    .first()
                )

                if existing_marker:
                    messages.error(
                        request, "Метка с такими координатами уже существует!"
                    )

                else:
                    marker = marker_form.save(commit=False)
                    marker.episode = episode
                    marker.save()

                    for child_form in child_formset:
                        if child_form.is_valid():
                            child = child_form.save(commit=False)
                            child.episode = episode
                            child.save()

                    return redirect("map_view")

    else:
        episode_form = EpisodeForm()
        heroine_form = HeroineForm()
        father_form = FatherForm()
        marker_form = MarkerForm()

        ChildFormSet = child_formset_factory(1)
        child_formset = ChildFormSet(queryset=Child.objects.none(), prefix="child_set")

    context = {
        "episode_form": episode_form,
        "heroine_form": heroine_form,
        "father_form": father_form,
        "marker_form": marker_form,
        "child_formset": child_formset,
    }

    return render(request, "create_marker.html", context)
