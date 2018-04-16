var jobsTab = document.getElementById("tab-jobs");
var aboutTab = document.getElementById("tab-about");

function smoothScroll(ele){
   document.getElementById(ele).scrollIntoView({ 
   behavior: 'smooth' 
  });
}

jobsTab.addEventListener("click", () => {smoothScroll("jobs-list")}, false);
aboutTab.addEventListener("click", () => { smoothScroll("aboutContent")}, false);