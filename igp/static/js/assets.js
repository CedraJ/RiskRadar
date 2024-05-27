// Get the modal
var modal = document.getElementById('addAssetModal');

// Get the button that opens the modal
var btn = document.getElementById('addAssetBtn');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function filterAssets() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("assetsTable");
  tr = table.getElementsByTagName("tr");

  for (i = 1; i < tr.length; i++) {
      tr[i].style.display = "none"; 
      for (var j = 0; j < tr[i].getElementsByTagName("td").length; j++) {
          td = tr[i].getElementsByTagName("td")[j];
          if (td) {
              txtValue = td.textContent || td.innerText;
              if (txtValue.toUpperCase().indexOf(filter) > -1) {
                  tr[i].style.display = "";
                  break; // Show the row if a match is found
              }
          }
      }
  }
}

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("assetsTable");
  switching = true;
  dir = "asc";
  
  while (switching) {
      switching = false;
      rows = table.getElementsByTagName("tr");
      for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("td")[n];
          y = rows[i + 1].getElementsByTagName("td")[n];
          
          if (dir == "asc") {
              if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                  shouldSwitch = true;
                  break;
              }
          } else if (dir == "desc") {
              if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                  shouldSwitch = true;
                  break;
              }
          }
      }
      if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          switchcount++;
      } else {
          if (switchcount == 0 && dir == "asc") {
              dir = "desc";
              switching = true;
          }
      }
  }
}
