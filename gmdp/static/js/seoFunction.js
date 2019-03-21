//random image in the donation page
function setRandomImage( img_array ) {
    var len = img_array.length;
    var randIndex = Math.floor(len * Math.random());
    var randElt = img_array[randIndex];
    $("#top_image").attr("src", randElt);
}

setRandomImage( [ "img/donate/random1.jpg",
                  "img/donate/random2.jpg",
                  "img/donate/random3.jpg",
                  "img/donate/random4.jpg",
                  "img/donate/random5.jpg" ] );


//slideshow function in the application page
var scrollTime = 300; // ms for the animation to run

// Find how many slides are in the entire list of images
var totalNumberOfSlides = $("#slides li").length;

// Find the length of each slide in the carousel. This code makes the
// assumption that they all have the same width. If that's not so, the
// amount of scrolling will be incorrect.
var slideLength = parseInt($("#slides li").css("width"));

// Global variable. Since we already show a picture in carousel, that is
// slide number 0.
var currentSlide = 0;

/* Function to change to a different slide, where direction is either +1
 * to advance or -1 to go to the previous slide..  */
/* Function to change to a different slide, where direction is either +1
 * to advance or -1 to go to the previous slide..  */
function slide_goto(slideNumber) {
    console.log("Going to slide "+slideNumber);

    // The scrollLength is actually how much of the slide container will
    // be out of view (to the left of the shown slide)
    var scrollLength = (slideNumber * slideLength);
    $("#slides ul").animate({left: -scrollLength}, scrollTime);

  }

function slide_next() {
    currentSlide++;  // move onto the next slide

    // if showing the last slide, then circle back to the first one
    if (currentSlide >= totalNumberOfSlides) {
        currentSlide = 0;
    }
    slide_goto(currentSlide);
}

function slide_prev() {
    currentSlide--;  // move to the previous slide

    if (currentSlide < 0) {
        currentSlide = totalNumberOfSlides - 1; // last slide number
    }
    slide_goto(currentSlide);
}

$("#arrowright").click(slide_next);
$("#arrowleft").click(slide_prev);


//Enlarge image
// Get the modal
var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
    modal.style.display = "none";
}

// Get all images and insert the clicked image inside the modal
// Get the content of the image description and insert it inside the modal image caption
var images = document.getElementsByTagName('img');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var i;
for (i = 0; i < images.length; i++) {
   images[i].onclick = function(){
      modal.style.display = "block";
      modalImg.src = this.src;
      modalImg.alt = this.alt;
      captionText.innerHTML = this.nextElementSibling.innerHTML;
   }
}

/* Drop Down Menu */
function dropDownMenu() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
