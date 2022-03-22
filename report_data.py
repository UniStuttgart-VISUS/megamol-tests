report_top = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
.coloredblock {
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.test {
  background-color: #80c0ff;
  color: black;
  padding-top: 6px;
  padding-bottom: 6px;
}

.failed {
  background-color: #ffd780;
  color: black;
  padding-top: 18px;
  padding-bottom: 18px;
}

.output {
  background-color: #ffd780;
  color: black;
  padding-top: 6px;
  padding-bottom: 6px;
}

.activetest, .test:hover, .activeoutput, .output:hover, .failed:hover {
  filter: drop-shadow(4px 4px 4px black);
}

.test:after, .output:after {
  content: '\\002B';
  color: white;
  font-weight: bold;
  float: right;
  margin-left: 5px;
}

.activetest:after {
  content: "\\2212";
}

.activeoutput::after {
  content: "\\2212";
}

.testcontent {
  padding: 0 18px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
  background-color: #f1f1f1;
}

.outputcontent {
  padding: 0 18px;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
  background-color: #f1f1f1;
}
</style>
</head>
<body>
"""

report_bottom = """
<script>
var coll = document.getElementsByClassName("test");
var coll2 = document.getElementsByClassName("output")
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("activetest");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

for (i = 0; i < coll2.length; i++) {
  coll2[i].addEventListener("click", function() {
    this.classList.toggle("activeoutput");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
    var parent = this.parentElement;
    if (parent.style.maxHeight) {
      parent.style.maxHeight = parseInt(parent.style.maxHeight) + content.scrollHeight + "px";
    } else {
      parent.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

</script>

</body>
</html>
"""