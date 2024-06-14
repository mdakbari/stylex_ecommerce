from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from .utils import encode_id, decode_id

class OrderIdHashMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        hashed_order_id = view_kwargs.get('hashed_order_id')

        if hashed_order_id:
            order_id = decode_id(hashed_order_id)
            if order_id is None:
                # Handle invalid hash
                return redirect('error_page')  # Replace with your actual error page
            # Replace the hashed_order_id with the actual order_id
            view_kwargs['order_id'] = order_id
            del view_kwargs['hashed_order_id']
        
        return None
    