
var modal = document.getElementById("id01");

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.formHasErrors = {% if form.errors %}true{% else %}false{% endif %};
</script>

<script>
$( document ).ready(function() {
   if (document.formHasErrors) {
       $('#id01').modal('toggle');
   }
});
        
                                                                 
var slideIndex = 0;
carousel();

function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > x.length) {slideIndex = 1}
    x[slideIndex-1].style.display = "block";
    setTimeout(carousel, 5000);
}

                                                                 
                                                                 
                                                                 
                                                                 
                                                                 
                                                                 