function mousemove(){
    window.addEventListener('mousemove',function(dets){     // 'mousemove' action name on which the function will be triggered
        document.querySelector("#minicircle").style.transform = `translate(${dets.clientX}px, ${dets.clientY}px)`}); 
    
}

mousemove();