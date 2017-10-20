
var tds = document.getElementsByTagName("td");
for(var i = 0; i < tds.length; i++) {
tds[i].onmouseover = function() {
 this.parentNode.style.backgroundColor = "#ccc";
}
tds[i].onmouseout = function() {
this.parentNode.style.backgroundColor = "white";
}
}


function handleSelect(dni)
{
  var url = "liquidacion/0".replace('0', dni);
  nueva = window.location.href.replace('agentes_a_cargo', url)
  window.location.href = nueva;
}

// codigo perteneciente a la tabla (apuntar a la vista y paginacion)
$(document).ready(function($) {
  $(".paginate").click(function() {
    window.location = $(this).data("href");
   });

 });

 $(function($) {
    // Grab whatever we need to paginate
    var pageParts = $(".paginate");

    // How many parts do we have?
    var numPages = pageParts.length;
    // How many parts do we want per page?
    var perPage = 8;

    // When the document loads we're on page 1
    // So to start with... hide everything else
    pageParts.slice(perPage).hide();
    // Apply simplePagination to our placeholder
    $("#page-nav").pagination({
        items: numPages,
        itemsOnPage: perPage,
        cssStyle: "light-theme",
        // We implement the actual pagination
        //   in this next function. It runs on
        //   the event that a user changes page
        onPageClick: function(pageNum) {
            // Which page parts do we show?
            var start = perPage * (pageNum - 1);
            var end = start + perPage;
            // First hide all page parts
            // Then show those just for our page
            pageParts.hide().slice(start, end).show();
        }
      });
  });


// filtro para meses

function toggle(source) {
    checkboxes = document.getElementsByName('check');
    for(var i=0, n=checkboxes.length;i<n;i++) {
      checkboxes[i].checked = source.checked;}}

function funcion(documento){
  window.location.href="{% url 'liquidaciones_a_pdf' documento=0 %}".replace(0,documento);
}
