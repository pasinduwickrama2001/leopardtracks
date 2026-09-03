from django import template

register = template.Library()

@register.filter(name='cloudinary_opt')
def cloudinary_opt(url, width=None):
    """
    Transforms a Cloudinary URL to automatically deliver optimal format (WebP/AVIF)
    and quality compression (f_auto,q_auto) with optional responsive width constraint.
    Usage: {{ image_url|cloudinary_opt:800 }} or {{ image_url|cloudinary_opt }}
    """
    if not url or not isinstance(url, str):
        return url
    
    url = url.strip()
    if 'res.cloudinary.com' not in url or '/image/upload/' not in url:
        return url
    
    if 'f_auto' in url or 'q_auto' in url:
        return url
    
    transform_parts = ['f_auto', 'q_auto']
    if width:
        transform_parts.append(f'w_{width}')
        transform_parts.append('c_limit')
    
    transform_str = ','.join(transform_parts) + '/'
    return url.replace('/image/upload/', f'/image/upload/{transform_str}')
