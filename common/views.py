from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect


class TitleMixin:
    title = None
    context_title_name = 'title'

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        context[self.context_title_name] = f'StoreTracker | {title}' if title else 'StoreTracker'
        return context


class LogoutRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class PaginationUrlMixin:
    context_pagination_url_name = 'pagination_url'

    def get_pagination_url(self):
        return '?page='

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_pagination_url_name] = self.get_pagination_url()
        return context


class UserViewTrackingMixin:
    """Tracking of whether the user called a view during a some time."""

    view_tracking_cache_key = ''
    view_tracking_cache_time = 60

    def get_view_tracking_cache_key(self):
        return self.view_tracking_cache_key

    def get_view_tracking_cache_time(self):
        return self.view_tracking_cache_time

    def get(self, *args, **kwargs):
        response = super().get(*args, **kwargs)
        if self._has_viewed(self.request):
            self.user_viewed()
        else:
            self.user_not_viewed()
        return response

    def user_viewed(self):
        """Logic if the user has already called this view."""
        pass

    def user_not_viewed(self):
        """Logic if the user has not yet called this view."""
        pass

    def _has_viewed(self, request):
        key = self.get_view_tracking_cache_key()

        is_exists = cache.get(key)

        if is_exists:
            return True
        cache.set(key, True, self.get_view_tracking_cache_time())
        return False
