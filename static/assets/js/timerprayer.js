window.onload = new function() {
    var soundHandler = null;  
    var typeTimeFormat = 'en-GB';
    var timeZoneOptions = { timeZone: 'UTC',year: "numeric", month: "numeric",day: "numeric"};
    var myVar = setInterval(myTimer, 1000); 
    var played =false;
    Number.prototype.pad = function(size) {
      var s = String(this);
      while (s.length < (size || 2)) { s = "0" + s;}
      return s;
    }
    function msToHMS( ms ) {
        var seconds = ms / 1000;
        var hours = parseInt( seconds / 3600 );
        seconds = seconds % 3600;
        var minutes = parseInt( seconds / 60 );
        seconds = parseInt(seconds % 60);
        return hours.pad(2)+":"+minutes.pad(2)+":"+seconds.pad(2);
    }
    
    function getCityDate(){
        var d = new Date();
        var utc = d.getTime() + (d.getTimezoneOffset() * 60000);
        var thecitytimenow = new Date(utc + (3600000*city_offset));
        return thecitytimenow;
    }
    var untildate = getCityDate().getTime()+ reminingtime;
    function myTimer() {
    thecitytimenow = getCityDate();
        document.getElementById("timenowinthecity").innerHTML = thecitytimenow.toLocaleTimeString(typeTimeFormat,{hour12:true}).toUpperCase();
        var diff = untildate - thecitytimenow.getTime(); //in s     
        if(diff <= 0){
            if(!played){
                soundHandler = new Audio('//'+ clean_url +'/sounds/' + soundfile + '.mp3');  
                praySound();
                played= true;
            } 
        }else{
        document.getElementById("countdown").innerHTML = msToHMS(diff);
        }
    }
    function praySound(){
        document.getElementById("countdown").innerHTML = '00:00:00';
        playAzan();
        setTimeout(function(){
            location.reload();
        }, douration_sound*1000);
    }
    
    
    function playAzan() { 
        if(!soundHandler.paused){
        }else{
            soundHandler.play(); 
        }
    } 
    
    function pauseAzan() { 
        soundHandler.pause(); 
    } 
    
    
      }
    
    function showHideEle(elm) {
        var x = document.getElementById(elm);
        if (x.style.display === "block") {
            x.style.display = "none";
        } else {
            x.style.display = "block";
        }
    }
    function changeSettings(){
        var method = document.getElementById("method").value;
        var asr = document.getElementById("asr").value;
        var time = document.getElementById("time").value;
        window.location.href =  '//' + base_url + '/prayer-times-in-' + city_url + '-m' + method + 'j' + asr + 't' + time + '.html';
    }