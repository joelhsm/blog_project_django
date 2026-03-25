from .models import SiteSetup

def context_processor(request):
    return {
        'site_setup': SiteSetup.objects.first(),
    }