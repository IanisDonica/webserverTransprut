import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import ScoreEntry

@csrf_exempt
@require_POST
def create_score(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    missing = [key for key in ("score", "time", "playerHp", "level") if key not in payload]
    if missing:
        return JsonResponse({"error": f"Missing fields: {', '.join(missing)}."}, status=400)

    level = int(payload["level"])
    if level not in range(1, 6):
        return JsonResponse({"error": "Level must be between 1 and 5."}, status=400)

    ScoreEntry.objects.create(
        score=float(payload["score"]),
        time=float(payload["time"]),
        hp=int(payload["playerHp"]),
        level=level,
    )

    return JsonResponse({"status": "ok"}, status=201)

def list_scores(request):
    levels = [1, 2, 3, 4, 5]
    boards = []
    total_records = 0
    for level in levels:
        base_qs = ScoreEntry.objects.filter(level=level)
        total_records += base_qs.count()
        top_four = list(base_qs.order_by("-score", "-timestamp")[:4])
        most_recent = base_qs.order_by("-timestamp").first()
        boards.append(
            {
                "level": level,
                "label": f"Level {level}",
                "top_score": top_four[0] if top_four else None,
                "other_scores": top_four[1:],
                "most_recent": most_recent,
                "total": base_qs.count(),
            }
        )

    return render(
        request,
        "scores/list.html",
        {
            "boards": boards,
            "total_records": total_records,
        },
    )


def list_scores_by_level(request, level):
    if level not in range(1, 6):
        return JsonResponse({"error": "level shuld be 1-5"}, status=400)

    allowed_sorts = {
        "score": "score",
        "time": "time",
        "hp": "hp",
        "timestamp": "timestamp",
        "level": "level",
    }
    sort = request.GET.get("sort", "score")
    direction = request.GET.get("dir", "desc")
    sort_key = allowed_sorts.get(sort, "score")
    sort_prefix = "-" if direction == "desc" else ""
    order_by = f"{sort_prefix}{sort_key}"

    entries = ScoreEntry.objects.filter(level=level).order_by(order_by, "-timestamp")
    label = f"Level {level}"
    return render(
        request,
        "scores/level_list.html",
        {
            "entries": entries,
            "level": level,
            "label": label,
            "sort": sort_key,
            "dir": direction,
        },
    )
