var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value;
  const rows = document.querySelectorAll('#myTable tr:not(.header)');
  rows.forEach(tr => tr.style.display = parseInt(tr.children[3].innerHTML) < parseInt(output.innerHTML) ? '' : 'none');
}
