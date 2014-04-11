$(function() {
    var objects = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        limit: 10,
        prefetch: {
            url: window.typeahead_url,
            filter: function(list) {
                return list;
            }
        }
    });

    objects.initialize();

    $('#prefetch').typeahead(null, {
        name: 'objects',
        displayKey: 'name',
        source: objects.ttAdapter()
    }).on('typeahead:selected', function(e, object, dataset) {
        document.location = object['url'];
    });
});
