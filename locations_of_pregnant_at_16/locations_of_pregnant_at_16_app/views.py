from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import ValidationError, modelformset_factory
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
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "home.html")


def map_view(request):
    return render(request, "map.html")


def markers_view(request):
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

    return HttpResponse(json.dumps(markers_data))


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


def get_marker_by_id(request, id):
    """
    Возвращает данные маркера и связанной информации о героине, отце и детях.
    """
    marker = get_object_or_404(Marker, id_marker=id)
    episode = marker.episode

    marker_data = {
        "id_marker": marker.id_marker,
        "latitude": marker.latitude,
        "longitude": marker.longitude,
        "date_of_creation": marker.created_at,
        "season_number": episode.season_number,
        "episode_number": episode.episode_number,
        "city": episode.city,
    }

    heroine_data = {
        "id_heroine": episode.heroine.id_heroine,
        "heroine_name": episode.heroine.heroine_name,
        "heroine_age": episode.heroine.heroine_age,
        "heroine_photo": (
            episode.heroine.heroine_photo.url if episode.heroine.heroine_photo else None
        ),
    }

    father_data = (
        {
            "id_father": episode.father.id_father,
            "father_name": episode.father.father_name,
            "father_age": episode.father.father_age,
            "father_photo": (
                episode.father.father_photo.url if episode.father.father_photo else None
            ),
        }
        if hasattr(episode, "father") and episode.father is not None
        else None
    )

    children = list(episode.children.all())
    children_label = (
        "Ребенок:"
        if len(children) == 1
        else "Ребенок" if len(children) > 1 else "Нет детей"
    )
    children_data = [
        {"id_child": child.id_child, "child_name": child.child_name}
        for child in children
    ]

    response_data = {
        "marker": marker_data,
        "heroine": heroine_data,
        "father": father_data,
        "children": {
            "label": children_label,
            "data": children_data,
        },
    }

    return JsonResponse(response_data)


@csrf_exempt
def edit_marker(request, marker_id):
    marker = get_object_or_404(Marker, id_marker=marker_id)
    episode = marker.episode
    heroine = episode.heroine
    father = episode.father if hasattr(episode, "father") else None
    children = episode.children.all()

    if request.method == "POST":
        csrf_token = request.META.get("HTTP_X_CSRFTOKEN")
        print(csrf_token)
        if not csrf_token:
            print({"error": "CSRF token missing"}, status=403)
        data = json.loads(request.body)

        try:
            # Обновление данных метки
            marker.latitude = data.get("latitude", marker.latitude)
            marker.longitude = data.get("longitude", marker.longitude)
            marker.save()

            # Обновление данных эпизода
            episode.season_number = data.get("season_number", episode.season_number)
            episode.episode_number = data.get("episode_number", episode.episode_number)
            episode.city = data.get("city", episode.city)
            episode.save()

            # Обновление данных героини
            heroine.heroine_name = data["heroine"].get(
                "heroine_name", heroine.heroine_name
            )
            heroine.heroine_age = data["heroine"].get(
                "heroine_age", heroine.heroine_age
            )
            heroine.save()

            # Обновление данных отца
            if "father" in data and data["father"]:
                if not father:
                    from .models import Father

                    father = Father(episode=episode)
                father.father_name = data["father"].get(
                    "father_name", father.father_name
                )
                father.father_age = data["father"].get("father_age", father.father_age)
                father.save()

            # Обновление данных детей
            if "children" in data:
                from .models import Child

                child_ids = (
                    []
                )  # Список идентификаторов детей, которые остаются связанными с эпизодом
                for child_data in data["children"]:
                    # Обновление данных детей
                    if "children" in data:
                        child_ids = (
                            []
                        )  # Список идентификаторов детей, которые остаются связанными с эпизодом
                        for child_data in data["children"]:
                            if "id_child" in child_data and child_data["id_child"]:
                                # Обновляем существующих детей
                                child = get_object_or_404(
                                    Child, id_child=child_data["id_child"]
                                )
                                child.child_name = child_data.get(
                                    "child_name", child.child_name
                                )
                                child.save()
                                child_ids.append(child.id_child)

                        # Удаляем детей, которые были связаны с эпизодом, но больше не переданы в данных
                        episode.children.exclude(id_child__in=child_ids).delete()

            return JsonResponse({"message": "Метка успешно обновлена."})
        except ValidationError as e:
            return JsonResponse(
                {"message": "Ошибка валидации данных.", "errors": e.message_dict},
                status=400,
            )
        except Exception as e:
            return JsonResponse(
                {"message": "Ошибка обновления данных.", "errors": str(e)}, status=400
            )

    if request.method == "GET":
        marker_data = {
            "marker": {
                "season_number": marker.episode.season_number,
                "episode_number": marker.episode.episode_number,
                "city": marker.episode.city,
                "latitude": marker.latitude,
                "longitude": marker.longitude,
            },
            "heroine": {
                "heroine_name": heroine.heroine_name,
                "heroine_age": heroine.heroine_age,
            },
            "father": {
                "father_name": father.father_name if father else "",
                "father_age": father.father_age if father else "",
            },
            "children": [
                {"id_child": child.id_child, "child_name": child.child_name}
                for child in children
            ],
        }
        return JsonResponse(marker_data)

    return JsonResponse({"message": "Метод не поддерживается."}, status=405)
