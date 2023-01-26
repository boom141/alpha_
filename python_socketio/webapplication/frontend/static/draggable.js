var dragElement = null;

// Mark TODO as complete

$("ul").on("click", "li", function(){
    $(this).toggleClass("completed");
});


// drag and drop effects

$("ul").on("dragstart","li",function(event){
    $(this).css("opacity", 0.4);
    dragElement = $(this);
    event.originalEvent.dataTransfer.effectAllowed = 'move';
    event.originalEvent.dataTransfer.setData('text/html', $(this).html());
});

$("ul").on("dragenter","li",function(){
    $(this).addClass("over");
});

$("ul").on("dragleave","li",function(){
    $(this).removeClass("over");
});


$("ul").on("dragover","li",function(event){
    if (event.preventDefault) {
        event.preventDefault(); // Necessary. Allows us to drop.
    }
  event.originalEvent.dataTransfer.dropEffect = 'move';  // See the section on the DataTransfer object.
  return false;
});

// drag and drop handle

$("ul").on("drop","li",function(event){
  if (event.stopPropagation) {
    event.stopPropagation(); 
  }

  if (dragElement != $(this)) {
    $(dragElement).html($(this).html())
    dragElement.innerHTML = this.innerHTML;
    this.innerHTML = event.originalEvent.dataTransfer.getData('text/html');
  }
  return false;
});

$("ul").on("dragend","li",function(){
    $("ul li").removeClass("over");
    $(this).css("opacity", 1);
});


// delete TODO span

$("ul").on("click", "li span", function(event){
    $(this).parent().fadeOut(1000, function(){
        $(this).remove();
    });
    event.stopPropagation(); 
});


// add TODO button

$("#add-todo").on("keypress", function(event){
    if(event.which === 13){
        var newToDo = "<li> <span><i class='fa fa-trash' aria-hidden='true'></i></span> "+$(this).val()+"</li>";
        $(this).fadeOut(500, function(){
            $("ul").prepend(newToDo);
            $(this).val("");
        
        });
      $("#toggle").toggleClass("fa-minus-square");
      $("#toggle").toggleClass("fa-plus-square");
    }
});


// toggle icon 

$("#toggle").on("click", function(){
    $(this).toggleClass("fa-plus-square");
    $(this).toggleClass("fa-minus-square");
    $("#add-todo").slideToggle(400);
});