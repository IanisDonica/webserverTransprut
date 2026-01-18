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

    missing = [key for key in ("score", "time", "playerHp") if key not in payload]
    if missing:
        return JsonResponse({"error": f"Missing fields: {', '.join(missing)}."}, status=400)

    ScoreEntry.objects.create(
        score=float(payload["score"]),
        time=float(payload["time"]),
        hp=int(payload["playerHp"]),
        ip=request.META.get("REMOTE_ADDR", ""),
    )

    return JsonResponse({"status": "ok"}, status=201)



def list_scores(request):
    entries = ScoreEntry.objects.order_by("-timestamp")
    return render(request, "scores/list.html", {"entries": entries})
