$("#autocompletar").autocomplete({
    minLenght: 0,
    source: "autocomplete_skill/",
    select: function (event, ui) {
        $("#skillid").val(ui.item.id); // save selected id to hidden input
    },
    focus: function( event, ui ) {
        $("#autocompletar").val( ui.item.label );
        return false;
    }
});