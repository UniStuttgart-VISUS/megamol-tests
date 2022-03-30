report_top = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
table {
  border-spacing: 0;
}

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
  width: 90%;
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
  width: 90%;
}

.img-diff-container {
  position: relative;
  width: 100%;
}

.img-diff-reference {
  display: block;
  width: 100%;
}

.img-diff-result {
  position: absolute;
  bottom: 0;
  mix-blend-mode: difference;
  z-index: 2;
  width: 100%;
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

var thresh = document.getElementsByName("SSIM_Threshold")[0]
var search_thing = "SSIM = "
thresh.addEventListener("input", function(e) {
  var ref_num = parseFloat(thresh.value)
    for (i = 0; i < coll.length; i++) {
    var off = coll[i].textContent.indexOf(search_thing)
    var maybe_num = coll[i].textContent.substring(off + search_thing.length)
        var num = parseFloat(maybe_num)
    if (num < ref_num) {
      if (!coll[i].classList.contains("failed")) {
        coll[i].classList.add("failed")
      }
    } else {
      coll[i].classList.remove("failed")
    }
  }
})

</script>

</body>
</html>
"""