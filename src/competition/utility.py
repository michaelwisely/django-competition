from django.db.models import Q

def competitor_search_filter(queryset, search):
    # Split the full name on spaces
    if search != None:
        search = search.split(" ")
    else:
        search = []
    def jcq(q1,q2):
        if q1 == None:
            return q2
        return q1|q2        
    q = None
    for part in search:
        q = jcq(q,Q(username__icontains=part))
        q = jcq(q,Q(first_name__icontains=part))
        q = jcq(q,Q(last_name__icontains=part))
    queryset = queryset.filter(q)
    return queryset
