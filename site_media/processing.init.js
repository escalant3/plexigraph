if(window.addEventListener){window.addEventListener("load",function(){var scripts=document.getElementsByTagName("script");
for(var i=0;i<scripts.length;i++){
    if(scripts[i].type=="application/processing"){
            canvas=document.getElementById("procanvas");
            if(canvas){Processing(canvas,scripts[i].text);}}}},false);}
