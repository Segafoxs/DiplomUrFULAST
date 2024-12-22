
$(document).ready(function(){
 $("#countInp").keyup(function(){
       var count = parseInt($(this).val());
       for(i=1;i <= count; i++)
{
 $('#btnSub').before('<input type="text" class="newInp" name="f'+i+'"/>')

}
      });




 });/*end  ready*/
