/* ===========================
   HORAM PRINTER
   Professional JavaScript
=========================== */


/* ===========================
   Page Loader
=========================== */

window.addEventListener("load", function(){

    let loader = document.querySelector(".loader");

    if(loader){
        loader.style.display="none";
    }

});


/* ===========================
   Smooth Scroll
=========================== */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function(e){

        e.preventDefault();

        document.querySelector(this.getAttribute("href"))
        .scrollIntoView({
            behavior:"smooth"
        });

    });

});


/* ===========================
   Navbar Scroll Effect
=========================== */

window.addEventListener("scroll",function(){

    let header=document.querySelector("header");

    if(window.scrollY > 50){

        header.style.background="#111";

    }

    else{

        header.style.background="#000";

    }

});



/* ===========================
   Back To Top Button
=========================== */

let topBtn=document.createElement("button");

topBtn.innerHTML="⬆";

topBtn.className="top-btn";

document.body.appendChild(topBtn);


window.addEventListener("scroll",()=>{

    if(window.scrollY > 300){

        topBtn.style.display="block";

    }

    else{

        topBtn.style.display="none";

    }

});


topBtn.onclick=function(){

    window.scrollTo({

        top:0,
        behavior:"smooth"

    });

};



/* ===========================
   Scroll Reveal Animation
=========================== */


let cards=document.querySelectorAll(".card");


window.addEventListener("scroll",()=>{


cards.forEach(card=>{


let position=card.getBoundingClientRect().top;

let screen=window.innerHeight;


if(position < screen - 100){

card.style.opacity="1";

card.style.transform="translateY(0)";


}


});


});



/* ===========================
   WhatsApp Button
=========================== */


let whatsapp=document.createElement("a");


whatsapp.href="https://wa.me/923057877809";

whatsapp.target="_blank";

whatsapp.innerHTML="💬";


whatsapp.className="whatsapp-btn";


document.body.appendChild(whatsapp);