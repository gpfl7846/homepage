$(document).ready(function(){
$('[data-toggle="popover"]').popover({
  trigger: 'hover',
 'placement': 'right',
  'title' : '선수정보',
  'content' : hoverGetData,
  'html': true
});

function hoverGetData(){
 var id=$(this).attr('value');
 console.log(id);
 console.log('test');
  $.ajax({
    url:'/player_popup',
    type:'POST',
    data:{'player_pk':id},
    async: false,
    success: function(response){
        localData = response;
    },
    error:function(){
            console.log('error');
        },
    complete:function(){
            console.log('complete');
        }

});
  return localData
}
});