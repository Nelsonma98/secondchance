from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from panel.services.dashboard import get_panel_context


@login_required
def panel(request):
    return render(request, 'panel.html', get_panel_context())
