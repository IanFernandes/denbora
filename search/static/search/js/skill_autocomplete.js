$("#autocompletar").autocomplete({
    minLenght: 0,
    source: "autocomplete_skill/",
    focus: function( event, ui ) {
        $("#autocompletar").val( ui.item.label );
        return false;
    }
});